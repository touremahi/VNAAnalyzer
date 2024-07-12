"""Main program for vna_analyzer.
"""
import sys
from PySide6.QtWidgets import QApplication
from vna_analyzer.ui import VNAAnalyzerApp

def main():
    """
    Runs the VNA Analyzer application.
    
    This function 
        creates a QApplication instance,
        instantiates the VNAAnalyzerApp class,
        shows the application window,
        and enters the application event loop.
    """
    app = QApplication(sys.argv)
    window = VNAAnalyzerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
