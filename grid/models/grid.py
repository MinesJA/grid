from typing import List


class Grid():

    def __init__(self):
        self.nodes = {}
        self.drawing = {}
        self.generating = {}

    def add_node(self, node: 'Node', connections: List['Node']):
        for conn in connections:
            try:
                self.nodes[conn].append(node)
            except KeyError as e:
                print(
                    'Connection does not exist in grid. Can only connect to existing nodes.')
                print(e)
        self.nodes[node] = connections

    def remove_node(self, node: 'Node'):
        try:
            for n in self.nodes[node]:
                self.nodes[n].remove(node)

            del self.nodes[node]
        except KeyError as e:
            print('Node does not exist in grid.')
            print(e)
