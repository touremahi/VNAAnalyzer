import unittest
from PySide6.QtWidgets import QApplication
from vna_analyzer.ui import VNAAnalyzerApp

app = QApplication([])

class TestUI(unittest.TestCase):
    def setUp(self):
        self.app = VNAAnalyzerApp()

    def test_initial_state(self):
        self.assertEqual(self.app.windowTitle(), "VNA Analyzer")

if __name__ == '__main__':
    unittest.main()
