from uuid import uuid1
from time import time
from grid.messages import Message
from uuid import UUID
from grid.utils.strFormatter import format_attrs
from grid.utils.valueGetters import getuuid, getstr, getfloat
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

    async def execute(self, node, mailroom):
        """The main execute method for messages.

        Messages have specific executable logic
        depending on the envelope they are wrapped
        in. This is the main entry point for that
        logic. Ensures the right method is called
        based on which envelope type calls it.

        Args:
            node ([type]): [description]
            mailroom ([type]): [description]

        Raises:
            NameError: [description]
        """
        env_type = self.gettype()
        method = f"from_{env_type.lower()}"
        if hasattr(self.msg, method):
            if callable(msg_func := getattr(self.msg, method)):
                # TODO: Confirm we want to pass in self as best
                #   way to get message func access to env details
                await msg_func(node, mailroom, self)
        else:
            raise NameError(
                f'Unrecognized method {method} called from {env_type}.'
            )

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
