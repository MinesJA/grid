import sys
import asyncio
import signal
import aiohttp
from dotenv import load_dotenv
from grid.models.node import Node
from grid.models.mailRoom import MailRoom
from grid.services import InboundJob, OutboundJob, Server, Scheduler
from grid.cli import parse_args

# TODO: setup logging
# create logging branch
# https://docs.python.org/3/library/logging.html

"""
Message System
==============
Producer:
    - Server
    Receives http requests.
    Converts requests to Envelope with Message.
    Places Envelope in Inbox asyncio.Queue.

Consumer:
    - InboundJob
    Consumes messages from inbox.
    Calls execute method on Envelope which trigger
    specific execution logic on message.
    TODO: Rethink whos job it is to put outgoing
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

load_dotenv()

INBOX = asyncio.Queue()
OUTBOX = asyncio.Queue()
SESSION = aiohttp.ClientSession()


def replace_with_callable():
    # TODO: Implement scheduler callable
    pass


# TODO: Rethink this. Right now, parse args runs and then
#   assumption is server starts. Python app should run arg
#   parse, which should determine what to do (start server,
#   other stuff, etc.)
args = parse_args(sys.arv[1:])

node = Node(name=args.name,
            id=args.id,
            host=args.host,
            port=args.port)

mailroom = MailRoom(outbox=OUTBOX)

loop = asyncio.get_event_loop()

if __name__ == "__main__":
    print(f'Grid:   Starting Grid')
    print(f'Grid:   Created Node: {node.id}')

    # TODO: Figure out where all these setup should live...
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
        asyncio.gather(*services, loop=loop)
    )

    print(f'GRID:   Successfully exited Grid')
