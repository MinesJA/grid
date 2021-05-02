from asyncio import Queue


# TODO: Rethink hierarchy - Actor, Node, NodeProxy
class Actor:

    def __init__(self, id, address):
        self.id = id
        self.address = address

    def on_receive(self, message):
        # To be implemented by child class
        raise NotImplemented()
