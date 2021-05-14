from grid.envelopes import *
from grid.messages import *
from importlib import import_module
import json

__all__ = ['deserialize', 'serialize']
msg_mod = import_module('grid.messages')
env_mod = import_module('grid.envelopes')


def deserialize(req_body):

    data = json.loads(req_body)

    msg_type = data.get('msgType')
    env_type = data.get('envType')

    msg_class = getattr(msg_mod, msg_type)
    env_class = getattr(env_mod, env_type)
    msg_data = data.get('msg')

    msg_obj = msg_class.deserialize(msg_data)

    return env_class.deserialize(data, msg_obj)


def serialize(envelope):
    pass
