import unittest
from .context import grid
from grid.services.data_parser import parse


class TestDataParser(unittest.TestCase):

    def test_create_grid(self):
        x = parse()
        self.assertTrue(type(x) is list)


if __name__ == '__main__':
    unittest.main()
