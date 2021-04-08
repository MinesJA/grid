import falcon
from grid.models.node import Node
from operator import itemgetter

from grid.models.message import deserialize, Message


class Messages():

    def __init__(self, node_builder):
        self.node_builder = node_builder

    async def on_get_ask(self, req, resp, type):
        """Should call 'ask' of master node and return result
            in response. 

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        # TODO: Need to deserialize this to a message

        msg = await req.get_media()
        # {
        #  id: 'msg123',
        #  type: 'AddSibling',
        #  sender: 'address:port',
        #  sibling: 'address:port',
        #  self.sibling = sibling
        # }
        # AddSibling

        node = await self.node_builder.get(self.config)

        result = node.ask(msg)

        f'Successfully asked {node.id} with {msg.id}'

        resp.media = {'result': ''}
        resp.status = falcon.HTTP_200

    async def on_get_tell(self, req, resp, type):
        """Should call 'tell' of master node and let 
        the response be a 200.

        Args:
            req (Request): [description]
            resp (Response): [description]
            type (str): [description]
        """

        msg = await req.get_media()

        msg_obj = deserialize(type, msg)

        node = await self.node_builder.get(self.config)
        node.tell(msg_obj)
        resp.status = falcon.HTTP_200


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
#             f'({self.node.full_address}): Adding sibling with address {sib_addr}:{sib_port}')

#         data = {'msg': f'Added sibgling: {sibling.full_address}'}
#         # resp.media  = json.dumps(data, ensure_ascii=False)
#         resp.media = data