from uuid import uuid1
import datetime
from grid.models.nodeProxy import NodeProxy

TYPE = 'type'
SIBLING = 'sibling'
REQUIRES_RESPONSE = 'requires_response'
SENDER = 'sender'


class Message:
    def __init__(self, id, timestamp, requires_auth):
        """Base class for Message objects.

        Args:
            id (uuid1): [description]
        """
        self.id = id
        self.timestamp = timestamp
        self.requires_auth = requires_auth

    @staticmethod
    def deserialize(message):
        """To be implmented by child message class

        TODO: Figure out what exactly the Falcon media
        obj is

        TODO: Update to this:
        https://stackabuse.com/pythons-classmethod-and-staticmethod-explained/

        Args:
            message (media_obj): Falcon media object
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

    def __init__(self, nets: dict = {}):
        """Message requesting an updated Net value.

        Args:
            nets (dict): Collection of Net values from each node
        """
        super().__init__(uuid1(), False)
        self.nets = nets

    @classmethod
    def deserialize(clss, msg):
        # TODO: should be a classmethod prob
        return clss(id=msg.get('id'), nets=msg.get('nets'))

    def serialize(self):
        return {}


class AddSibling(Message):

    def __init__(self, id: uuid1,
                 timestamp: datetime,
                 sibling: NodeProxy):
        """AddSibling message to initiate an Add Sibling action.

        Args:
            id (uuid1): Message Id
            sibling ([type]): [description]

        """
        super().__init__(id, timestamp, False)
        self.sibling = sibling

    @classmethod
    def add_self(clss, node):
        return clss(
            id=uuid1(),
            timestamp=datetime(),
            sibling_id=node.id,
            sibling_name=node.name,
            sibling_address=node.address)

    @classmethod
    def deserialize(clss, message):
        """
            {
                id: [msg_uuid],
                timestamp: [msg_timestamp],
                sibling_id: [sender id to add as sibling],
                sibling_address: [sender address to add as sibling]
            }
        TODO: Look up media get methods from Falcon
        Args:
            message (dict): JSON dictionary

        Returns:
            [type]: [description]
        """
        sibling = NodeProxy(id=message.get('sibling_id'),
                            name=message.get('sibling_name'),
                            address=message.get('sibling_address'))
        return clss(message.get('id'), message.get('timestamp'), sibling)

    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'sibling_id': self.sibling.id,
            'sibling_name': self.sibling.name,
            'sibling_address': self.sibling.address
        }


class UpdateEnergy(Message):

    def __init__(self, id: uuid1,
                 production: int = None,
                 consumption: int = None):
        """UpdateEnergy message update either production
        consumption, or both.

        Args:
            production (int): new production value
            consumption (int): new consumption value
        """
        super().__init__(id, True)
        self.production = production
        self.consumption = consumption

    @staticmethod
    def deserialize(message):
        return UpdateEnergy(id=uuid1(), production=message.get('production'),
                            consumption=message.get('consumption'))

    def serialize(self):
        {'type': 'updateenergy',
         'id': str(self.id),
         'production': self.production,
         'consumption': self.consumption
         }


# TODO: Revisit, may not need these
class Forward(Message):

    def __init__(self, id: uuid1, sender: str, msg: Message):
        """[summary]

        Args:
            sender ([type]): [description]
            msg ([type]): [description]
        """
        super().__init__(id, False)
        self.sender = sender
        self.msg = msg

    def serialize(self):
        return {}

    def serialize(self):
        pass

# TODO: Revisit, may not need these


class Response(Message):

    def __init__(self, id: uuid1, sender: str, data: str):
        """

        TODO: think through how data response should be
        wrapped

        Args:
            sender ([type]): [description]
            data ([type]): [description]
        """
        super().__init__(id, False)
        self.sender = sender
        self.data = data

    def serialize(self):
        pass
