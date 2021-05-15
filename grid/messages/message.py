from uuid import uuid1, UUID
from grid.utils.valueGetters import *


class Message:
    def __init__(self, id: UUID = None):
        """Base class for Message objects.

        Args:
            id (uuid1): original id of message
        """
        self.id = id if id else uuid1()

    def reduce(self, responses, node):
        raise NotImplemented()

    @classmethod
    def deserialize(clss, data: dict):
        """To be implement by child message class"""
        raise NotImplemented()

    def serialize(self):
        """To be implmented by child message class"""
        raise NotImplemented()

    def gettype(self):
        return self.__class__.__name__

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
