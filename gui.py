import os
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QComboBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QGridLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
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
        self.searchButton = self.findChild(QPushButton, "searchButton")
        self.resetButton = self.findChild(QPushButton, "resetButton")

        self.resultsScrollArea = self.findChild(QScrollArea, "resultsScrollArea")

        # Create a QWidget and set it as the widget for resultsScrollArea
        self.resultsWidget = QWidget()
        self.resultsScrollArea.setWidget(self.resultsWidget)
        self.resultsScrollArea.setWidgetResizable(True)

        # Set a layout for the resultsWidget
        self.resultsLayout = QGridLayout(self.resultsWidget)
        self.resultsWidget.setLayout(self.resultsLayout)

        self.set_placeholders()
        self.populate_manufacturers()

        self.manufacturerComboBox.currentIndexChanged.connect(self.update_models)
        self.modelComboBox.currentIndexChanged.connect(self.update_engine_sizes)
        self.engineSizeComboBox.currentIndexChanged.connect(self.update_mark_series)
        self.markSeriesComboBox.currentIndexChanged.connect(self.update_drive_types)
        self.driveTypeComboBox.currentIndexChanged.connect(self.update_positions)
        self.searchButton.clicked.connect(self.search_parts)
        self.resetButton.clicked.connect(self.reset_dropdowns)

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
        manufacturers = database.get_unique_manufacturers("wheelbearings_LSODS.db")
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
        models = database.get_models("wheelbearings_LSODS.db", selected_manufacturer)
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
        engine_sizes = database.get_engine_sizes(
            "wheelbearings_LSODS.db", selected_manufacturer, selected_model
        )
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
        mark_series = database.get_mark_series(
            "wheelbearings_LSODS.db",
            selected_manufacturer,
            selected_model,
            selected_engine_size,
        )
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
        drive_types = database.get_drive_types(
            "wheelbearings_LSODS.db",
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
        )
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
        positions = database.get_positions(
            "wheelbearings_LSODS.db",
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
            selected_drive_type,
        )
        self.positionComboBox.addItems(positions)

    def clear_combo_box(self, combo_box, placeholder):
        combo_box.clear()
        combo_box.addItem(placeholder)

    def reset_dropdowns(self):
        # Reset the dropdowns
        self.clear_combo_box(self.manufacturerComboBox, "Select manufacturer")
        self.clear_combo_box(self.modelComboBox, "Select model")
        self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
        self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
        self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
        self.clear_combo_box(self.positionComboBox, "Select position")
        self.populate_manufacturers()

        # Clear the results layout
        self.clear_results()

    def clear_results(self):
        layout = self.resultsLayout
        count = layout.count()

        while count > 0:
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            count -= 1

        self.resultsWidget.update()
        self.resultsScrollArea.update()

    def search_parts(self):
        manufacturer = self.manufacturerComboBox.currentText()
        model = self.modelComboBox.currentText()
        engine_size = self.engineSizeComboBox.currentText()
        mark_series = self.markSeriesComboBox.currentText()
        drive_type = self.driveTypeComboBox.currentText()
        position = self.positionComboBox.currentText()

        criteria = {
            "manufacturer": (
                manufacturer if manufacturer != "Select manufacturer" else None
            ),
            "model": model if model != "Select model" else None,
            "engine_size": engine_size if engine_size != "Select engine size" else None,
            "mark_series": mark_series if mark_series != "Select mark series" else None,
            "drive_type": drive_type if drive_type != "Select drive type" else None,
            "position": position if position != "Select position" else None,
        }

        parts = database.get_parts("wheelbearings_LSODS.db", criteria)

        self.display_results(parts)

    def display_results(self, parts):
        self.clear_results()
        layout = self.resultsLayout

        # Add new results
        row = 0
        col = 0
        for part in parts:
            part_number, part_size, image_file = part

            # Create a layout to hold the image and text
            part_layout = QVBoxLayout()

            # Load and display the image
            image_label = QLabel()
            image_path = os.path.join(
                "wheelbearing-img2", image_file.replace(".jpeg", ".jpg")
            )
            if not os.path.exists(image_path):
                image_path = os.path.join("wheelbearing-img2", "generic.jpg")

            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(
                100, 100, Qt.KeepAspectRatio
            )  # Adjust the size as needed
            image_label.setPixmap(pixmap)
            part_layout.addWidget(image_label)

            # Display the part details
            part_label = QLabel(f"Part Number: {part_number}, Part Size: {part_size}")
            part_layout.addWidget(part_label)

            # Create a widget to hold the part layout and add it to the grid layout
            part_widget = QWidget()
            part_widget.setLayout(part_layout)
            layout.addWidget(part_widget, row, col)

            col += 1
            if col >= 3:  # Change the number of columns as needed
                col = 0
                row += 1

        self.resultsWidget.update()
        self.resultsScrollArea.update()
