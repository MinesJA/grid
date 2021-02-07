import uuid

class Battery(Node):

    def __init__(self, max_charge, charge, supply_rate):
        self.id = self.id = uuid.uuid1()
        self.max_charge = max_charge
        self.charge = charge
        self.supply_rate = supply_rate

    
