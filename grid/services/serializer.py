from grid.models.envelope import *
from grid.models.message import *
from importlib import import_module
import json

__all__ = ['deserialize', 'serialize']
msg_mod = import_module('grid.models.message')
env_mod = import_module('grid.models.envelope')

MESSAGE_TYPES = {
    'updatenet': UpdateNet,
    'addsibling': AddSibling,
    'updateenergy': UpdateEnergy
}

ENVELOPE_TYPES = {
    'ask': Ask,
    'tell': Tell,
    'response': Response
}


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

# class CustomJsonEncoder(json.JSONEncoder):
#     def default(self, o):
#         # Here you can serialize your object depending of its type
#         # or you can define a method in your class which serializes the object
#         if isinstance(o, (Employee, Autocar)):
#             return o.__dict__  # Or another method to serialize it
#         else:
#             return json.JSONEncoder.encode(self, o)


# >>> import json
# >>> def as_complex(dct):
# ...     if '__complex__' in dct:
# ...         return complex(dct['real'], dct['imag'])
# ...     return dct
# ...
# >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
# ...     object_hook=as_complex)
# (1+2j)
# >>> import decimal
# >>> json.loads('1.1', parse_float=decimal.Decimal)
# Decimal('1.1')


# # Usage
# json.dumps(items, cls=CustomJsonEncoder)
