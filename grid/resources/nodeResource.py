import time
import falcon
import json
from grid.models.node import Node
import logging
from operator import itemgetter


class NodeResource(object):

    def __init__(self, task_service, node):
        self.task_service = task_service
        self.node = node




    def on_get_message(self, req, resp):


    def on_put_message(self, req, resp):
        


    def on_get_siblings(self, req, resp):
        print(
            f'({self.node.full_address}): Getting {len(self.node.siblings)} siblings')
        resp.media = {'siblings': [
            sibling.full_address for sibling in self.node.siblings.values()
        ]}

    def on_get_net(self, req, resp):
        """Get net power output of grid
            as registered by specific node

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        print(f'({self.node.full_address}): Getting net power')
        resp.media = {'net': self.node.net}

    def on_get_energy(self, req, resp):
        """Get consumption and production values
        from specific node. Must be called with
        authentication (should not be open to 
        non-authenticated requests)

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        print(f'({self.node.full_address}): Getting energy values')
        resp.media = {
            'consumption': self.node.consumption,
            'production': self.node.production
        }

    def on_put_siblings(self, req, resp):
        """Add a sibling to Node

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        sib_addr, sib_port = itemgetter('address', 'port')(req.media)
        sibling = Node(address=sib_addr, port=sib_port)
        self.node.add_sibling(sibling)

        print(f'({self.node.full_address}): Adding sibling with address {sib_addr}:{sib_port}')

        data = {'msg': f'Added sibgling: {sibling.full_address}'}
        # resp.media  = json.dumps(data, ensure_ascii=False)
        resp.media = data


    def on_put_power(self, req, resp):
        """Updates a nodes power values. Can update
        Consumption, Production. Must be called with
        authentication (should not be open to 
        non-authenticated requests)

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """

    def on_put_net(self, req, resp):
        """Updates net output


        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """

        msgId = req.media.get('msgId')

        if(msgId in self.node.messages):
            # Must mean we've already processed this
            # No need to process again
            print("Handle")
        else:
            sib_net = req.media.get('net')
            self.node.adj_net()



        # 

       


class PowerResource(object):

    def __init__(self, task_service, node):
        self.task_service = task_service
        self.node = node

    def on_get(self, req, resp):

        data = {'id': str(self.node.id),
                'production': self.node.production,
                'consumption': self.node.consumption,
                'net': self.node.net,
                'timestamp': time.time()}

        resp.body = json.dumps(data, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        # Todo: If there is no body, then media will be none, should handle

        # Two options:
        #   1) Updating prod or con or both
        #   2) Updating net

        # {
        #  prodAdj:
        #   conAdj:
        # }

        # {
        #    msgId:
        #   netAdj:
        # }

        msg_id = req.media.get('msgId')

        if msg_id is not None:
            if msg_id not in self.node.messages:
                # Then this msg hasn't been dealt with. Update net and pass on to siblings
                self.node.messages.update(msg_id, req.media)
                self.node.adj_net(req.media.get('netAdj', 0))
                self.node.forward_message(req.media)

                resp.body = json.dumps(
                    {'msg': f'Node: {self.node.id} received Msg ID {msg_id} and net updated to {node.net}. CONTINUING'}, ensure_ascii=False)
            else:
                resp.body = json.dumps(
                    {'msg': f'Node: {self.node.id} received Msg ID {msg_id} but msg was already processed. Net: {node.net}. ENDING'}, ensure_ascii=False)
        else:
            prod_adj, con_adj = (req.media.get(key, 0)
                                 for key in ['prodAdj', 'conAdj'])

            # Adj prod or con
            # Recalculate net
            # Send message to siblings with updated net

            self.node.adj_production(prod_adj)
            self.node.adj_consumption(con_adj)
            self.node.update_siblings()

            data = {'id': str(self.node.id),
                    'production': self.node.production,
                    'consumption': self.node.consumption,
                    'net': self.node.net,
                    'timestamp': time.time()
                    }

            resp.body = json.dumps(data, ensure_ascii=False)
