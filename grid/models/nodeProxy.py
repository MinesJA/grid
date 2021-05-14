from uuid import UUID
from grid.utils.strFormatter import *
from grid.models.actor import Actor


class NodeProxy(Actor):

    def __init__(self, id: UUID, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address
