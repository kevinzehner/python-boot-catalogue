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
    QGridLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5 import uic
import database


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main_window_new.ui", self)  # Load the new .ui file
        self.initializeUI()

        # Load the stylesheet
        self.loadStylesheet("style.qss")

    def loadStylesheet(self, file_name):
        with open(file_name, "r") as file:
            self.setStyleSheet(file.read())

    def initializeUI(self):
        self.messageLabel = self.findChild(QLabel, "messageLabel")
        self.instructionLabel = self.findChild(QLabel, "instructionLabel")
        if self.instructionLabel is not None:
            self.instructionLabel.setText(
                "<html><body><p>Please select the manufacturer, model, engine size, mark series,<br>"
                "drive type, and position to search for wheel bearings.</p></body></html>"
            )
        else:
            print("instructionLabel not found")

        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")
        self.engineSizeComboBox = self.findChild(QComboBox, "engineSizeComboBox")
        self.markSeriesComboBox = self.findChild(QComboBox, "markSeriesComboBox")
        self.driveTypeComboBox = self.findChild(QComboBox, "driveTypeComboBox")
        self.positionComboBox = self.findChild(QComboBox, "positionComboBox")
        self.transmissionComboBox = self.findChild(
            QComboBox, "transmissionComboBox"
        )  # New dropdown
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

        # Set size policy to ensure the widget expands properly
        self.resultsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Find the new portrait labels
        self.imageLabel_1 = self.findChild(QLabel, "imageLabel_1")
        self.imageLabel_2 = self.findChild(QLabel, "imageLabel_2")

        # Set placeholder images for portrait labels
        self.setPortraitImages()

        # Set the logo image to the messageLabel
        self.setLogoImage()

        self.set_placeholders()
        self.populate_manufacturers()

        self.manufacturerComboBox.currentIndexChanged.connect(self.update_models)
        self.modelComboBox.currentIndexChanged.connect(self.update_engine_sizes)
        self.engineSizeComboBox.currentIndexChanged.connect(self.update_mark_series)
        self.markSeriesComboBox.currentIndexChanged.connect(self.update_drive_types)
        self.driveTypeComboBox.currentIndexChanged.connect(self.update_positions)
        self.positionComboBox.currentIndexChanged.connect(
            self.update_transmissions
        )  # Connect new dropdown
        self.searchButton.clicked.connect(self.search_parts)
        self.resetButton.clicked.connect(self.reset_dropdowns)

    def setPortraitImages(self):
        # Set the image for the first portrait label
        pixmap1 = QPixmap(os.path.join("main-images", "main2.JPG"))
        self.imageLabel_1.setPixmap(
            pixmap1.scaled(
                self.imageLabel_1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def setLogoImage(self):
        # Set the logo image to the messageLabel
        logo_path = os.path.join(
            "main-images", "title.png"
        )  # Replace with the actual logo image path
        pixmap = QPixmap(logo_path)
        self.messageLabel.setPixmap(
            pixmap.scaled(
                self.messageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

        # Set the image for the second portrait label
        pixmap2 = QPixmap(os.path.join("main-images", "main4.JPG"))
        self.imageLabel_2.setPixmap(
            pixmap2.scaled(
                self.imageLabel_2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

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
        self.transmissionComboBox.addItem(
            "Select transmission"
        )  # Set placeholder for new dropdown
        self.transmissionComboBox.setCurrentIndex(0)

    def populate_manufacturers(self):
        manufacturers = database.get_unique_manufacturers("boots.db")
        self.manufacturerComboBox.addItems(manufacturers)

    def update_models(self):
        self.clear_combo_box(self.modelComboBox, "Select model")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        if selected_manufacturer == "Select manufacturer":
            self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
            self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
            self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
            self.clear_combo_box(self.positionComboBox, "Select position")
            self.clear_combo_box(
                self.transmissionComboBox, "Select transmission"
            )  # Clear new dropdown
            return
        models = database.get_models("boots.db", selected_manufacturer)
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
            self.clear_combo_box(
                self.transmissionComboBox, "Select transmission"
            )  # Clear new dropdown
            return
        engine_sizes = database.get_engine_sizes(
            "boots.db", selected_manufacturer, selected_model
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
            self.clear_combo_box(
                self.transmissionComboBox, "Select transmission"
            )  # Clear new dropdown
            return
        mark_series = database.get_mark_series(
            "boots.db",
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
            self.clear_combo_box(
                self.transmissionComboBox, "Select transmission"
            )  # Clear new dropdown
            return
        drive_types = database.get_drive_types(
            "boots.db",
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
            self.clear_combo_box(
                self.transmissionComboBox, "Select transmission"
            )  # Clear new dropdown
            return
        positions = database.get_positions(
            "boots.db",
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
            selected_drive_type,
        )
        self.positionComboBox.addItems(positions)
        self.update_transmissions()  # Update new dropdown

    def update_transmissions(self):
        self.clear_combo_box(self.transmissionComboBox, "Select transmission")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        selected_mark_series = self.markSeriesComboBox.currentText()
        selected_drive_type = self.driveTypeComboBox.currentText()
        selected_position = self.positionComboBox.currentText()
        if selected_position == "Select position":
            return
        transmissions = database.get_transmissions(
            "boots.db",
            selected_manufacturer,
            selected_model,
            selected_engine_size,
            selected_mark_series,
            selected_drive_type,
            selected_position,
        )
        self.transmissionComboBox.addItems(transmissions)

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
        self.clear_combo_box(self.transmissionComboBox, "Select transmission")
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
        transmission = self.transmissionComboBox.currentText()  # Get new dropdown value

        criteria = {
            "manufacturer": (
                manufacturer if manufacturer != "Select manufacturer" else None
            ),
            "model": model if model != "Select model" else None,
            "engine_size": engine_size if engine_size != "Select engine size" else None,
            "mark_series": mark_series if mark_series != "Select mark series" else None,
            "drive_type": drive_type if drive_type != "Select drive type" else None,
            "position": position if position != "Select position" else None,
            "transmission": (
                transmission if transmission != "Select transmission" else None
            ),  # Add new criteria
        }

        parts = database.get_parts("boots.db", criteria)

        self.display_results(parts)

    def display_results(self, parts):
        self.clear_results()
        layout = self.resultsLayout

        row = 0
        col = 0
        for part in parts:
            part_number, part_size = part

            # Create a layout to hold the text
            part_layout = QVBoxLayout()

            # Display the part number
            part_number_label = QLabel(f"Part Number: {part_number}")
            part_number_label.setAlignment(Qt.AlignCenter)
            part_number_label.setObjectName("partNumberLabel")
            part_layout.addWidget(part_number_label)

            # Display the part size
            part_size_label = QLabel(f"Part Size: {part_size}")
            part_size_label.setAlignment(Qt.AlignCenter)
            part_size_label.setObjectName("partSizeLabel")
            part_layout.addWidget(part_size_label)

            # Create a widget to hold the part layout and add it to the grid layout
            part_widget = QWidget()
            part_widget.setLayout(part_layout)
            layout.addWidget(
                part_widget, row, col, alignment=Qt.AlignTop | Qt.AlignLeft
            )

            col += 1
            if col >= 3:  # Change the number of columns as needed
                col = 0
                row += 1

        self.resultsWidget.setLayout(layout)
        self.resultsWidget.update()
        self.resultsScrollArea.update()
