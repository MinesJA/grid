import pytest
import falcon
from falcon import testing
from unittest.mock import MagicMock
# from grid.app import app
from grid.server import create_app


# @mock.patch('grid.server.parse_args',
#             return_value=argparse.Namespace(id='n1', address='123.123.123', port=1234))


def test_app():
    assert 1 == 1

# @pytest.fixture
# def client():
#     return testing.TestClient(app)


# @pytest.fixture
# def mock_args():
#     return MagicMock()


# @pytest.fixture
# def client(mock_args):
#     app = create_app(mock_args)
#     return testing.TestClient(app)


# def test_get_messages(client):
#     body = {'sibling': '127.0.0.1:8080'}

#     response = client.simulate_get('/messages/addsibling')
#     # result_doc = msgpack.unpackb(response.content, raw=False)

#     assert response.status == falcon.HTTP_OK


# def test_ask(client):
#     response = client.simulate_get('/messages/addsibling')

#     response = client.simulate_get(
#         '/ask/addsibling',
#         body={'sibling': '127.0.0.1:8080'},
#         headers={'content-type': 'application/json'}
#     )

#     import pdb
#     pdb.set_trace()
#     # result_doc = msgpack.unpackb(response.content, raw=False)

#     assert response.status == falcon.HTTP_OK
