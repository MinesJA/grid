from .node import Node


# Demand Rate and supply rate in kw/hr
class House(Node):

    def __init__(self, demand_rate, supply_rate):
        """[summary]

        Args:
            demand_rate ([type]): [description]
            supply_rate ([type]): [description]
        """
        super().__init__()
        self.demand_rate = demand_rate
        self.supply_rate = supply_rate