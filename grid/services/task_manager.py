import asyncio


class TaskManager():

    def __init__(self):
        self.stop = True

    async def process_messages(self, inbox, node):
        self.stop = False

        while not self.stop:
            print("Processing messages")
            if not inbox.empty():
                msg = await inbox.get()
                await node.on_receive(msg)
                inbox.task_done()
            else:
                await asyncio.sleep(2)
        await inbox.join()

    def exit(self):
        self.stop = True
