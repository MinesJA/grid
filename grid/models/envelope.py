from uuid import uuid1
from time import time
from grid.models.message import Message
from uuid import UUID
from grid.utils.strFormatter import *
from grid.utils.valueGetters import *


__all__ = ['Tell', 'Ask', 'Response']


# TODO: If we want to convert to datetime and back again
# from timestamp float
# def to_timestamp(dt):
#     dt.replace(tzinfo=timezone.utc).timestamp()

class Envelope:

    def __init__(self,
                 to: str,
                 msg: Message,
                 id: UUID = None,
                 timestamp: float = None):
        """[summary]

        Args:
            id (uuid1): [description]
            timestamp (float): timestamp of when envelope was sent
            to (str): address to
            msg (Message): Message object
        """
        self.to = to
        self.msg = msg
        self.id = id if id else uuid1()
        self.timestamp = timestamp if timestamp else time()

    def get_type(self):
        return self.__class__.__name__

    @classmethod
    def deserialize(clss, data: dict, msg: Message):
        return {'id': getuuid(data, 'id'),
                'to': getstr(data, 'to'),
                'msg': msg,
                'timestamp':  getfloat(data, 'timestamp')}

    def serialize(self):
        return {'to': self.to,
                'msgType': self.msg.get_type(),
                'envType': self.get_type(),
                'msg': self.msg.serialize(),
                'id': str(self.id),
                'timestamp': str(self.timestamp)}

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


class Tell(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)

    @classmethod
    def deserialize(clss, req_body: dict, msg: Message):
        return clss(**super().deserialize(req_body, msg))

    def serialize(self):
        return super().serialize()

    def __repr__(self):
        attrs = format_attrs(production=self.production,
                             consumption=self.consumption,
                             net=self.net,
                             grid_net=self.grid_net)
        return f'{super().__str__()} {attrs}'

    def __str__(self):
        return self.__repr__()


class Ask(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 return_id: int,
                 req_id: UUID,
                 master_req_id: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        """
        TODO: [SUMMARY]

        Args:

            to (str): address of node to send envelope to
            msg (Message): [description]
            return_id (UUID): id of node to reply to
            req_id (UUID): id to be used in response
            master_req_id (UUID, optional): Request Id of primary request.
            id (UUID): id of message
            timestamp (float): [description]
        """
        super().__init__(to, msg, id, timestamp)
        self.return_id = return_id
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id

    @classmethod
    def deserialize(clss, data: dict, msg: Message):

        return_id = getint(data, 'returnId')
        req_id = getuuid(data, 'reqId')
        master_req_id = getuuid(data, 'masterReqId')

        return clss(return_id=return_id,
                    req_id=req_id,
                    master_req_id=master_req_id,
                    **super().deserialize(data, msg))

    def serialize(self):
        dict = {'returnId': str(self.return_id),
                'reqId': str(self.req_id),
                'masterReqId': str(self.master_req_id)}
        return {**super().serialize(), **dict}

    def __repr__(self):
        attrs = format_attrs(return_id=self.return_id,
                             req_id=self.req_id,
                             master_req_id=self.master_req_id)
        return f'{super().__str__()} {attrs}'

    def __str__(self):
        return self.__repr__()


class Response(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 req_id: UUID,
                 master_req_id: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id

    @classmethod
    def to_ask(clss, ask: Ask, msg, node):
        sibling = node.siblings.get(ask.return_id)

        if not sibling:
            raise ValueError(f'{ask.return_id} not a recognize sibling')

        return clss(to=sibling.address,
                    msg=msg,
                    req_id=ask.req_id,
                    master_req_id=ask.master_req_id)

    @classmethod
    def deserialize(clss, data: dict, msg: Message):
        req_id = getuuid(data, 'reqId')
        master_req_id = getuuid(data, 'masterReqId')

        return clss(req_id=req_id,
                    master_req_id=master_req_id,
                    **super().deserialize(data, msg))

    def serialize(self):
        dict = {'reqId': str(self.req_id),
                'masterReqId': str(self.master_req_id)}
        return {**super().serialize(), **dict}

    def __repr__(self):
        attrs = format_attrs(return_id=self.return_id,
                             req_id=self.req_id,
                             master_req_id=self.master_req_id)
        return f'{super().__str__()} {attrs}'

    def __str__(self):
        return self.__repr__()
