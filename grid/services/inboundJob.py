import asyncio
from termcolor import colored
from grid.models.mailRoom import MessageRegisteredException


class InboundJob:

    def __init__(self, inbox, mailroom, node):
        self.inbox = inbox
        self.mailroom = mailroom
        self.node = node
        self.stop = True

    async def __call__(self):
        self.stop = False
        print('GRID:    ', self.node)

        while not self.stop:
            await asyncio.sleep(1)
            if not self.inbox.empty():
                env = await self.inbox.get()
                print('GRID:    ', colored(f'CONSUMING: {env}', 'blue'))
                try:
                    self.mailroom.register_inbound(env)
                    await self.node.onReceive(env)
                except (MessageRegisteredException):
                    # Generate empty Response and send back
                    pass

                finally:
                    self.inbox.task_done()

                # TODO: Implement error handling here....not sure
                #   what the default error handling should be tho
                # await env.execute(self.mailroom, self.node)

        await self.inbox.join()
  
    def exit(self):
        self.stop = True
