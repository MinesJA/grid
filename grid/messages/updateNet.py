from uuid import UUID
from grid.utils.valueGetters import *
from grid.messages import Message


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

    def reduce(self, responses, node=None):
        # TODO: need to find way to standarize serialization
        # of id.
        curr = {str(node.id): node.net} if node else {}
        for resp in responses.values():
            curr.update(resp.msg.nets)

        return UpdateNet(nets=curr)

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        nets = data.get('nets')
        return clss(nets, id)

    def serialize(self):
        return {'id': str(self.id),
                'nets': self.nets}
