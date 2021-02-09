from .node import Node


class Commercial(Node):

    def __init__(self, address, supply_type, demand_multiple, supply_multiple):
        """Commercial unit which can both supply and consume power. Supply type
        can be any of the pre-established supply types.

        Args:
            supply_type (string): kwH demand_rate
            demand_multiple (float): multiplied against avg demand rate
            supply_multiple (float): multiplied against avg supply rate for that type
        """
        super().__init__()
        self.address = address
        self.supply_type = supply_type
        self.demand_rate = demand_rate
        self.supply_rate = supply_rate
