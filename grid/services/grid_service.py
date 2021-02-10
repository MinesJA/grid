from .data_parser import parse
from ..models.node import NODE_TYPES


def build_grid():
    details = parse()

    # [{'Residential': {...}}, {'Residential': {...}}, {'Residential': {...}}, {'Residential': {...}}, {'Residential': {...}}, {'Commercial': {...}}, {'Commercial': {...}}, {'Generator': {...}}]

    nodes = {}

    for d in details:
        # - Residential:
        #     address: 5
        #     supplyType: solar
        #     demandMultiple: 0.5
        #     supplyMultiple: 1

        head, *tail = d.keys()

        node_class = NODE_TYPES[head]
        node = node_class.build(d[head])
        
        conns = d[head]['connections']


        



        
