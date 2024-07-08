"""
This module defines the MainWindow class, which is the main GUI window of the application.
The MainWindow class inherits from QMainWindow and integrates UI components and logic by
inheriting from UiComponents and UiLogic classes. The UI layout is loaded from a .ui file,
and the setup methods for components and logic are called during initialization.
"""

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
