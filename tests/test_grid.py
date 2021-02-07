import unittest
from .context import grid

from grid.models.grid import Grid
from grid.models.node import Node
from grid.models.house import House


class TestGrid(unittest.TestCase):

    def test_create_grid(self):
        grid = Grid()
        self.assertEqual(grid.nodes, {})

    def test_add_node(self):
        grid = Grid()

        node_a = House(1, 2)
        node_b = House(1, 2)
        node_c = House(1, 2)

        grid.nodes = {
            node_a: [node_b, node_c],
            node_b: [node_a],
            node_c: [node_a]
        }

        node_d = House(3, 4)

        grid.add_node(node_d, [node_b, node_c])

        self.assertListEqual(grid.nodes[node_b], [node_a, node_d])
        self.assertListEqual(grid.nodes[node_c], [node_a, node_d])
        self.assertListEqual(grid.nodes[node_d], [node_b, node_c])

    def test_remove_node(self):
        


if __name__ == '__main__':
    unittest.main()
