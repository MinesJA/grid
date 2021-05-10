import asyncio
from termcolor import colored


class MessageService():

    def __init__(self):
        self.stop_incoming = True
        self.stop_outgoing = True

    async def process_incoming(self, inbox, node):
        self.stop_incoming = False

        while not self.stop_incoming:
            await asyncio.sleep(2)
            if not inbox.empty():
                env = await inbox.get()
                print('GRID:    ', colored(f'RECEIVING: {env}', 'blue'))
                await node.on_receive(env)
                inbox.task_done()

            print('GRID:    ', colored('INBOX empty', 'blue'))
            print('GRID:    ', node)

        await inbox.join()

    async def process_outgoing(self, outbox, session):
        self.stop_outgoing = False

        while not self.stop_outgoing:
            await asyncio.sleep(2)

            if not outbox.empty():
                env = await outbox.get()
                url = f'http://{env.to}/messaging'
                print('GRID:    ', colored(f'SENDING: {env}', 'red'))
                data = env.serialize()
                async with session.get(url, json=data) as response:
                    pass

            print('GRID:    ', colored('OUTBOX empty', 'red'))

    def exit(self):
        self.stop_incoming = True
        self.stop_outgoing = True
