import pytest
from falcon import testing
from grid.server import create_app
from grid.models.node import Node, NodeBuilder
from unittest.mock import AsyncMock
from unittest import TestCase
from grid.models.nodeProxy import NodeProxy


@pytest.fixture()
def mock_builder():
    node = Node('n1', '111.222.333', 1234, 10, 5)
    node.siblings = {'n2': NodeProxy('n2', '222.333.444', 2345)}
    node_builder = AsyncMock()
    node_builder.get.return_value = node
    return node_builder


@pytest.fixture()
def builder():
    return NodeBuilder('n1', '111.222.333', 1234, 10, 5)


@pytest.fixture()
def client(node_builder):
    app = create_app(node_builder)
    client = testing.TestClient(app)
    return client


def test_get_siblings(client):
    resp = client.simulate_get('/nodes/siblings')

    assert resp.status == '200 OK'
    TestCase().assertDictEqual(resp.json, {'siblings': ['222.333.444:2345']})


def test_get_energy(client):
    resp = client.simulate_get('/nodes/energy')

    assert resp.status == '200 OK'
    TestCase().assertDictEqual(resp.json,
                               {'production': 10, 'consumption': 5, 'net': 5})
