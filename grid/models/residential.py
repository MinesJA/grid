from .node import Node
from ..models.node import SupplyType
# SupplyType(head).name

class Residential(Node):

    def __init__(self, address, supply_type, demand_multiple, supply_multiple):
        """[summary]

        Args:
            supply_type (string): kwH demand_rate
            demand_multiple (float): [description]
            supply_multiple (float): [description]
        """
        super().__init__(address)
        self.supply_type = supply_type
        self.demand_multiple = demand_multiple
        self.supply_multiple = supply_multiple