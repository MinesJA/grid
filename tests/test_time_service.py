import unittest
from .context import grid

from grid.services.time_service import TimeService

class TestTimeService(unittest.TestCase):

    def test_start(self):
        ts = TimeService()
        ts.start()

if __name__ == '__main__':
    unittest.main()