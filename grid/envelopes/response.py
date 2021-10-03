from grid.envelopes import Envelope
from grid.messages import Message
from uuid import UUID
from grid.utils.strFormatter import format_attrs
from grid.utils.valueGetters import getuuid
from typing import Type


class Response(Envelope):

    def __init__(self,
                 to: str,
                 msg: Type[Message],
                 reqid: UUID,
                 master_reqid: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)
        self.reqid = reqid
        self.master_reqid = master_reqid if master_reqid else reqid

    @classmethod
    def deserialize(clss, data: dict, msg: Type[Message]):
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
        attrs = format_attrs(reqid=self.reqid,
                             master_reqid=self.master_reqid)
        return f'{super().__repr__()} {attrs}'

    def __str__(self):
        return self.__repr__()
