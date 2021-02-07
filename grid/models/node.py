import uuid 

class Node:
    
    def __init__(self):
        self.id = uuid.uuid1()

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Node):
            return self.id == other.id
        return False
    
    def __hash__(self):
        """Overrides the default implementation"""
        return id(self.id)