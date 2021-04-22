from uuid import uuid1
from grid.models.message import UpdateNet


class Envelope:
    # NOTE: Borrowed partially from Pykka

    # # Using slots speeds up envelope creation with ~20%
    # __slots__ = ['id', 'msg', 'reply_to', 'resp_msg']

    def __init__(self, id, msg):
        """[summary]

        Args:
            id (uuid1): [description]
            msg (Message): [description]
            reply_to (uuid1, optional): [description]. Defaults to None.
            resp_message (uuid1): [description]. Defaults to None.
        """
        self.id = id
        self.msg = msg

    def __repr__(self):
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k, v in self.__dict__.items()]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'


class Tell(Envelope):

    def __init__(self, id, msg):
        super().__init__(id, msg)


class Ask(Envelope):

    def __init__(self, msg, reply_to, req_id, master_req_id=None):
        """[summary]

        Args:
            msg ([type]): [description]
            reply_to (uuid1): id of node to reply to
            req_id ([type]): [description]
            master_req_id ([type], optional): [description]. Defaults to None.
        """
        super().__init__(uuid1(), msg)
        self.reply_to = reply_to
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id


class Response(Envelope):

    def __init__(self, msg, req_id, master_req_id=None):
        super().__init__(uuid1(), msg)
        self.req_id = req_id
        self.master_req_id = master_req_id if master_req_id else req_id
