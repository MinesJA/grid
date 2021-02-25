import falcon
import json
import time

class PowerResource(object):

    def __init__(self, task_service, node):
        self.task_service = task_service
        self.node = node

    def on_get(self, req, resp):

        data = {'id': str(self.node.id),
                'production': self.node.production,
                'consumption': self.node.consumption,
                'net': self.node.net,
                'timestamp': time.time()
                }
        
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
            if msg_id not in node.messages:
                # Then this msg hasn't been dealt with. Update net and pass on to siblings
                node.messages.update(msg_id, req.media)
                node.adj_net(req.media.get('netAdj', 0))
                node.forward_message(req.media)

                resp.body = json.dumps({'msg': f'Node: {node.id} received Msg ID {msg_id} and net updated to {node.net}. CONTINUING'}, ensure_ascii=False)
            else:
                resp.body = json.dumps({'msg': f'Node: {node.id} received Msg ID {msg_id} but msg was already processed. Net: {node.net}. ENDING'}, ensure_ascii=False)
        else:
            prod_adj, con_adj = (req.media.get(key, 0) for key in ['prodAdj', 'conAdj'])

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

        
