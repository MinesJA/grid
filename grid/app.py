from uvicorn import Config
import sys
import os
import asyncio
import argparse
import falcon
import falcon.asgi
from falcon import media
import signal
import aiohttp
from grid.models.node import Node
from grid.models.mailRoom import MailRoom
from grid.server import Server
from grid.services.messageService import MessageService
from grid.services.serializer import *
from grid.resources.messaging import Messaging

"""
Message System
==============
Producer:
    - server.serve()
    Receices http requests and "produces" messages
    placing them in the message inbox

Inbox:
    - asyncio.Queue()
    A queue for storing and processing incoming messages

Consumer:
    - task_manager.process_messages(inbox, node)
    Looks for messages to process in Queue
    and calls node.on_receive with message
    when one comes up
"""

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


def create_app(inbox, token, name):
    app = falcon.asgi.App()
    json_handler = media.JSONHandler(
        loads=deserialize,
    )
    extra_handlers = {
        'application/json': json_handler,
    }

    app.req_options.media_handlers.update(extra_handlers)
    app.resp_options.media_handlers.update(extra_handlers)

    messaging = Messaging(inbox=inbox)
    app.add_route('/messaging', messaging)
    return app


def parse_args(args):
    return create_parser().parse_args(args)


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--name', '-n')
    parser.add_argument('--id', '-i', type=int)
    parser.add_argument('--token', '-t')
    parser.add_argument('--host', '-s')
    parser.add_argument('--port', '-p', type=int)
    return parser


INBOX = asyncio.Queue()
OUTBOX = asyncio.Queue()
SESSION = aiohttp.ClientSession()
ARGS = parse_args(sys.argv[1:])


def handle_exit(server, task_manager):
    server.exit()
    task_manager.exit()


mailroom = MailRoom(outbox=OUTBOX)


node = Node(name=ARGS.name,
            id=ARGS.id,
            host=ARGS.host,
            port=ARGS.port,
            production=10,
            consumption=5)

app = create_app(inbox=INBOX, token=ARGS.token, name=ARGS.name)

loop = asyncio.get_event_loop()

config = Config(app=app, host=ARGS.host, port=ARGS.port, loop=loop)
server = Server(config)
message_service = MessageService()

if __name__ == "__main__":
    print(f'Grid:   Starting Grid')
    print(f'Grid:   Created Node: {node.id}')
    print(f'GRID:   pid {os.getpid()}: send SIGINT or SIGTERM to exit.')

    server_task = loop.create_task(server.serve())
    in_msg_task = loop.create_task(
        message_service.process_incoming(INBOX, node, mailroom)
    )
    out_msg_task = loop.create_task(
        message_service.process_outgoing(OUTBOX, SESSION)
    )

    # TODO: Do we need this?
    tasks = [server_task, in_msg_task, out_msg_task]

    for sig in HANDLED_SIGNALS:
        loop.add_signal_handler(sig, handle_exit, server, message_service)

    loop.run_until_complete(
        asyncio.gather(
            server_task,
            in_msg_task,
            out_msg_task,
            loop=loop
        ))

    print(f'GRID:   Successfully exited Grid')

    # TODO: setup logging
    # create logging branch
    # https://docs.python.org/3/library/logging.html
