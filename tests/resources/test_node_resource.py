from falcon import testing
from tests.context import grid
from grid.app import get_app
# import myapp


class TestSetup(testing.TestCase):
    def setUp(self):
        super(TestSetup, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = get_app()


class TestNodeResource(TestSetup):
    def test_get_message(self):
        doc = {u'message': u'Hello world!'}

        result = self.simulate_get('/messages/42')
        self.assertEqual(result.json, doc)

    def test_put_message(self):
        doc = {u'message': u'Hello world!'}

        result = self.simulate_get('/messages/42')
        self.assertEqual(result.json, doc)