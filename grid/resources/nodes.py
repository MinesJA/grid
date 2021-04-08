import json
from grid.models.node import Node
from operator import itemgetter


CONSUMPTION = 'consumption'
PRODUCTION = 'production'


class Nodes:
    """The Resource for all Node related info. All requests
    must provide proper authorization. Intended for the actual
    owner of the Node, not for communiation between other Nodes.

    TODO: Implement Auth
    """

    def __init__(self, node_builder):
        self.node_builder = node_builder

    async def on_get_siblings(self, req, resp):
        """Get all siblings of a node.

        TODO: Must be called with authentication.

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
        """
        node = await self.node_builder.get()

        # TODO: This type of serialization should be moved to node
        resp.media = {'siblings': [
            sibling.full_address for sibling in node.siblings.values()]}

    async def on_get_energy(self, req, resp):
        """Get all energy related values
        from specific node.

        TODO: Must be called with authentication.

        TODO: Implement requesting specific values
            ie. only consumption or production

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
        """
        node = await self.node_builder.get()
        # TODO: Serializer...
        data = node.get_energy()

        resp.body = json.dumps(data, ensure_ascii=False)

    async def on_patch_energy(self, req, resp):
        """Updates a nodes consumption and production values.
        Will automatically trigger attemp to update all other Nodes
        net values.

        Ex. body:
            {
                production: 5,
                consumption: 10
            }

        Must be called withauthentication.

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
        """
        node = await self.node_builder.get()

        media = await req.get_media()
        node.update_energy(media.get(CONSUMPTION), media.get(PRODUCTION))

        resp.body = json.dumps(node.get_energy(), ensure_ascii=False)
