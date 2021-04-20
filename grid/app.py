from uvicorn import Config
import sys
import os
import asyncio
import argparse
import falcon.asgi
import signal
from grid.models.node import Node
from grid.server import Server
from grid.services.task_manager import TaskManager
from grid.auth_middleware import AuthMiddleware
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
    app = falcon.asgi.App(middleware=AuthMiddleware(token, name))

    messaging = Messaging(inbox=inbox)
    app.add_route('/ask/{type}', messaging, suffix='ask')
    app.add_route('/tell/{type}', messaging, suffix='tell')

    # nodes = Nodes(inbox)
    # app.add_route('/nodes/siblings', nodes, suffix='siblings')
    # app.add_route('/nodes/energy', nodes, suffix='energy')
    return app


def parse_args(args):
    return create_parser().parse_args(args)


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--name', '-n')
    parser.add_argument('--token', '-t')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p', type=int)
    return parser


def handle_exit(server, task_manager):
    server.exit()
    task_manager.exit()


INBOX = asyncio.Queue()
ARGS = parse_args(sys.argv[1:])


node = Node(name=ARGS.name, address=ARGS.address,
            port=ARGS.port, production=10, consumption=5)

app = create_app(inbox=INBOX, token=ARGS.token, name=ARGS.name)

loop = asyncio.get_event_loop()
config = Config(app=app, loop=loop)
server = Server(config)
task_manager = TaskManager()

if __name__ == "__main__":
    print(f'Grid:   Starting Grid')
    print(f'GRID:   pid {os.getpid()}: send SIGINT or SIGTERM to exit.')

    server_task = loop.create_task(server.serve())
    message_task = loop.create_task(
        task_manager.process_messages(INBOX, node))

    tasks = [server_task, message_task]

    for sig in HANDLED_SIGNALS:
        loop.add_signal_handler(sig, handle_exit, server, task_manager)

    loop.run_until_complete(
        asyncio.gather(
            server_task,
            message_task,
            loop=loop
        ))

    print(f'GRID:   Successfully exited Grid')

    # TODO: setup logging
    # create logging branch
    # https://docs.python.org/3/library/logging.html
