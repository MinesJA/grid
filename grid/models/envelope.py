from uuid import uuid1
from time import time
from grid.models.message import Message
from uuid import UUID

__all__ = ['Tell', 'Ask', 'Response']


# TODO: If we want to convert to datetime and back again
# from timestamp float
# def to_timestamp(dt):
#     dt.replace(tzinfo=timezone.utc).timestamp()

class Envelope:

    def __init__(self,
                 to: str,
                 msg: Message,
                 id: UUID,
                 timestamp: float):
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

    def __repr__(self):
        # TODO: Redo this to format timestamp, not print uuid
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k, v in self.__dict__.items()]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'

    def format_url(self):
        action = self.__class__.__name__
        msg_type = self.msg.__class__.__name__
        return f'http://{self.to}/{action}/{msg_type}'


class Tell(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 id: UUID = None,
                 timestamp: float = None):
        super().__init__(to, msg, id, timestamp)

    @classmethod
    def deserialize(clss, msg, req_body):
        id = req_body.get('id')
        timestamp = req_body.get('timestamp')
        return clss(id, timestamp, msg)

    def serialize(self):
        return {'id': self.id,
                'timestamp': self.timestamp,
                'msg': self.msg.serialize()}


class Ask(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 reply_to_id: UUID,
                 req_id: UUID,
                 id: UUID = None,
                 timestamp: float = None,
                 master_req_id: UUID = None):
        """
        TODO: [SUMMARY]

        Args:
            id (UUID): [description]
            timestamp (float): [description]
            to (str): address of node to send envelope to
            msg (Message): [description]
            reply_to_id (UUID): id of node to reply to
            req_id (UUID): [description]
            master_req_id (UUID, optional): [description]. Request Id of
                initial request.
        """
        super().__init__(to, msg, id, timestamp)
        self.reply_to_id = reply_to_id
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id

    @classmethod
    def deserialize(clss, msg, req_body):
        id = req_body.get('id')
        timestamp = req_body.get('timestamp')
        reply_to_id = req_body.get('replyToId')
        req_id = req_body.get('reqId')
        master_req_id = req_body.get('masterReqId')

        return clss(id,
                    timestamp,
                    msg,
                    reply_to_id,
                    req_id,
                    master_req_id)

    def serialize(self):
        return {'id': self.id,
                'timestamp': self.timestamp,
                'msg': self.msg.serialize(),
                'replyToId': self.reply_to_id,
                'reqId': self.req_id,
                'masterReqId': self.master_req_id}


class Response(Envelope):

    def __init__(self,
                 to: str,
                 msg: Message,
                 req_id: UUID,
                 id: UUID = None,
                 timestamp: float = None,
                 master_req_id: UUID = None):
        super().__init__(to, msg, id, timestamp)
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id

    @classmethod
    def deserialize(clss, msg, req_body):
        id = req_body.get('id')
        timestamp = req_body.get('timestamp')
        req_id = req_body.get('reqId')
        master_req_id = req_body.get('masterReqId')

        return clss(id,
                    timestamp,
                    msg,
                    req_id,
                    master_req_id)

    def serialize(self):
        return {'id': self.id,
                'timestamp': self.timestamp,
                'msg': self.msg.serialize(),
                'reqId': self.req_id,
                'masterReqId': self.master_req_id}
