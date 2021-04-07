from asyncio import Queue


class TaskManager(object):

    def __init__(self):
        self.queue = Queue()

    def add_task(self, task):
        self.queue.put(task)

    def start_processing(self):
        while not self.queue.empty():
            task = self.queue.get()
            print(task)
            task.execute()


    async def process_messages(self):
        while self.running:
            msg = await self.inbox.get()
            await self.on_receive(msg)
            self.inbox.task_done()
