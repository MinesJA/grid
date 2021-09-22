from uuid import UUID
from grid.utils.strFormatter import *
# TODO: Need to check if preloading in __init__ and importing from there
#   is better practice
#   from grid.models import Actor
from grid.models.actor import Actor

# TODO: Do we need this? Seems like it's exactly same as Actor


class NodeProxy(Actor):

    def __init__(self, id: UUID, address: str, name: str):
        super().__init__(id, address, name)
