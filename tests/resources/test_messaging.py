import pytest
from uuid import uuid1
from falcon import testing
from unittest import TestCase
from unittest.mock import AsyncMock
from grid.server import create_app
from grid.models.node import Node, NodeBuilder
from grid.models.nodeProxy import NodeProxy


@pytest.fixture()
def mock_builder():
    # id = uuid1()
    node = Node('n1', 'abcd', '111.222.333', 1234, 10, 5)
    node.siblings = {'n2': NodeProxy('n2', '222.333.444', 2345)}
    node_builder = AsyncMock()
    node_builder.get.return_value = node
    return node_builder


@pytest.fixture()
def builder():
    return NodeBuilder('n1', 'abcd', '111.222.333', 1234, 10, 5)


@pytest.fixture()
def client(builder):

    app = create_app(inbox, token, id)
    client = testing.TestClient(app)
    return client


# def test_ask(client):
#     # response = client.simulate_get('/messages/addsibling',
#     # json={'sibling': '127.0.0.1:8080'})
#     assert 1 == 2


# def test_tell(client):
#     assert 1 == 2


def test_update_energy(client):
    resp = client.simulate_get(
        '/tell/updateenergy',
        json={'production': 5},
        headers={'authorization': 'abcd'})

    assert resp.status == '200 OK'

    import pdb
    pdb.set_trace()

    # TestCase().assertDictEqual(resp.json,
    #                            {'production': 5, 'consumption': 5, 'net': 0})
