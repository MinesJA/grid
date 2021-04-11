from uuid import uuid1

TYPE = 'type'
SIBLING = 'sibling'
REQUIRES_RESPONSE = 'requires_response'
SENDER = 'sender'


# TODO:
"""How I'm thinking about auth:
    Only a Node's IoT devices should be able to update
    it's own energy. That would constitute one type of auth.
    However, there should prob be another type of check for other
    messages. For example, receiving an UpdateNet message should prob
    only be able to come from sibling nodes? Whereas AddSibling
    should be able to come from any Node.

    For now, we'll use Auth to mean Authorized as an IoT belonging
    to the Node (think solar panel readings, smart meter, etc.)
"""


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
    if type == 'updateenergy':
        return _deserialize_to_updateenergy
    elif type == 'addsibling':
        return _deserialize_to_addsibling
    elif type == 'updatenet':
        return _deserialize_to_updatenet
    else:
        raise ValueError(type)


def _deserialize_to_updateenergy(message):
    return UpdateEnergy(id=uuid1(), production=message.get('production'),
                        consumption=message.get('consumption'))


def _deserialize_to_addsibling(message):
    return AddSibling(id=uuid1(), sibling=message.get('sibling'),
                      requires_response=message.get('requires_response'))


def _deserialize_to_updatenet(message):
    return UpdateNet(id=uuid1(), sender=message.get('sender'))


class Message:
    def __init__(self, id, requires_auth):
        """Base class for Message objects.

        Args:
            id (uuid1): [description]
        """
        self.id = id
        self.requires_auth = requires_auth

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

    def __init__(self, id: uuid1, sender: str):
        """[summary]

        Args:
            sender ([type]): [description]
        """
        super().__init__(id, False)
        self.sender = sender

    def serialize(self):
        return {
            'id': self.id,
            'image': self.uri,
            'modified': falcon.dt_to_http(self.modified),
            'size': self.size,
        }

    def __str__(self):
        return f'<UpdateNet sender={self.sender}'


class AddSibling(Message):

    def __init__(self, id: uuid1, sender: str, sibling: str, respond: bool):
        """AddSibling message to initiate an Add Sibling action.
        Inlcudes the sibling to be added as well as an indicator
        of whether it requires a reciprocal call to add sibling.

        Reciprocal call is only to ensure

        Args:
            sibling ([type]): [description]
            respond (bool, optional): should respond. Defaults to False.
        """
        super().__init__(id, False)
        self.sender = sender
        self.sibling = sibling
        self.respond = respond if respond else True

    def serialize(self):
        return {
            'sender': self.sender,
            'sibling': self.sibling,
            'respond': self.respond,
        }


class UpdateEnergy(Message):

    def __init__(self, id: uuid1,
                 production: int = None, consumption: int = None):
        """UpdateEnergy message update either production
        consumption, or both.

        Args:
            production (int): new production value
            consumption (int): new consumption value
        """
        super().__init__(id, True)
        self.production = production
        self.consumption = consumption

    def serialize(self):
        {'type': 'updateenergy',
         'id': str(self.id),
         'production': self.production,
         'consumption': self.consumption
         }


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
        return {
            'id': self.id,
            'sender': self.sender,
            'modified': falcon.dt_to_http(self.modified),
            'size': self.size,
        }

    def serialize(self):
        pass


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
