import pytest
from falcon import testing
from unittest import TestCase
from unittest.mock import AsyncMock
from grid.server import create_app
from grid.models.node import Node
from grid.models.nodeProxy import NodeProxy


@pytest.fixture()
def mock_builder():
    node = Node('n1', '111.222.333', 1234, 10, 5)
    node.siblings = {'n2': NodeProxy('n2', '222.333.444', 2345)}
    node_builder = AsyncMock()
    node_builder.get.return_value = node
    return node_builder


@pytest.fixture()
def client(mock_builder):
    app = create_app(mock_builder)
    client = testing.TestClient(app)
    return client


def test_ask(client):
    # response = client.simulate_get('/messages/addsibling',
    # json={'sibling': '127.0.0.1:8080'})
    assert 1 == 2


def test_tell(client):
    assert 1 == 2
