from grid.models.actor import Actor
from grid.messages import *
from grid.envelopes import *
from grid.utils.strFormatter import *
from termcolor import colored
from typing import Tuple


class Node(Actor):

    def __init__(self,
                 name: str,
                 id: int,
                 host: str,
                 port: str,
                 production: int,
                 consumption: int):
        """Builds a Node object. Net describes the net energy
        output of the entire grid. If no siblings, then net
        is simply the net output of the invididual node.

        Args:
            name (str): [description]
            id (int): [description]
            host (str): http address of the node (ex. '123.123.123')
            port (str): port of the node (ex. '8080')
            production (int): [description]
            consumption (int): [description]
        """

        super().__init__(id, f'{host}:{port}', name)
        self.siblings = {}

        self._production = production
        self._consumption = consumption
        self._gridnet = production - consumption

    @property
    def gridnet(self):
        return self._gridnet

    @property
    def net(self):
        return self._production - self._consumption

    @property
    def production(self):
        return self._consumption

    @production.setter
    def production(self, production):
        self._production = production

    @property
    def consumption(self):
        return self._consumption

    @consumption.setter
    def consumption(self, consumption):
        self._consumption = consumption

    def update_gridnet(self, gridnet):
        print('GRID:    ', colored(f'Updating Grid Net: {gridnet}', 'magenta'))
        print('GRID:    ', self)
        self._gridnet = gridnet

    def add_sibling(self, sibling):
        print('GRID:    ', colored(f'Updating Siblings: {sibling}', 'magenta'))
        print('GRID:    ', self)
        # TODO: Should have a check in case siblings already added?
        self.siblings.update({sibling.id: sibling})

    def update_energy(self, energy: Tuple):
        print('GRID:    ', colored(f'Updating energy: {energy}', 'magenta'))
        print('GRID:    ', self)

        # TODO: Really hate this....refactor
        self.production = energy[0]
        self.consumption = energy[1]

    def __repr__(self):
        siblings = [sib.name for sib in self.siblings.values()]

        attrs = format_attrs(energy=(self._production, -self._consumption),
                             siblings=siblings,
                             gridnet=self.gridnet)

        return f'{super(Node, self).__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()
