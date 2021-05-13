from grid.envelopes.envelope import Envelope
from uuid import uuid1
from grid.messages import *
from grid.models.node import Node
from uuid import UUID
from grid.utils.strFormatter import *
from grid.utils.valueGetters import *
from typing import Type


class Tell(Envelope):

    def __init__(self,
                 to: str,
                 msg: Type[Message],
                 return_id: int,
                 reqid: UUID,
                 master_reqid: UUID = None,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)
        self.return_id = return_id
        self.reqid = reqid
        self.master_reqid = master_reqid if master_reqid else reqid

    @classmethod
    def from(clss, node: Node, msg: Type[Message]):
        return clss(node.address, msg, node.id, uuid1())

    @classmethod
    def deserialize(clss, data: dict, msg: Type[Message]):

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
