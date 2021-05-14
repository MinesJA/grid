from uuid import uuid1
from time import time
from grid.messages import *
from uuid import UUID
from grid.utils.strFormatter import *
from grid.utils.valueGetters import *
from typing import Type


class Envelope:

    def __init__(self,
                 to: str,
                 msg: Type[Message],
                 id: UUID = None,
                 timestamp: float = None):
        """
        TODO: docs....

        Args:
            to (str): address to
            msg (Message): Message object
            id (uuid1): [description]
            timestamp (float): timestamp of when envelope was sent
        """
        self.to = to
        self.msg = msg
        self.id = id if id else uuid1()
        self.timestamp = timestamp if timestamp else time()

    @classmethod
    def deserialize(clss, data: dict, msg: Type[Message]):
        return {'id': getuuid(data, 'id'),
                'to': getstr(data, 'to'),
                'msg': msg,
                'timestamp':  getfloat(data, 'timestamp')}

    def serialize(self):
        return {'to': self.to,
                'msgType': self.msg.gettype(),
                'envType': self.gettype(),
                'msg': self.msg.serialize(),
                'id': str(self.id),
                'timestamp': str(self.timestamp)}

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
        base_attrs = format_attrs(to=self.to, msg=self.msg)
        return f'[{clss_name}] {base_attrs}'

    def __str__(self):
        return self.__repr__()
