import uuid
import enum


class Node():

    def __init__(self, address):
        self.id = uuid.uuid1()
        self.address = address

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.id == other.id
        return False

    def __hash__(self):
        """Overrides the default implementation"""
        return id(self.id)


