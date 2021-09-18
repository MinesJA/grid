import asyncio
from termcolor import colored
from grid.commands import commands


class MessageService():

    def __init__(self):
        self.stop_incoming = True
        self.stop_outgoing = True

    async def process_incoming(self, inbox, node, mailroom):

        self.stop_incoming = False
        print('GRID:    ', node)

        while not self.stop_incoming:
            await asyncio.sleep(1)
            if not inbox.empty():
                env = await inbox.get()
                print('GRID:    ', colored(f'RECEIVING: {env}', 'blue'))
                # TODO: Already deserialized Envelope and Message, so should
                #   probably just have commands deserialized?
                # TODO: Why are Messages different from commands in the first
                #   place? They should probably be the same thing. or at
                #   the very least, a message should include a Task.
                execute = commands.get(env.msg.gettype())
                await execute(mailroom, node, env)

                inbox.task_done()
            # print(node)

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
                    print(response)

    def exit(self):
        self.stop_incoming = True
        self.stop_outgoing = True
