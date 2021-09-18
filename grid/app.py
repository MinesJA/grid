from uvicorn import Config
import sys
import os
import asyncio
import falcon
import falcon.asgi
from falcon import media
import signal
import aiohttp
from grid.models.node import Node
from grid.models.mailRoom import MailRoom
from grid.server import Server
from grid.services.messageService import MessageService
from grid.services.serializer import deserialize, serialize
from grid.resources.messaging import Messaging
from grid.cli import parse_args
from grid.clockcycle import Scheduler
from solana.rpc.async_api import AsyncClient
from solana.publickey import PublicKey
from solana.account import Account
from solana.transaction import Transaction, TransactionInstruction, AccountMeta



# TODO: Need to break this apart. Getting big

"""
Message System
==============
Producer:
    - server.serve()
    Receives http requests and "produces" messages
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

INBOX = asyncio.Queue()
OUTBOX = asyncio.Queue()
SESSION = aiohttp.ClientSession()
ARGS = parse_args(sys.argv[1:])
SOLANA_CLIENT_URL = 'https://api.devnet.solana.com'

SCHEDULER = Scheduler.every(5, )


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


def handle_exit(server, task_manager):
    # Stop the background schedule thread
    SCHEDULER.stop()
    server.exit()
    task_manager.exit()

node = Node(name=ARGS.name,
            id=ARGS.id,
            host=ARGS.host,
            port=ARGS.port,
            production=0,
            consumption=0)

mailroom = MailRoom(outbox=OUTBOX)

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

    for sig in HANDLED_SIGNALS:
        loop.add_signal_handler(sig, handle_exit, server, message_service)

    SCHEDULER.start()

    loop.run_until_complete(
        asyncio.gather(
            server_task,
            in_msg_task,
            out_msg_task,
            run_solana_client,
            loop=loop
        ))

    print(f'GRID:   Successfully exited Grid')

    # TODO: setup logging
    # create logging branch
    # https://docs.python.org/3/library/logging.html
