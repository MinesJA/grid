import unittest
from .context import grid
from grid.services.data_parser import parse
from grid.services.grid_service import build_grid


class TestDataParser(unittest.TestCase):

    def test_create_grid(self):
        grid = build_grid()
        self.assertTrue(type(x) is list)


if __name__ == '__main__':
    unittest.main()
