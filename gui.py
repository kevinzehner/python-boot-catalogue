import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox
from PyQt5 import uic
import database

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_window.ui", self)
        self.initializeUI()

    def initializeUI(self):
        self.messageLabel = self.findChild(QLabel, "messageLabel")
        self.messageLabel.setText("Wheel Bearing Catalogue")

        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")
        self.engineSizeComboBox = self.findChild(QComboBox, "engineSizeComboBox")
        self.markSeriesComboBox = self.findChild(QComboBox, "markSeriesComboBox")
        self.driveTypeComboBox = self.findChild(QComboBox, "driveTypeComboBox")
        self.positionComboBox = self.findChild(QComboBox, "positionComboBox")

        self.set_placeholders()
        self.populate_manufacturers()

        self.manufacturerComboBox.currentIndexChanged.connect(self.update_models)
        self.modelComboBox.currentIndexChanged.connect(self.update_engine_sizes)
        self.engineSizeComboBox.currentIndexChanged.connect(self.update_mark_series)
        self.markSeriesComboBox.currentIndexChanged.connect(self.update_drive_types)
        self.driveTypeComboBox.currentIndexChanged.connect(self.update_positions)

    def set_placeholders(self):
        self.manufacturerComboBox.addItem("Select manufacturer")
        self.manufacturerComboBox.setCurrentIndex(0)
        self.modelComboBox.addItem("Select model")
        self.modelComboBox.setCurrentIndex(0)
        self.engineSizeComboBox.addItem("Select engine size")
        self.engineSizeComboBox.setCurrentIndex(0)
        self.markSeriesComboBox.addItem("Select mark series")
        self.markSeriesComboBox.setCurrentIndex(0)
        self.driveTypeComboBox.addItem("Select drive type")
        self.driveTypeComboBox.setCurrentIndex(0)
        self.positionComboBox.addItem("Select position")
        self.positionComboBox.setCurrentIndex(0)

    def populate_manufacturers(self):
        manufacturers = database.get_unique_manufacturers('wheelbearings.db')
        self.manufacturerComboBox.addItems(manufacturers)

    def update_models(self):
        self.clear_combo_box(self.modelComboBox, "Select model")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        if selected_manufacturer == "Select manufacturer":
            self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
            self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
            self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
            self.clear_combo_box(self.positionComboBox, "Select position")
            return
        models = database.get_models('wheelbearings.db', selected_manufacturer)
        self.modelComboBox.addItems(models)
        self.update_engine_sizes()

    def update_engine_sizes(self):
        self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        if selected_model == "Select model":
            self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
            self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
            self.clear_combo_box(self.positionComboBox, "Select position")
            return
        engine_sizes = database.get_engine_sizes('wheelbearings.db', selected_manufacturer, selected_model)
        self.engineSizeComboBox.addItems(engine_sizes)
        self.update_mark_series()

    def update_mark_series(self):
        self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        if selected_engine_size == "Select engine size":
            self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
            self.clear_combo_box(self.positionComboBox, "Select position")
            return
        mark_series = database.get_mark_series('wheelbearings.db', selected_manufacturer, selected_model, selected_engine_size)
        self.markSeriesComboBox.addItems(mark_series)
        self.update_drive_types()

    def update_drive_types(self):
        self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        selected_mark_series = self.markSeriesComboBox.currentText()
        if selected_mark_series == "Select mark series":
            self.clear_combo_box(self.positionComboBox, "Select position")
            return
        drive_types = database.get_drive_types('wheelbearings.db', selected_manufacturer, selected_model, selected_engine_size, selected_mark_series)
        self.driveTypeComboBox.addItems(drive_types)
        self.update_positions()

    def update_positions(self):
        self.clear_combo_box(self.positionComboBox, "Select position")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        selected_mark_series = self.markSeriesComboBox.currentText()
        selected_drive_type = self.driveTypeComboBox.currentText()
        if selected_drive_type == "Select drive type":
            return
        positions = database.get_positions('wheelbearings.db', selected_manufacturer, selected_model, selected_engine_size, selected_mark_series, selected_drive_type)
        self.positionComboBox.addItems(positions)

    def clear_combo_box(self, combo_box, placeholder):
        combo_box.clear()
        combo_box.addItem(placeholder)