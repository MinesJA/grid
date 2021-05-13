from uuid import uuid1
from grid.models.actor import Actor
from grid.models.mailRoom import MailRoom
from grid.messages import *
from grid.envelopes import *
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
        self._siblings = {}

        self.production = production
        self.consumption = consumption
        self._gridnet = production - consumption

        self.mailroom = mailroom

    def update_gridnet(self, gridnet):
        print('GRID:    ', colored(f'Updating Grid Net: {gridnet}', 'purple'))
        self._gridnet = gridnet

    def update_siblings(self, sibling):
        print('GRID:    ', colored(f'Updating Siblings: {sibling}', 'purple'))
        # TODO: Should have a check in case siblings already added?
        # TODO: Need to ensure that every update of siblings also fires
        #   a corresponding update of the grid
        self._siblings.update({sibling.id: sibling})

    @property
    def net(self):
        return self.production - self.consumption
    
    async def update_energy(self):
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

        await self.sync_grid(Tell.from(self, SyncGrid()))
    





    async def on_receive(self, env):
        if isinstance(env.msg, UpdateEnergy):
            await self.handle_update_energy(env)
        elif isinstance(env.msg, AddSibling):
            await self.handle_add_sibling(env)
        elif isinstance(env.msg, UpdateNet):
            await self.handle_update_net(env)
        elif isinstance(env.msg, SyncGrid):
            await self.handle_sync_grid(env)
        else:
            self.print(
                f'{self.name}: Did not recognize message {env.msg}')

  

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
                                        msgbuilder=UpdateNet,
                                        reducer=reduce_msg,
                                        valhandler=self.gridnet,
                                        sender=self)

    

    async def sync_grid(self, env):
        await self.update_net(Tell.from(self, UpdateNet()))
        await self.mailroom.forward_tell(env)

    def __repr__(self):
        attrs = format_attrs(production=self.production,
                             consumption=self.consumption,
                             net=self.net,
                             siblings=self.siblings.keys(),
                             gridnet=self.gridnet)

        return f'{super(Node, self).__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()
