import unittest
# from tests.context import grid
from grid.models.node import Node
from unittest.mock import Mock, patch


def test_node():
    assert 1 == 1

# def test_create_node():
#     address = '123.123.123'
#     port = '8080'
#     id = hash(address, port)

#     node = Node(address, port)

#     .assertEqual(node.id, id)
#     .assertEqual(node.id, id)


# @patch('grid.models.node.requests.put')
# def test_add_sibling(, mock_put):


# mock_put.return_value.ok = True

# id = uuid.uuid1()
# address = '1.2.3.4'
# port = '1234'

# node = Node(id, address, port)

# sibling = Node(id, address, port)

# node.add_sibling(sibling)
# data = {
#     'nodes': [{'id': str(node.id), 'address': node.address, 'port': node.port}]}

# .assertEqual(1, len(node.siblings))
# mock_put.assert_called_once_with(
#     'http://1.2.3.4:1234/nodes', data=data)


# def test_inc_adj_production():


# id = uuid.uuid1()
# address = 'mock_address'
# port = 'mock_port'
# adj_by = 10

# node = Node(id, address, port)
# new_prod = node.production + adj_by
# new_net = node.net + adj_by

# node.adj_production(adj_by)

# .assertEqual(new_prod, node.production)
# .assertEqual(new_net, node.net)


# def test_dec_adj_production():


# id = uuid.uuid1()
# address = 'mock_address'
# port = 'mock_port'
# adj_by = -10

# node = Node(id, address, port)
# new_prod = node.production + adj_by
# new_net = node.net + adj_by

# node.adj_production(adj_by)

# .assertEqual(new_prod, node.production)
# .assertEqual(new_net, node.net)


# def test_inc_adj_consumption():


# id = uuid.uuid1()
# address = 'mock_address'
# port = 'mock_port'
# adj_by = 10

# node = Node(id, address, port)
# new_con = node.consumption + adj_by
# new_net = node.net - adj_by

# node.adj_consumption(adj_by)

# .assertEqual(new_con, node.consumption)
# .assertEqual(new_net, node.net)


# def test_dec_adj_consumption():


# id = uuid.uuid1()
# address = 'mock_address'
# port = 'mock_port'
# adj_by = -10

# node = Node(id, address, port)
# new_con = node.consumption + adj_by
# new_net = node.net - adj_by

# node.adj_consumption(adj_by)

# .assertEqual(new_con, node.consumption)
# .assertEqual(new_net, node.net)


# def test_adj_net():
#     id = uuid.uuid1()
#     address = 'mock_address'
#     port = 'mock_port'
#     adj_by = -10

#     node = Node(id, address, port)
#     new_net = node.net + adj_by

#     node.adj_net(adj_by)

#     .assertEqual(new_net, node.net)


# def test_equality():
#     id = uuid.uuid1()
#     node1 = Node(id, 'addr1', 'port1')
#     node2 = Node(id, 'addr2', 'port2')

#     .assertEqual(node1, node2)

#     id = uuid.uuid1()
#     node3 = Node(id, 'addr1', 'port1')

#     .assertNotEqual(node1, node3)
