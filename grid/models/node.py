import uuid
import enum
import requests
import time


class Node():

    def __init__(self, id: uuid, address: str, port: str):
        self.id = id
        self.address = address
        self.port = port
        self.siblings = {}
        self.messages = {}
        self.production = 10
        self.consumption = 5
        # Todo: Don't like this, revisit
        self.net = self.production+self.consumption

    def add_sibling(self, node):
        """Adds a sibling node to the siblings dict. Then sends a message to 
        that node with it's own node info so that the relationship is
        reciprocal. All nodes siblings should be aware of each other.

        Args:
            node (Node): node sibling instance
        """
        self.siblings.update({node.id: node})
        data = {
            'nodes': [{'id': str(self.id), 'address': self.address, 'port': self.port}]
        }
        requests.put(node._format_url('nodes'), data=data)

    def update_siblings(self):
        now = time.time()
        data = {
            'msgId': hash((now, self.uuid)),
            'net': self.net
        }
        for id, node in self.siblings.items():
            requests.put(node._format_url('power'), data=data)

    def adj_production(self, adjustment):
        self.production += adjustment
        self.net += adjustment

    def adj_consumption(self, adjustment):
        self.consumption += adjustment
        self.net -= adjustment

    def adj_net(self, adjustment):
        self.net += adjustment

    def forward_message(self, msg):
        for node in self.siblings:
            requests.put(node._format_url('power'), data=msg)

    def _format_url(self, route: str):
        return f'http://{self.address}:{self.port}/{route}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)
