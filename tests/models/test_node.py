import pytest
from grid.models.node import Node
from unittest import TestCase


def test_create_node():
    id = 'n1'
    address = '123.123.123'
    port = 1234
    consumption = 10
    production = 5

    node = Node(id, address, port, consumption, production)

    assert type(node) is Node
    assert node.id == id
    assert node.address == address
    assert node.port == port
    assert node.consumption == consumption
    assert node.production == production
    assert node.net == 5
    assert node.full_address == f'{address}:{port}'
    assert node.siblings == {}


def test_equality():
    id = 'n1'
    consumption = 10
    production = 5

    address1 = '111.111.111'
    address2 = '222.222.222'
    port1 = 1111
    port2 = 2222

    node1 = Node(id, address1, port1, consumption, production)
    node2 = Node(id, address2, port2, consumption, production)
    node3 = Node('n2', address2, port2, consumption, production)

    assert node1 == node2
    assert node1 != node3


def test_get_energy():
    id = 'n1'
    address = '123.123.123'
    port = 1234
    consumption = 10
    production = 5

    node = Node(id, address, port, consumption, production)
    data = {'consumption': consumption, 'production': production, 'net': 5}

    TestCase().assertDictEqual(node.get_energy(), data)


def test_update_energy():
    id = 'n1'
    address = '123.123.123'
    port = 1234
    consumption = 10
    production = 5

    node = Node(id, address, port, consumption, production)

    node.update_energy(consumption=20, production=None)
    assert node.consumption == 20
    assert node.production == production

    node.update_energy(consumption=None, production=10)
    assert node.consumption == 20
    assert node.production == 10

    node.update_energy(consumption=30, production=20)
    assert node.consumption == 30
    assert node.production == 20


def test_on_receive():
    assert 1 == 2


def test_add_sibling():
    assert 1 == 2


def test_update_siblings():
    assert 1 == 2

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
