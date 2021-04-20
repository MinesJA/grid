from asyncio import Queue
from grid.models.message import Envelope


class Actor:

    def __init__(self, id, address):
        self.id = id
        self.address = address
        self.inbox = Queue(maxsize=100)
        self.running = False

    async def start(self):
        self.running = True
        await self.process_messages()

    def stop(self):
        self.running = False

    def is_stopped(self):
        not self.running

    async def tell(self, message):
        await self.inbox.put(Envelope(message))

    async def ask(self, message, reply_to):
        await self.inbox.put(Envelope(message, reply_to))

    def on_receive(self, message):
        # To be implemented by child class
        pass
