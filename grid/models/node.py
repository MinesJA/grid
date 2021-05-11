from asyncio import Queue
from time import time
from uuid import uuid1
from grid.models.actor import Actor
from grid.models.mailRoom import MailRoom
from grid.models.message import *
from grid.models.envelope import *
from grid.models.mailRoom import MailRoom
from grid.models.nodeProxy import NodeProxy
from grid.utils.strFormatter import *
from termcolor import colored


class Node(Actor):

    def __init__(self,
                 name: str,
                 id: int,
                 host: str,
                 port: str,
                 production: int,
                 consumption: int,
                 mailroom: MailRoom):
        """Builds a Node object. Net describes the net energy
        output of the entire grid. If no siblings, then net
        is simply the net output of the invididual node.

        Args:
            address (str): http address of the node (ex. '123.123.123')
            port (str): port of the node (ex. '8080')
        """
        super().__init__(id, f'{host}:{port}', name)
        self.siblings = {}

        self.production = production
        self.consumption = consumption

        self._gridnet = production - consumption

        self.mailroom = mailroom

    @property
    def gridnet(self):
        return self._gridnet

    @gridnet.setter
    def gridnet(self, net):
        self._gridnet = net

    @property
    def net(self):
        return self.production - self.consumption

    async def on_receive(self, env):
        if isinstance(env.msg, UpdateEnergy):
            await self.update_energy(env)
        elif isinstance(env.msg, AddSibling):
            await self.add_sibling(env)
        elif isinstance(env.msg, UpdateNet):
            await self.update_net(env)
        elif isinstance(env.msg, SyncGrid):
            await self.sync_grid(env)
        else:
            self.print(
                f'{self.name}: Did not recognize message {env.msg}')

    async def add_sibling(self, env):
        """Adds a sibling NodeProxy to siblings. Then sends
        response message AddSibling with it's own info to maintain
        a bidirectional graph. Then sends a request to update
        the grids net output.

        Args:
            env (Envelope): envelope with add sibling details
        """
        sibling = NodeProxy(env.msg.sibling_id,
                            env.msg.sibling_name,
                            env.msg.sibling_address)

        if isinstance(env, Tell) and sibling.id not in self.siblings:
            await self.mailroom.ask(msg=AddSibling.with_node(self),
                                    sender=self,
                                    recipients=[sibling])

        elif isinstance(env, Ask) and sibling.id not in self.siblings:
            self.siblings.update({sibling.id: sibling})
            self.mailroom.respond(ask=env,
                                  recipient=sibling,
                                  msg=AddSibling.with_node(self))

            # TODO: Implement
            await self.sync_nodes()

        elif isinstance(env, Response) and sibling.id not in self.siblings:
            self.siblings.update({sibling.id: sibling})
            self.mailroom.close_req(resp=env)
            # TODO: Implement
            await self.sync_grid()

    async def update_net(self, env):
        """Update net by collecting net values
        of entire grid and summing them up.

        Args:
            env (Envelope): envelope
        """

        def reduce_msg(responses):
            curr = {self.id: self.net}

            for resp in responses.values():
                curr.update(resp.nets)

            return UpdateNet(nets=curr)

        await self.mailroom.forward_ask(env=env,
                                        msg_class=UpdateNet,
                                        reducer=reduce_msg,
                                        valhandler=self.gridnet,
                                        sender=self)

    async def update_energy(self, env):
        """Updates the energy production and/or
        consumption of Node

        Args:
            env ([type]): [description]
        """
        # TODO: Refactor to one liners
        if env.msg.consumption is not None:
            self.consumption = env.msg.consumption
        if env.msg.production is not None:
            self.production = env.msg.production

        await self.sync_nodes()

    async def sync_grid(self, env):

        await self.update_net(Tell(self.address, UpdateNet()))

        self.mailroom.forward_tell(env, SyncGrid, self)

    def __repr__(self):
        attrs = format_attrs(production=self.production,
                             consumption=self.consumption,
                             net=self.net,
                             gridnet=self.gridnet)
        # print('GRID:    ', colored(f'RECEIVING: {env}', 'blue'))
        return f'{super(Node, self).__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()


#  # result_handler(sum(self.net, env.msg.nets.values())

#                        # return UpdateNet(ask=package.og_ask, recipient=?????, msg=msg)

#                        # def package_msg()
#                        #     sum(sender.net, env.msg.nets.values())

#                        #     if isinstance(env, Tell):
#                        #     elif isinstance(env, Ask):
#                        #     elif isinstance(env, Response):

#                        #     # UpdateNet({sender.id: sender.net}

#                        # if should_forward
#                        # elif already_processed
#                        # elif dead_end

#                        # Forward_Ask:
#                        # if not visited and siblings:
#                        # 1. This request has not been forwarded before
#                        # 2. This is not a dead end
#                        # Forward message to all siblings
#                        msg = UpdateNet()

#                        # Already_Processed
#                        # elif visited:
#                        # 1. This message has already been processed by another node
#                        # Respond with a 0 value to prevent duplicate counting
#                        msg = UpdateNet({self.id: 0}))

#         # elif not siblings:
#         # 1. This is a dead end
#         # Begin retrieval process
#         msg=UpdateNet({self.id: self.net})

#         # if isinstance(env, Tell):
#         #     await self.mailroom.ask(msg=UpdateNet(),
#         #                             sender=self,
#         #                             recipients=self.siblings.values())

#         # elif isinstance(env, Ask):
#         #     siblings = [s for (i, s) in self.siblings.items()
#         #                 if i != env.return_id]

#         #     resp_to = self.siblings.get(env.return_id)
#         #     visited = self.mailroom.has_package(env.master_reqid)

#         #     if not visited and siblings:
#         #         # 1. This request has not been forwarded before
#         #         # 2. This is not a dead end
#         #         # Forward message to all siblings
#         #         await self.mailroom.forward_ask(og_ask=env,
#         #                                         sender=self,
#         #                                         msg=UpdateNet(),
#         #                                         recipients=siblings)
#         #     elif visited:
#         #         # 1. This message has already been processed by another node
#         #         # Respond with a 0 value to prevent duplicate counting
#         #         self.mailroom.respond(ask=env,
#         #                               recipient=resp_to,
#         #                               msg=UpdateNet({self.id: 0}))
#         #     elif not siblings:
#         #         # 1. This is a dead end
#         #         # Begin retrieval process
#         #         self.mailroom.respond(ask=env,
#         #                               recipient=resp_to,
#         #                               msg=UpdateNet({self.id: self.net}))
#         #     else:
#         #         raise ValueError(
#         #             f'{self.address}: Something bad happend in Ask UpdateNet')

#         # elif isinstance(env, Response):
#         #     self.mailroom.close_req(env)

#         #     is_compl = self.mailroom.package_ready(env.master_reqid)
#         #     msg_returned = self.mailroom.msg_returned(env.master_reqid, self)

#         #     if msg_returned:
#         #         # 1. The response has reached the start
#         #         # Close out request
#         #         self.gridnet = sum(self.net, env.msg.nets.values())

#         #     elif is_compl:
#         #         def combine(responses):
#         #             compiled_nets = {self.id: self.net}
#         #             for resp in responses:
#         #                 compiled_nets.update(resp.msg.nets)
#         #             return UpdateNet(compiled_nets)

#         #         self.mailroom.forward_resp(env, combine)
#         #     else:
#         #         raise ValueError(f'{self.address}: Something has gone \
#         #         wrong in Response handling')
