"""
    UI elements
    It sets up the user interface, handles user interactions,
        and manages the loading and plotting of network data.
"""
import os
import logging
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QKeySequence, QShortcut, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton,
    QFileDialog, QListWidget, QListWidgetItem,
    QMessageBox, QWidget, QHBoxLayout)
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import matplotlib.pyplot as plt

from vna_analyzer.logic import load_network

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='vna_analyzer.log')

class VNAAnalyzerApp(QMainWindow):
    """The `VNAAnalyzerApp` class is the main entry point for the VNA Analyzerapplication."""

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.modify_widgets()
        self.setup_connections()

        plt.rcParams['axes.grid'] = True
        self.network = None

    def setup_ui(self):
        """
        Sets up the user interface for the VNA Analyzer application.
        
        This method initializes the main window,
        creates the central widget and layout, and adds the following UI elements:
        
        The layout and connections between the UI elements are also set up in this method.
        """
        self.setWindowTitle("VNA Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.btn_layout = QHBoxLayout()

        self.load_button = QPushButton("Charger un fichier .s2p")
        self.btn_layout.addWidget(self.load_button)

        self.save_image_button = QPushButton("Exporter Capture d'écran")
        self.btn_layout.addWidget(self.save_image_button)

        self.save_s2p_button = QPushButton("Exporter .s2p")
        self.btn_layout.addWidget(self.save_s2p_button)

        self.layout.addLayout(self.btn_layout)
        self.res_layout = QHBoxLayout()

        # Ajouter ListWidget
        self.lw_data = QListWidget()

        self.lw_data.setMinimumWidth(200)
        self.lw_data.setMinimumHeight(400)
        self.lw_data.setMaximumWidth(400)

        self.res_layout.addWidget(self.lw_data)

        self.fig, self.axes = plt.subplots(2, 2)
        self.fig.suptitle('S-parameters (dB and phase)')
        self.canvas = FigureCanvas(self.fig)

        self.res_layout.addWidget(self.canvas)
        self.layout.addLayout(self.res_layout)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar)

    def modify_widgets(self):
        """
        Applies a custom stylesheet to the main window of the VNA Analyzer application.
        The stylesheet is loaded from a file named 'styles.qss'
        """
        try:
            self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resources', 'VNAAnalyzer.ico')))
            if hasattr(sys, '_MEIPASS'):
                # pylint: disable=protected-access
                qss_file = os.path.join(sys._MEIPASS, 'vna_analyzer', 'resources', 'styles.qss')
            else:
                qss_file = os.path.join(os.path.dirname(__file__), 'resources', 'styles.qss')

            with open(qss_file, 'r', encoding='utf-8') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            logging.error("Impossible de charger le fichier de styles.")
            QMessageBox.critical(self, "Erreur", "Impossible de charger le fichier de styles.")
            self.setStyleSheet("")

    def setup_connections(self):
        """
        Sets up the connections between
        the UI elements and their corresponding event handlers.
        """
        self.load_button.clicked.connect(self.load_file)
        self.save_image_button.clicked.connect(self.export_image)
        self.save_s2p_button.clicked.connect(self.export_s2p)

        self.lw_data.itemSelectionChanged.connect(self.selected_item)
        QShortcut(QKeySequence("Delete"), self).activated.connect(self.delete_seleted_item)

    def load_file(self):
        """
        If an error occurs a critical error message is displayed to the user.
        """
        file_filter = "S2P Touchstone (*.s2p);;DAT Files (*.dat);;All Files (*)"
        selected_filter = "S2P Touchstone (*.s2p)"
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Sélectionnez un fichier", "",
                                                  file_filter,
                                                  selected_filter,
                                                  options=options)
        if filepath:
            self.load_data(filepath)

    def load_data(self, filepath):
        """
        Attempts to load network data from the specified file path.
        If OK, the `plot_data()` method is called to update the plot.
        If an error occurs during the file loading process,
            a critical error message is displayed to the user.
        
        Args:
            filepath (str): The file path of the .dat file to load.
        
        Raises:
            Exception: If an error occurs while loading the file.
        """

        try:
            self.network = load_network(filepath)
            element = LwItem(self.network.name)
            element.network = self.network
            self.lw_data.addItem(element)
            self.plot_data()
        except FileNotFoundError as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de lecture du fichier: {e}")
        except Exception as e: # pylint: disable=broad-except
            logging.error("Une erreur inattendue s'est produite", exc_info=True)
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le fichier: {e}")

    def selected_item(self):
        """
        Returns the currently selected item in the list widget.

        Returns:
            str: The currently selected item in the list widget.
        """
        selected_items = self.lw_data.selectedItems()
        if not selected_items:
            return None
        selected_item = selected_items[0]
        self.network = selected_item.network
        self.plot_data()

    def delete_seleted_item(self):
        """
        Deletes the currently selected item in the list widget.
        """
        selected_items = self.lw_data.selectedItems()
        if not selected_items:
            return
        selected_item = selected_items[0]
        self.lw_data.takeItem(self.lw_data.row(selected_item))

        if self.lw_data.count() == 0:
            self.network = None
            self.__clear_axes()
            self.canvas.draw()
        else:
            self.network = self.lw_data.item(0).network
            self.plot_data()

    def plot_data(self):
        """
        Plots the network data on the figure canvas.
        """
        self.__clear_axes()
        # S11_S22_dB
        # self.axes[0][0].set_title('S11 & S22 (dB)')
        self.network.plot_s_db(m=0,n=0,ax=self.axes[0][0])
        self.network.plot_s_db(m=1,n=1,ax=self.axes[0][0])

        # S11_S22_phase
        # self.axes[0][1].set_title('S11 & S22 (deg)')
        self.network.plot_s_deg(m=0,n=0,ax=self.axes[0][1])
        self.network.plot_s_deg(m=1,n=1,ax=self.axes[0][1])

        # S21_S12_dB
        # self.axes[1][0].set_title('S21 & S12 (dB)')
        self.network.plot_s_db(m=1,n=0,ax=self.axes[1][0])
        self.network.plot_s_db(m=0,n=1,ax=self.axes[1][0])

        # S21_S12_phase
        # self.axes[1][1].set_title('S21 & S12 (deg)')
        self.network.plot_s_deg(m=1,n=0,ax=self.axes[1][1])
        self.network.plot_s_deg(m=0,n=1,ax=self.axes[1][1])

        self.axes[0][0].set_ylim(top=1)
        self.axes[1][0].set_ylim(top=1)

        self.canvas.draw()

    def __clear_axes(self):
        """
        Clears the axes of the figure canvas.
        """
        self.axes[0][0].clear()
        self.axes[0][1].clear()
        self.axes[1][0].clear()
        self.axes[1][1].clear()

    def export_image(self):
        """
        Exports the current plot as an image file.
        If a network data has been loaded, this method opens a file dialog 
            to allow the user to select a save location and 
            file name for the exported image. 
            The plot is then saved to the selected file path in PNG format.
        
        If no network data has been loaded,
            a warning message is displayed to the user.
        """
        if self.network:
            options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Exporter Capture d'écran", "",
                                                       "PNG Files (*.png);;All Files (*)",
                                                       options=options)
            if save_path:
                self.fig.savefig(save_path)
                QMessageBox.information(self, "Succès", "Capture d'écran exportée avec succès")
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez d'abord charger un fichier")

    def export_s2p(self):
        """
        Exports the current network data to an S2P file.
        If a network data has been loaded,
            this method opens a file dialog
            to allow the user to select a save location
            and file name for the exported S2P file.
            The network data is then written to the selected file path in S2P format.

        If no network data has been loaded,
            a warning message is displayed to the user.
        """
        if self.network:
            options = QFileDialog.Options()
            save_path, _ = QFileDialog.getSaveFileName(self, "Exporter .s2p", "",
                                                       "S2P Files (*.s2p);;All Files (*)",
                                                       options=options)
            if save_path:
                self.network.write_touchstone(save_path)
                QMessageBox.information(self, "Succès", "Fichier .s2p exporté avec succès")
        else:
            QMessageBox.warning(self, "Avertissement", "Veuillez d'abord charger un fichier")

class LwItem(QListWidgetItem):
    """
    A custom QListWidgetItem subclass that sets the size hint and text alignment to be centered.
    """
    def __init__(self, titre):
        super().__init__(titre)
        self.setSizeHint(QSize(80,80))
        self.setTextAlignment(Qt.AlignCenter)
        self.network = None

if __name__ == "__main__":
    pass
