from .node import Node

class Generator(Node):

    def __init__(self, address, supply_type, supply_multiple):
        """Generator unit which supplies power. Supply type
        can be any of the pre-established supply types.

        Args:
            supply_type (string): kwH demand_rate
            supply_multiple (float): multiplied against avg supply rate for that type
        """
        super().__init__(address)
        self.supply_type = supply_type
        self.supply_rate = supply_rate
