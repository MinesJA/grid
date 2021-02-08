import uuid
from .node import Node

class Battery(Node):

    def __init__(self, max_charge, charge, supply_rate):
        super().__init__()
        self.max_charge = max_charge
        self.charge = charge
        self.supply_rate = supply_rate

    
