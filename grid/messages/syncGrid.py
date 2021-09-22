from uuid import UUID
from grid.utils.valueGetters import getuuid
from grid.messages import Message, UpdateNet
from grid.envelopes import Tell


class SyncGrid(Message):

    def __init__(self, id: UUID = None):
        super().__init__(id)

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        return clss(id)

    def serialize(self):
        return {'id': str(self.id)}

    async def from_tell(self, node, mailroom, env):
        # TODO: Verify that package get's closed in mailroom
        if isinstance(env, Tell):
            if not mailroom.is_registered(env):
                siblings = node.siblings.values()
                await mailroom.ask(msg=UpdateNet(),
                                   sender=node,
                                   recipients=siblings)

                await mailroom.forward_tell(env, node)
