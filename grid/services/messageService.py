import asyncio


class MessageService():

    def __init__(self):
        self.stop_incoming = True
        self.stop_outgoing = True

    async def process_incoming(self, inbox, node):
        self.stop_incoming = False

        while not self.stop_incoming:
            await asyncio.sleep(2)
            print(f'GRID:    {node}')
            if not inbox.empty():
                envelope = await inbox.get()
                await node.on_receive(envelope)
                inbox.task_done()

        await inbox.join()

    # TODO: Finish this
    async def process_outgoing(self, outbox):
        self.stop_outging = False

        while not self.stop_outoing:
            await asyncio.sleep(2)
            if not outbox.empty():
                pass

    def exit(self):
        self.stop = True
