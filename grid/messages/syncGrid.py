from uuid import UUID
from grid.utils.valueGetters import *
from grid.messages import Message


class SyncGrid(Message):

    def __init__(self, id: UUID = None):
        super().__init__(id)

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        return clss(id)

    def serialize(self):
        return {'id': str(self.id)}
