import time
import json
import logging
import falcon
from grid.models.node import Node
from operator import itemgetter

from grid.models.message import deserialize, Message


class Messages():

    def __init__(self, builder):
        self.builder = builder

    async def on_get(self, req, resp):
        """Should call 'ask' of master node and return result
            in response. 

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        # TODO: Need to deserialize this to a message
        
        media = await req.get_media()
        # {
        #  id: 'msg123',
        #  type: 'AddSibling',
        #  sender: 'address:port',
        #  sibling: 'address:port',
        #  self.sibling = sibling
        # }
        # AddSibling

        import pdb; pdb.set_trace()

        node = await self.builder.get_node(self.config)
        import pdb; pdb.set_trace()

        result = node.ask(message)
        
        f'Successfully asked {node.id} with {message.id}'

        resp.media = {'result': ''}
        resp.status = falcon.HTTP_200


    async def on_put(self, req, resp, type):
        """Should call 'tell' of master node and let 
        the response be a 200

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        
        msg = await req.get_media()

        msg_obj = deserialize(type, msg)

        node = await self.builder.get_node(self.config)
        node.tell(msg_obj)
        resp.status = falcon.HTTP_200
