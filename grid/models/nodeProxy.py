class NodeProxy:

    def __init__(self, id: str, address: str, port: str):
        self.id = id
        self.full_address = f'{address}:{port}'
        self.address = address
        self.port = port

    def __eq__(self, other):
        if isinstance(other, NodeProxy):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)
