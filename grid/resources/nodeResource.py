import falcon
import json
from grid.models.node import Node


class NodeResource(object):

    def __init__(self, task_service, node):
        self.task_service = task_service
        self.node = node

    def on_get(self, req, resp):
        
        siblings = [s.__dict__ for s in self.node.siblings]

        resp.body = json.dumps(siblings, ensure_ascii=False)

    # /nodes
    def on_put(self, req, resp):
        # Todo: Custom serializer?
        siblings = [Node(n.get('address'))
                    for n in req.media.get('nodes', [])]

        self.node.add_siblings(siblings)

        data = {'msg': f'Added {len(siblings)} siblings'}
        resp.body = json.dumps(data, ensure_ascii=False)
        resp.status = falcon.HTTP_200