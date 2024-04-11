import unittest
from src.utils import stringify


class TestUtils(unittest.TestCase):
    def test_stringify_rnb(self):
        expected = "R N B"
        result = stringify("r-n-b")
        self.assertEqual(expected, result)


    def test_stringify_pop(self):
        expected = "Pop"
        result = stringify("pop")
        self.assertEqual(expected, result)

    def test_stringify_french_hip_hop(self):
        expected = "French Hip Hop"
        result = stringify("french hip-hop")
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
