import uuid 


# Demand Rate and supply rate in kw/hr
class House(object):

    def __init__(self, demand_rate, supply_rate):
        self.id = uuid.uuid1()
        self.demand_rate = demand_rate
        self.supply_rate = supply_rate