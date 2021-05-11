from uuid import uuid1, UUID
from grid.utils.strFormatter import *
from grid.models.actor import Actor
from grid.models.envelope import *
from grid.models.message import *


class NodeProxy(Actor):

    def __init__(self, id: UUID, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address

    def get_ask(self, return_id, msg):
        return Ask(to=self.address,
                   msg=msg,
                   return_id=return_id,
                   reqid=uuid1())

        # reqid = uuid1()
        #     ask_env = Ask(to=sibling.address,
        #                   msg=AddSibling.with_self(self),
        #                   return_id=self.id,
        #                   reqid=reqid)
