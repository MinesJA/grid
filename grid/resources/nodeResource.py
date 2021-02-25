import falcon
import json
from grid.models.node import Node
import uuid
import logging


class NodeResource(object):

    def __init__(self, task_service, node):
        self.task_service = task_service
        self.node = node

    def on_get(self, req, resp):
        print(f'SIblings length get: {len(self.node.siblings)}')
        siblings = [node.__dict__ for id, node in self.node.siblings.items()]
        print(f'{len(siblings)} siblings get')
        resp.body = json.dumps(siblings, ensure_ascii=False)

    def on_put(self, req, resp):
        """Adds Siblings to Node

        Node -> [Siblings]
        Siblings <- Node

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        # Todo: Custom serializer?
        siblings = [Node(id=uuid.UUID(n.get('id')), address=n.get('address'), port=n.get('port'))
                    for n in req.media.get('nodes', [])]

        print(f'{len(siblings)} siblings are being added')

        # If siblings aren't in node siblings yet
        for node in siblings:
            if node.id not in self.node.siblings:
                print(f'Adding sibling {node.port}')
                self.node.add_sibling(node)

        data = {'msg': f'Added {len(siblings)} siblings'}
        resp.body = json.dumps(data, ensure_ascii=False)
