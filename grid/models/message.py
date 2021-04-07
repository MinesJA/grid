from uuid import uuid1

TYPE = 'type'
SIBLING = 'sibling'
REQUIRES_RESPONSE = 'requires_response'
SENDER = 'sender'


def deserialize(type, message):
    """Creates a Message object from a type
    and message dict. Uses factory pattern.

        https://realpython.com/factory-method-python/

    Args:
        type (str): type of message
        message (dict): dict of info

    Returns:
        Message: Message based type
    """
    deserializer = get_deserializer(type)
    return deserializer(message)


def get_deserializer(type):
    if type == 'addsibling':
        return _deserialize_to_addsibling
    elif type == 'updatenet':
        return _deserialize_to_updatenet
    else:
        raise ValueError(type)


def _deserialize_to_addsibling(message):
    return AddSibling(sibling=message.get('sibling'), requires_response=message.get('requires_response'))


def _deserialize_to_updatenet(message):
    return UpdateNet(sender=message.get('sender'))


class Message:
    def __init__(self, id):
        """Base class for Message objects.

        Args:
            id (uuid1): [description]
        """
        self.id = id

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)


class UpdateNet(Message):

    def __init__(self, sender):
        """[summary]

        Args:
            sender ([type]): [description]
        """
        super().__init__(uuid1())
        self.sender = sender

    def serialize(self):
        return {
            'id': self.image_id,
            'image': self.uri,
            'modified': falcon.dt_to_http(self.modified),
            'size': self.size,
        }

    def __str__(self):
        return f'<UpdateNet sender={self.sender}'


class AddSibling(Message):

    def __init__(self, sibling, requires_response):
        """AddSibling message to initiate an Add Sibling action.
        Inlcudes the sibling to be added as well as an indicator
        of whether it requires a response as well.

        Args:
            sibling ([type]): [description]
            requires_response (bool, optional): [description]. Defaults to False.
        """
        super().__init__(uuid1())
        self.sibling = sibling
        self.requires_response = requires_response if requires_response else True

    def serialize(self):
        return {
            'id': self.image_id,
            'image': self.uri,
            'modified': falcon.dt_to_http(self.modified),
            'size': self.size,
        }

    def __str__(self):
        return f'<AddSibling sibling={self.sibling}'


class Forward(Message):

    def __init__(self, sender, msg):
        """[summary]

        Args:
            sender ([type]): [description]
            msg ([type]): [description]
        """
        super().__init__(uuid1())
        self.sender = sender
        self.msg = msg

    def serialize(self):
        return {
            'id': self.id,
            'sender': self.sender,
            'modified': falcon.dt_to_http(self.modified),
            'size': self.size,
        }

    def __str__(self):
        return f'<AddSibling sender={self.sender} sibling={self.sibling}'


class Response(Message):

    def __init__(self, sender, data):
        """[summary]

        Args:
            sender ([type]): [description]
            data ([type]): [description]
        """
        super().__init__(uuid1())
        self.sender = sender
        self.data = data

    def __str__(self):
        return f'<AddSibling sender={self.sender} sibling={self.sibling}'
