from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from gui.ui_components import UiComponents
from gui.ui_logic import UiLogic


class MainWindow(QMainWindow, UiComponents, UiLogic):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_window_new.ui", self)  # Load the new .ui file
        self.setup_ui_components()
        self.setup_ui_logic()
