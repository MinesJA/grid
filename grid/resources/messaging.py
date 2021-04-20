import falcon
from grid.models.node import Node
from grid.models.node import NodeProxy
from grid.models.message import Envelope, UpdateEnergy, UpdateNet, AddSibling
from operator import itemgetter

from grid.models.message import deserialize, Message

# TODO: Not sure if deserializatio belongs in here
MESSAGE_TYPES = {
    'updateenergy': UpdateEnergy,
    'updatenet': UpdateNet,
    'addsibling': AddSibling,
}


def deserialize(type, message):
    """Creates a Message object from a type
    and message dict. Uses factory pattern.

    https://realpython.com/factory-method-python/

    Args:
        type (str): type of message
        message (dict): dict of info

    Returns:
        Message: Message based type
    """
    message_class = MESSAGE_TYPES.get(type)
    if message_class is not None:
        message_class.deserializer(message)
    else:
        raise ValueError(type)

# TODO: Prob shoulld be considered a controller?


class Messaging():

    def __init__(self, inbox):
        self.inbox = inbox

    async def on_get_ask(self, req, resp, type):
        """Should deserialize message to proper message
        object and call 'ask' of node and return result
        in response.
            ex. address: 'messaging/ask/addsibling?sender=n1'
                body: {id: 'abcd123, sibling: '123.123.123:8080'}

        {
            "message": {
                "id": "uuid",
                "timestamp": "datetime",
                "sibling_address": "str",
                "sibling_id": "uuid",
                "sibling_name": "str"
            },
            "reply_to": "uuid"
        }

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
            type (str): type of message
        """

        body = await req.get_media()
        message = body.get('message')
        recip_id = body.get('reply_to')
        msg_obj = deserialize(type, message)

        # # TODO: What if this is already in Node
        # # siblings dict?
        # sibling = NodeProxy.deserialize(reply_to)
        envelope = Envelope(msg_obj, recip_id)
        # TODO: Need a try catch here
        await self.inbox.put(envelope)

        resp.status = falcon.HTTP_200

    async def on_get_tell(self, req, resp, type):
        """Should drop a tell message into inbox and
        let the response be a 200.

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
            type (str): type of message
        """
        msg = await req.get_media()
        msg_obj = deserialize(type, msg)
        envelope = Envelope(msg_obj)
        # TODO: Need a try catch here
        await self.inbox.put(msg_obj)

        resp.status = falcon.HTTP_200

# As an IoT device, I will send an UpdateEnergy message:
# to: http://address:port/tell?type=updateenergy
# {token: 'my_auth_token', consumption: 15}
#
# Message will be deserialized
# Auth will be checked
# Then tell will be called
# Tell should drop message into message queue
# Where it should be picked up and dealth with


# def on_put_siblings(self, req, resp):
#         """Add a sibling to Node

#         Args:
#             req ([type]): [description]
#             resp ([type]): [description]
#         """
#         sib_addr, sib_port = itemgetter('address', 'port')(req.media)
#         sibling = Node(address=sib_addr, port=sib_port)
#         self.node.add_sibling(sibling)

#         print(
#             f'({self.node.full_address}): Adding sibling with address
# {sib_addr}:{sib_port}')

#         data = {'msg': f'Added sibgling: {sibling.full_address}'}
#         # resp.media  = json.dumps(data, ensure_ascii=False)
#         resp.media = data

#  async def on_patch_energy(self, req, resp):
#         """Updates a nodes consumption and production values.
#         Will automatically trigger attemp to update all other Nodes
#         net values.

#         Ex. body:
#             {
#                 production: 5,
#                 consumption: 10
#             }

#         Must be called withauthentication.

#         Args:
#             req (Request): Falcon Request object
#             resp (Response): Falcon Response object
#         """
#         node = await self.node_builder.get()

#         media = await req.get_media()
#         node.update_energy(media.get(CONSUMPTION), media.get(PRODUCTION))

#         resp.body = json.dumps(node.get_energy(), ensure_ascii=False)
