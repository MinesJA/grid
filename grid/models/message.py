import uuid
from uuid import uuid1, UUID
from grid.models.nodeProxy import NodeProxy

# TODO:
# def generate_primary_message
# Should we develop some concept of creating
# primary messages and secondary messages?
__all__ = ['UpdateNet',
           'AddSibling',
           'UpdateEnergy']


class Message:
    def __init__(self, id: UUID):
        """Base class for Message objects.

        Args:
            id (uuid1): original id of message
        """
        self.id = id

    @classmethod
    def deserialize(clss, msg_dict: dict):
        """To be implement by child message class

        Args:
            clss ([type]): [description]
            msg_dict ([type]): [description]
        """
        pass

    def serialize(self):
        """To be implmented by child message class"""
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __repr__(self):
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k, v in self.__dict__.items()]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'


class UpdateNet(Message):

    def __init__(self,
                 id: UUID,
                 ,
                 nets: dict = {}):
        """Message requesting an updated Net value.

        Args:
            id (uuid1): Id of UpdateNet message
            nets (dict): Collection of Net values from each node
        """
        super().__init__(id)
        self.nets = nets

    @classmethod
    def deserialize(clss, msg_dict: dict):
        # TODO: Refactor this...
        id = UUID(msg_dict.get('id'))
        nets = msg_dict.get('nets', {})
        return clss(id, nets)

    def serialize(self):
        return {'id': self.id,
                'nets': self.nets}


class AddSibling(Message):

    def __init__(self,
                 id: UUID,
                 sibling_id: UUID,
                 sibling_name: str,
                 sibling_address: str):
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
    def with_self(clss, node):
        # TODO: This may fit into the concept of
        # a primary message creation
        return clss(
            id=uuid1(),
            sibling_id=node.id,
            sibling_name=node.name,
            sibling_address=node.address)

    @classmethod
    def deserialize(clss, msg_dict):

        # TODO: Refactor this...
        id = uuid.UUID(msg_dict.get('id'))
        sibling_id = msg_dict.get('siblingId')
        sibling_name = msg_dict.get('siblingName')
        sibling_address = msg_dict.get('siblingAddress')

        return clss(id,
                    sibling_id,
                    sibling_name,
                    sibling_address)

    def serialize(self):
        return {
            'id': self.id,
            'sibling_id': self.sibling_id,
            'sibling_name': self.sibling_name,
            'sibling_address': self.sibling_address
        }


class UpdateEnergy(Message):

    def __init__(self,
                 id: UUID,
                 production: int = None,
                 consumption: int = None):
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
    def deserialize(clss, msg_dict):
        id = uuid.UUID(msg_dict.get('id'))
        production = msg_dict.get('production')
        consumption = msg_dict.get('consumption')

        return clss(id,
                    production,
                    consumption)

    def serialize(self):
        return {
            'id': self.id,
            'production': self.production,
            'consumption': self.consumption,
        }
