import uuid
from uuid import uuid1, UUID
from grid.utils.valueGetters import *

# TODO:
# def generate_primary_message
# Should we develop some concept of creating
# primary messages and secondary messages?
__all__ = ['Message',
           'UpdateNet',
           'AddSibling',
           'UpdateEnergy',
           'SyncGrid']


class Message:
    def __init__(self, id: UUID = None):
        """Base class for Message objects.

        Args:
            id (uuid1): original id of message
        """
        self.id = id if id else uuid1()

    def get_type(self):
        return self.__class__.__name__

    @classmethod
    def deserialize(clss, data: dict):
        """To be implement by child message class
        """
        raise NotImplemented()

    def serialize(self):
        """To be implmented by child message class"""
        raise NotImplemented()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __repr__(self):
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k,
                     v in self.__dict__.items() if not isinstance(v, UUID)]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'


class SyncGrid(Message):

    def __init__(self, id: UUID = None):
        super().__init__(id)

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        return clss(id)

    def serialize(self):
        return {'id': str(self.id)}


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


class UpdateEnergy(Message):

    def __init__(self,
                 production: int = None,
                 consumption: int = None,
                 id: UUID = None):
        """UpdateEnergy message update either production
        consumption, or both.

        Args:
            production (int): new production value
            consumption (int): new consumption value
        """
        super().__init__(id)
        self.production = production
        self.consumption = consumption

    @classmethod
    def deserialize(clss, data: dict):
        id = getuuid(data, 'id')
        pro = getint(data, 'production')
        con = getint(data, 'consumption')
        return clss(pro, con, id)

    def serialize(self):
        return {
            'id': str(self.id),
            'production': self.production,
            'consumption': self.consumption,
        }
