import asyncio


class MessageService():

    def __init__(self):
        self.stop_incoming = True
        self.stop_outgoing = True

    async def process_incoming(self, inbox, node):
        self.stop_incoming = False

        while not self.stop_incoming:
            await asyncio.sleep(2)
            print(f'GRID:    Inbox {node}')
            if not inbox.empty():
                envelope = await inbox.get()
                await node.on_receive(envelope)
                inbox.task_done()

        await inbox.join()

    async def process_outgoing(self, outbox, session):
        self.stop_outgoing = False

        while not self.stop_outgoing:
            await asyncio.sleep(2)
            print(f'GRID:    Outbox')
            if not outbox.empty():
                env = await outbox.get()
                url = env.format_url()
                data = env.serialize()
                async with session.get(url, json=data) as response:
                    print("Status:", response.status)

    def exit(self):
        self.stop_incoming = True
        self.stop_outgoing = True
