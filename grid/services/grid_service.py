from .data_parser import parse
from ..models.grid import Grid

from ..models.residential import Residential
from ..models.commercial import Commercial
from ..models.generator import Generator


NODE_TYPES = {
        'Residential': Residential,
        'Commericial': Commercial,
        'Generator': Generator
    }   


def build_grid():
    
    grid = Grid()
    nodes = {}

    for d in parse():
        # - Residential:
        #     address: 5
        #     supplyType: solar
        #     demandMultiple: 0.5
        #     supplyMultiple: 1

        head, *tail = d.keys()

        node_class = NODE_TYPES[head]
        print(node_class)
        node = node_class.build(d[head])
        nodes[node.address] = node

    for address, node in nodes.items():
        connections = list(map(lambda addr: nodes[addr], node.connections))
        grid.add_node(node, connections)

    return grid
