from uuid import uuid1
import aiohttp
import asyncio


# TODO: This should probably inherit from Actor but that would
# require Actor to not have it's own inbox
# OR would have to rethink how that works
class NodeProxy:

    def __init__(self, id: uuid1, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address

    def tell(self, envelope):

        async with aiohttp.ClientSession() as session:
            async with session.get(f'http://{self.address}/tell/') as response:

                print("Status:", response.status)
                print("Content-type:", response.headers['content-type'])

                html = await response.text()
                print("Body:", html[:15], "...")

    def ask(self, envelope, block=False):
        pass

    @classmethod
    def deserialize(clss, data):
        id = data.get('id')
        name = data.get('name')
        address = data.get('address')
        return clss(id, name, address)

    def __eq__(self, other):
        if isinstance(other, NodeProxy):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __str__(self):
        return f'NodeProxy<name={self.name}'\
            f' address={self.address}>'
