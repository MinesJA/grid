from uuid import uuid1
import datetime
from collections import namedtuple

TYPE = 'type'
SIBLING = 'sibling'
REQUIRES_RESPONSE = 'requires_response'
SENDER = 'sender'

Envelope = namedtuple(
    'Envelope', ['envelope_id', 'message', 'reply_to', 'response'])


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

    def __str__(self):
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k, v in self.__dict__.items()]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'


class UpdateNet(Message):

    def __init__(self, id: uuid1,
                 req_id: uuid1,
                 sender_id: uuid1,
                 nets: dict = {}):
        """Message requesting an updated Net value. Orig_sender
        represents the original sender of the message, no matter
        how far down the line the message gets passed. Orig_id
        represents the same concept but for the message id. Nets
        are the net values collected from each Node in the grid.

        Args:
            sender_id (uuid1): Id of Node that made original request
            nets (dict): Collection of Net values from each node
        """
        super().__init__(id, False)
        self.req_id = req_id
        self.sender_id = sender_id
        self.nets = nets

    @staticmethod
    def deserialize(message):
        # TODO: should be a classmethod prob
        return UpdateNet(id=uuid1(), orig_sender=message.get('orig_sender'))

    def serialize(self):
        return {}

    def __str__(self):
        return f'<UpdateNet sender={self.sender}'


class AddSibling(Message):

    def __init__(self, id: uuid1,
                 timestamp: datetime,
                 sibling_id: uuid1,
                 sibling_name: str,
                 sibling_address: str):
        """AddSibling message to initiate an Add Sibling action.

        Args:
            id (uuid1): Message Id
            sibling ([type]): [description]

        """
        super().__init__(id, timestamp, False)
        self.sibling_id = sibling_id
        self.sibling_name = sibling_name
        self.sibling_address = sibling_address

    @staticmethod
    def deserialize(message):
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
        return AddSibling(id=message.get('id'),
                          sibling_id=message.get('sibling_id'),
                          sibling=message.get('sibling'))

    def serialize(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'sibling_id': self.sibling_id,
            'sibling_name': self.sibling_name,
            'sibling_address': self.sibling_address
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
