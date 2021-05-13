
from uuid import UUID
from grid.utils.valueGetters import *
from grid.messages.message import Message


class UpdateNet(Message):

    def __init__(self,
                 nets: dict = {},
                 id: UUID = None):
        """Message requesting an updated Net value.

        Args:
            id (uuid1): Id of UpdateNet message
            nets (dict): Collection of Net values from each node
        """
        super().__init__(id)
        self.nets = nets

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        nets = data.get('nets')
        return clss(nets, id)

    def serialize(self):
        return {'id': str(self.id),
                'nets': self.nets}
