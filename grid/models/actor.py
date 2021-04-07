from grid.models.envelope import Envelope
from queue import Queue


class Actor:

    def __init__(self, id, task_manager):
        self.id = id
        self.task_manager = task_manager
        self.running = False

    async def start(self):
        self.running = True
        await self.process_messages()

    def stop(self):
        self.running = False
    
    def is_stopped(self):
        not self.running

    async def tell(self, message):
        await self.inbox.put(message)

    async def ask(self, message):
        # Create a future here

        # try:
        #     if not self.is_alive():
        #         raise ActorDeadError(f"{self} not found")
        # except ActorDeadError:
        #     future.set_exception()
        # else:
        #     self.actor_inbox.put(Envelope(message, reply_to=future))

        # if block:
        #     return future.get(timeout=timeout)
        # else:
        #     return future
        #   return self.on_receive(message)
        pass

    def on_receive(self, message):
        # To be implemented by child class
        pass

    async def process_messages(self):
        while self.running:
            msg = await self.inbox.get()
            await self.on_receive(msg)
            self.inbox.task_done()
