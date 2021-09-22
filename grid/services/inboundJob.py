import asyncio
from termcolor import colored


class InboundJob:

    def __init__(self, inbox, mailroom, node):
        self.inbox = inbox
        self.mailroom = mailroom
        self.node = node
        self.stop = True

    async def __call__(self):
        self.stop_incoming = False
        print('GRID:    ', self.node)

        while not self.stop_incoming:
            await asyncio.sleep(1)
            if not self.inbox.empty():
                env = await self.inbox.get()
                print('GRID:    ', colored(f'CONSUMING: {env}', 'blue'))

                # TODO: Implement error handling here....not sure
                #   what the default error handling should be tho
                await env.execute(self.mailroom, self.node)
                self.inbox.task_done()

        await self.inbox.join()

    def exit(self):
        self.stop = True
