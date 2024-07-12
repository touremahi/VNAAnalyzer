import unittest
from vna_analyzer.logic import load_network

class TestLogic(unittest.TestCase):
    def test_load_network(self):
        filepath = "path/to/testfile.s2p"
        network = load_network(filepath)
        self.assertIsNotNone(network)

if __name__ == '__main__':
    unittest.main()
