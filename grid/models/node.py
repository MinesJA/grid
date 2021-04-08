from grid.models.actor import Actor
from grid.models.message import AddSibling, UpdateNet, Forward
import requests
import time


class NodeBuilder():

    _instance = None

    def __init__(self, id: str, address: str, port: str, production: int, consumption: int):
        self.id = id
        self.address = address
        self.port = port
        self.production = production
        self.consumption = consumption

    async def get(self):
        if self._instance is None:
            node = Node(self.id, self.address,
                        self.port, self.production, self.consumption)
            self._instance = await node.start()
        elif self._instance.is_stopped():
            await self._instance.start()
        return self._instance


class Node(Actor):

    def __init__(self, id: str, address: str, port: str,
                 production: int, consumption: int):
        """Builds a Node object. Net describes the net energy
        output of the entire grid. If no siblings, then net
        is simply the net output of the invididual node.

        Args:
            address (str): http address of the node (ex. '123.123.123')
            port (str): port of the node (ex. '8080')
        """
        super().__init__(id)
        self.address = address
        self.port = port
        self.full_address = f'{address}:{port}'
        self.siblings = {}
        self.production = production
        self.consumption = consumption

        self.net = production - consumption

    async def on_receive(self, message):
        if isinstance(message, AddSibling):
            await self.add_sibling(message.sibling)
        elif isinstance(message, UpdateNet):
            await self.update_net()
        elif isinstance(message, Forward):
            await self.forward(message)
        else:
            self.print(f'{self.id}: Did not recognize message')

    async def add_sibling(self, sibling):
        """Adds a sibling node to the siblings dict. Then sends an
        AddSibling message to the sibling node with it's own info to
        maintain a bidirectional graph. Then sends a request to update
        the grids net output.

        Args:
            sibling (Node): node sibling instance
        """
        if sibling.id not in self.siblings:
            self.print(f'{self.id}: Adding {sibling.id} as sibling')
            self.siblings[sibling.id] = sibling

            sibling.tell(AddSibling(self, False))

            sibling.tell(AddSibling(self.id, self))

        if sibling.id not in self.node.siblings:
            self.siblings.update({sibling.id: sibling})

            requests.put(sibling._format_url('siblings'),
                         data={'address': self.address, 'port': self.port})

            self.update_siblings()

    def update_siblings(self):
        now = time.time()
        data = {
            'msgId': hash((now, self.id)),
            'sender': self.id,
            'timeStamp': now,
            'net': self.net
        }
        for node in self.siblings.values():
            requests.put(node._format_url('net'), data=data)

    def update_energy(self, consumption, production):
        # TODO: Refactor to one liners
        if consumption:
            self.consumption = consumption
        if production:
            self.production = production

        self.net = self.production - self.consumption
        # TODO: Then shoud update siblings

    def get_energy(self):
        return {'production': self.production,
                'consumption': self.consumption,
                'net': self.net}

    def handle_net_sync_req(self, msg):
        if msg.id not in self.node.messages:
            self.node.messages[msg.id] = msg
            self.net = self._calculate_net(msg.net)

            self.forward_message(self.net, msg)
            return self.net

    def forward_message(self, msg):
        # abc = {"type":"insecure","id":"1","name":"peter"}

        black_list_values = set(('timeStamp'))

        xyz = {k: v for k, v in abc.iteritems() if k not in black_list_values}
        xyz["identity"] = abc["id"]

        for node in self.siblings:
            requests.put(node._format_url('power'), data=msg)

    def _generate_msg(self, timeStamp, latest_net):
        return {
            'msgId': hash((timeStamp, self.id)),
            'timeStamp': timeStamp,
            'sender': self.id,
            'net': latest_net
        }

    def _calculate_net(self, other_net):
        """Returns personal net added to incoming net.

        Args:
            other_net (int): net to be added to personal net
        """
        return self.productionduction + self.consumptionsumption + other_net

    def _format_url(self, route: str):
        return f'http://{self.address}:{self.port}/{route}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)
