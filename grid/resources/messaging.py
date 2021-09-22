import falcon
from grid.serializer import *


class Messaging():

    def __init__(self, inbox):
        self.inbox = inbox

    async def on_get(self, req, resp):
        """Should call proper envelope action on node
        with deserialized envelope wrapping message

        TODO: This should be a POST

        Args:
            req (Request): Falcon Request object
            resp (Response): Falcon Response object
            action (str): type of envelope action
        """
        # TODO: Need better error handling:
        # 1. What if msg doesn't come back properly?
        # 2. What if inbox malfunctions?
        envelope = await req.get_media()
        await self.inbox.put(envelope)
        resp.status = falcon.HTTP_200
