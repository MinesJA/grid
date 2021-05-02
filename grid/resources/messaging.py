import falcon
from grid.models.envelope import *
from grid.models.message import *

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


class Messaging():

    def __init__(self, inbox):
        self.inbox = inbox

    async def on_get(self, req, resp, action, msg_type):
        """Should call proper envelope action on node
        with deserialized envelope wrapping message

        {
            "message": "dictionary",
            "replyToId": "uuid",
            "reqId": "uuid",
            "masterReqId": "uuid"
        }

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
            env_type (str): type of action
            msg_type (str): type of message
        """
        # TODO: Need better error handling:
        # 1. What if msg doesn't come back properly?
        # 2. What if inbox malfunctions?

        body = await req.get_media()
        msg_data = body.get('message')

        message = MESSAGE_TYPES.get(msg_type).deserialize(msg_data)
        envelope = ENVELOPE_TYPES.get(action).deserialize(body, message)

        await self.inbox.put(envelope)
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
