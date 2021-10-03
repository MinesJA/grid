import asyncio
import signal
import aiohttp

from grid.models.node import Node
from grid.models.mailRoom import MailRoom
from grid.services import InboundJob, OutboundJob, Server, Scheduler

# TODO: setup logging
# create logging branch
# https://docs.python.org/3/library/logging.html

"""
Message System
==============

Server (Producer)
    - Ensures Envelopes/Messages are deserialized
    - Routes deserialized messages to Messaging resource
    - Messaging Resource drops envelops in asyncio.Inbox

InboundJob (Consumer)
    - Picks Envelopes from inbox.
    - Routes Envelopes to proper executor...




Producer (Server):
    - Receives http requests.
    - Converts requests to Envelope with Message.
    - Places Envelope in Inbox asyncio.Queue.

Consumer (InboundJob):
    
    

    - If there is a result Envelope

    TODO: Rethink whose job it is to put outgoing
        messages in Outbox queue.
        Maybe Message/Mailroom/Node should just be
        responsible for producing a message and
        give that back to InboundJob which puts it in
        Outbox queue.

    Mailroom puts result of processing in Outbox
        asyncio.Queue as Envelope with Message

    - OutboundJob
    Pulls from Outbox queue.
    Serializes and sends out Envelopes w/ Message
    as http requests
"""


def replace_with_callable():
    # TODO: Implement scheduler callable
    pass


def start_application(args):
    INBOX = asyncio.Queue()
    OUTBOX = asyncio.Queue()
    SESSION = aiohttp.ClientSession()
    Executor

    mailroom = MailRoom(outbox=OUTBOX)
    node = Node(name=args.name,
                id=args.id,
                host=args.host,
                port=args.port)

    print(f'Grid:   Starting Grid')
    print(f'Grid:   Created Node: {node.id}')

    loop = asyncio.get_event_loop()

    # TODO: Should these be called jobs?
    services = [
        InboundJob(INBOX, mailroom, node),
        OutboundJob(OUTBOX, SESSION),
        Server(INBOX, loop, args.host, args.port),
        Scheduler(replace_with_callable, 5)
    ]

    tasks = [loop.create_task(start()) for start in services]

    def handle_exit(*services):
        for service in services:
            service.exit()

    for sig in {signal.SIGINT, signal.SIGTERM}:
        loop.add_signal_handler(sig, handle_exit, *services)

    loop.run_until_complete(
        asyncio.gather(*tasks, loop=loop)
    )

    print(f'GRID:   Successfully exited Grid')
