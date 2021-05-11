from uuid import uuid1
from time import time
from grid.models.message import Message
from uuid import UUID
from grid.utils.strFormatter import *
from grid.utils.valueGetters import *


__all__ = ['Envelope', 'Tell', 'Ask', 'Response']


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
        attrs = format_attrs(to=self.to,
                             msg=self.msg)
        return f'{super().__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()


class Ask(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 return_id: int,
                 reqid: UUID,
                 master_reqid: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        """
        TODO: [SUMMARY]

        Args:

            to (str): address of node to send envelope to
            msg (Message): [description]
            return_id (UUID): id of node to reply to
            reqid (UUID): id to be used in response
            master_reqid (UUID, optional): Request Id of primary request.
            id (UUID): id of message
            timestamp (float): [description]
        """
        super().__init__(to, msg, id, timestamp)
        self.return_id = return_id
        self.reqid = reqid
        self.master_reqid = master_reqid if master_reqid else reqid

    @classmethod
    def deserialize(clss, data: dict, msg: Message):

        return_id = getint(data, 'returnId')
        reqid = getuuid(data, 'reqId')
        master_reqid = getuuid(data, 'masterReqId')

        return clss(return_id=return_id,
                    reqid=reqid,
                    master_reqid=master_reqid,
                    **super().deserialize(data, msg))

    def serialize(self):
        dict = {'returnId': str(self.return_id),
                'reqId': str(self.reqid),
                'masterReqId': str(self.master_reqid)}
        return {**super().serialize(), **dict}

    def __repr__(self):
        attrs = format_attrs(return_id=self.return_id,
                             reqid=self.reqid,
                             master_reqid=self.master_reqid)
        return f'{super().__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()


class Response(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 reqid: UUID,
                 master_reqid: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)
        self.reqid = reqid
        self.master_reqid = master_reqid if master_reqid else reqid

    @classmethod
    def to_ask(clss, ask: Ask, msg, node):
        sibling = node.siblings.get(ask.return_id)

        if not sibling:
            raise ValueError(f'{ask.return_id} not a recognize sibling')

        return clss(to=sibling.address,
                    msg=msg,
                    reqid=ask.reqid,
                    master_reqid=ask.master_reqid)

    @classmethod
    def deserialize(clss, data: dict, msg: Message):
        reqid = getuuid(data, 'reqId')
        master_reqid = getuuid(data, 'masterReqId')

        return clss(reqid=reqid,
                    master_reqid=master_reqid,
                    **super().deserialize(data, msg))

    def serialize(self):
        dict = {'reqId': str(self.reqid),
                'masterReqId': str(self.master_reqid)}
        return {**super().serialize(), **dict}

    def __repr__(self):
        attrs = format_attrs(return_id=self.return_id,
                             reqid=self.reqid,
                             master_reqid=self.master_reqid)
        return f'{super().__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()
