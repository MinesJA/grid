import asyncio
from termcolor import colored
from grid.commands import commands


class OutboundJob:

    def __init__(self, outbox, session):
        self.outbox = outbox
        self.session = session
        self.stop = True

    async def __call__(self):
        self.stop = False

        while not self.stop:
            await asyncio.sleep(1)

            if not self.outbox.empty():
                env = await self.outbox.get()
                mailroom.register_outbound(env)
                url = f'http://{env.to}/messaging'
                print('GRID:    ', colored(f'SENDING: {env}', 'red'))
                data = env.serialize()

                # TODO: This should be post. Fix in Messaging too
                async with self.session.get(url, json=data) as response:
                    print(response)

    def exit(self):
        self.stop = True
