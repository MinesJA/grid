from uvicorn import Config
import sys
import asyncio
import os
from asyncio import Queue
import threading
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
    - process_messages(inbox, node)
    Looks for messages to process in Queue
    and calls node.on_receive with message
    when one comes up
"""

HANDLED_SIGNALS = (
    signal.SIGINT,  # Unix signal 2. Sent by Ctrl+C.
    signal.SIGTERM,  # Unix signal 15. Sent by `kill <pid>`.
)


def create_app(inbox, token, id):
    app = falcon.asgi.App(middleware=AuthMiddleware(token, id))

    messaging = Messaging(inbox=inbox)
    # nodes = Nodes(inbox)

    app.add_route('/ask/{type}', messaging, suffix='ask')
    app.add_route('/tell/{type}', messaging, suffix='tell')

    # app.add_route('/nodes/siblings', nodes, suffix='siblings')
    # app.add_route('/nodes/energy', nodes, suffix='energy')
    return app


def parse_args(args):
    return create_parser().parse_args(args)


def create_parser():
    parser = argparse.ArgumentParser(description='Start a node')
    parser.add_argument('--id', '-i')
    parser.add_argument('--token', '-t')
    parser.add_argument('--address', '-a')
    parser.add_argument('--port', '-p', type=int)
    return parser


def handle_exit(server, task_manager):
    server.exit()
    task_manager.exit()


INBOX = Queue()
APP_PATH = 'grid.app:app'
ARGS = parse_args(sys.argv[1:])


node = Node(id=ARGS.id, address=ARGS.address,
            port=ARGS.port, production=10, consumption=5)

app = create_app(inbox=INBOX, token=ARGS.token, id=ARGS.id)

loop = asyncio.get_event_loop()
config = Config(app=app, loop=loop)
server = Server(config)
task_manager = TaskManager()

if __name__ == "__main__":
    print("Event loop running for 1 hour, press Ctrl+C to interrupt.")
    print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

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
    print("Completed")
    print("Completed out of with ")

# uvicorn.run(APP_PATH, host=ARGS.address, port=args.port, log_level="info")
