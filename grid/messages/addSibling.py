from uuid import uuid1, UUID
from grid.utils.valueGetters import *
from grid.messages import Message


class AddSibling(Message):

    def __init__(self,
                 sibling_id: int,
                 sibling_name: str,
                 sibling_address: str,
                 id: UUID = None):
        """Add a sibling message

        Args:
            id (UUID): Id of message
            sibling_id (UUID): id of sibling to add
            sibling_name (str): name of sibling to add
            sibling_address (str): address of sibling to add
        """
        super().__init__(id)
        self.sibling_id = sibling_id
        self.sibling_name = sibling_name
        self.sibling_address = sibling_address

    @classmethod
    def with_node(clss, node):
        # TODO: This may fit into the concept of
        # a primary message creation
        return clss(
            id=uuid1(),
            sibling_id=node.id,
            sibling_name=node.name,
            sibling_address=node.address)

    @classmethod
    def deserialize(clss, data):
        id = getuuid(data, 'id')
        sib_id = getint(data, 'siblingId')
        sib_name = getstr(data, 'siblingName')
        sib_address = getstr(data, 'siblingAddress')

        return clss(sib_id, sib_name, sib_address, id)

    def serialize(self):
        return {
            'id': str(self.id),
            'siblingId': str(self.sibling_id),
            'siblingName': self.sibling_name,
            'siblingAddress': self.sibling_address
        }
