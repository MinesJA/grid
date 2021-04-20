class Envelope:
    # NOTE: Borrowed partially from Pykka

    # Using slots speeds up envelope creation with ~20%
    __slots__ = ['id', 'msg', 'reply_to', 'resp_msg']


def __init__(self, id, msg, reply_to=None, resp_msg=None):
    """[summary]

    Args:
        id (uuid1): [description]
        msg (Message): [description]
        reply_to (uuid1, optional): [description]. Defaults to None.
        resp_message (uuid1): [description]. Defaults to None.
    """
    self.id = id
    self.msg = msg
    self.reply_to = reply_to
    self.resp_msg = resp_msg


def __repr__(self):
    return f'Envelope<message={self.msg}, \
        reply_to={self.reply_to}, \
        resp_msg={self.resp_msg}>'
