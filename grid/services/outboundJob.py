import asyncio
from termcolor import colored
from grid.commands import commands


class OutboundJob:

    def __init__(self, outbox, session):
        self.outbox = outbox
        self.session = session
        self.stop = True

    async def __call__(self):
        self.stop_outgoing = False

        while not self.stop_outgoing:
            await asyncio.sleep(1)

            if not self.outbox.empty():
                env = await self.outbox.get()
                url = f'http://{env.to}/messaging'
                print('GRID:    ', colored(f'SENDING: {env}', 'red'))
                data = env.serialize()

                async with self.session.get(url, json=data) as response:
                    print(response)

    def exit(self):
        self.stop = True
