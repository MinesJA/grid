from grid.envelopes import Envelope
from grid.messages import Message
from uuid import UUID
from grid.utils.strFormatter import format_attrs
from grid.utils.valueGetters import getint, getuuid
from typing import Type
from grid.envelopes import Response
from grid.models.actor import Actor


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

    def build_response(self, msg: Message, node: Actor):
        sibling = node.siblings.get(self.return_id)

        if not sibling:
            raise ValueError(f'{self.return_id} not a recognized sibling')

        return Response(to=sibling.address,
                        msg=msg,
                        reqid=self.reqid,
                        master_reqid=self.master_reqid)

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
