import unittest
from tests.context import grid
from grid.models.node import uuid
from grid.models.node import Node


class TestNode(unittest.TestCase):

    @patch('grid.models.node.requests.put')
    def test_add_sibling(self, mock_put):
        mock_put.return_value.ok = True

        id = uuid.uuid1()
        address = 'mock_address'
        port = 'mock_port'

        node = Node(id, address, port)

        sibling = Node(id, address, port)

        node.add_sibling(sibling)

        self.assertEqual(1, len(node.siblings))
        

    def test_inc_adj_production(self):
        id = uuid.uuid1()
        address = 'mock_address'
        port = 'mock_port'
        adj_by = 10

        node = Node(id, address, port)

        new_prod = node.production + adj_by
        node.adj_production(adj_by)

        self.assertEqual(new_prod, node.production)

    def test_dec_adj_production(self):
        id = uuid.uuid1()
        address = 'mock_address'
        port = 'mock_port'
        adj_by = -10

        node = Node(id, address, port)

        new_prod = node.production + adj_by
        node.adj_production(adj_by)

        self.assertEqual(new_prod, node.production)

    def test_inc_adj_consumption(self):
        id = uuid.uuid1()
        address = 'mock_address'
        port = 'mock_port'
        adj_by = 10

        node = Node(id, address, port)

        new_prod = node.consumption + adj_by
        node.adj_consumption(adj_by)

        self.assertEqual(new_prod, node.consumption)

    def test_dec_adj_consumption(self):
        id = uuid.uuid1()
        address = 'mock_address'
        port = 'mock_port'
        adj_by = -10

        node = Node(id, address, port)

        new_prod = node.consumption + adj_by
        node.adj_consumption(adj_by)

        self.assertEqual(new_prod, node.production)


if __name__ == '__main__':
    unittest.main()
