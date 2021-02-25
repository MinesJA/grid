import uuid
import enum
import requests
import time


class Node():

    def __init__(self, address: str = ""):
        self.id = uuid.uuid1()
        self.address = address
        self.siblings = []
        self.messages = {}
        self.production = 10
        self.consumption = 5
        self.net = self.production+self.consumption

    def add_siblings(self, nodes):
        self.siblings.extend(nodes)

    def adj_production(self, adjustment):
        self.production += adjustment
        self.net += adjustment

    def adj_consumption(self, adjustment):
        self.consumption += adjustment
        self.net -= adjustment

    def adj_net(self, adjustment):
        self.net += adjustment
    
    def forward_message(self, msg):
        for node in siblings:
            requests.put(node.address+'/power', data=msg)

    def update_siblings(self):
        now = time.time()
        data = {
            'msgId': hash((now, self.uuid)),
            'net': self.net
        }
        for node in siblings:
            requests.put(node.address+'/power', data=data)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)
