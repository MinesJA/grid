from uuid import UUID


# TODO: This should probably inherit from Actor but that would
# require Actor to not have it's own inbox
# OR would have to rethink how that works

class NodeProxy:

    def __init__(self, id: UUID, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address

    def __eq__(self, other):
        if isinstance(other, NodeProxy):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __str__(self):
        return f'NodeProxy<name={self.name}'\
            f' address={self.address}>'
