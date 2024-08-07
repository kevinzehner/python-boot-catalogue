"""
This module defines the UiComponents class, which is responsible for setting up the UI components
of the application. It includes methods for initializing various widgets, setting their properties,
and populating data in the UI elements such as combo boxes. The UI layout is enhanced by setting
placeholders and loading images for display.
"""

import os
from PyQt5.QtWidgets import (
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
import database


class UiComponents:
    def setup_ui_components(self):
        """Initializes and sets up the UI components."""
        self.init_labels()
        self.init_comboboxes()
        self.init_buttons()
        self.init_results_area()

        self.set_placeholders()
        self.populate_manufacturers()

        self.init_images()

    def init_labels(self):
        self.logoLabel = self.findChild(QLabel, "logoLabel")
        if self.logoLabel is not None:
            self.logoLabel.setFixedSize(150, 150)  
            self.logoLabel.setAlignment(Qt.AlignCenter)

        self.messageLabel = self.findChild(QLabel, "messageLabel")
        self.instructionLabel = self.findChild(QLabel, "instructionLabel")
        if self.instructionLabel is not None:
            self.instructionLabel.setText(
                "<html><body><p>Please select the manufacturer, model, engine size, mark series,<br>"
                "drive type, position, and transmission to search for wheel bearings.</p></body></html>"
            )

    def init_comboboxes(self):
        """Initializes the dropdowns."""
        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")
        self.engineSizeComboBox = self.findChild(QComboBox, "engineSizeComboBox")
        self.markSeriesComboBox = self.findChild(QComboBox, "markSeriesComboBox")
        self.driveTypeComboBox = self.findChild(QComboBox, "driveTypeComboBox")
        self.positionComboBox = self.findChild(QComboBox, "positionComboBox")
        self.transmissionComboBox = self.findChild(QComboBox, "transmissionComboBox")

    def init_buttons(self):
        self.searchButton = self.findChild(QPushButton, "searchButton")
        self.resetButton = self.findChild(QPushButton, "resetButton")

    def init_results_area(self):
        self.resultsScrollArea = self.findChild(QScrollArea, "resultsScrollArea")

        self.resultsWidget = QWidget()
        self.resultsScrollArea.setWidget(self.resultsWidget)
        self.resultsScrollArea.setWidgetResizable(True)

        
        self.resultsLayout = QGridLayout(self.resultsWidget)
        self.resultsWidget.setLayout(self.resultsLayout)

      
        self.resultsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def init_images(self):
        self.set_logo_image()
        self.bottomImageLabel = self.findChild(QLabel, "bottomImageLabel")
        if self.bottomImageLabel is not None:
            self.set_bottom_image()

    def set_logo_image(self):
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "..", "main-images", "logo.JPG")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            self.logoLabel.setPixmap(
                pixmap.scaled(
                    self.logoLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )

    def set_bottom_image(self):
        """Sets the bottom image to the bottomImageLabel."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "..", "main-images", "boots-main-img.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.bottomImageLabel.setPixmap(
                pixmap.scaled(
                    self.bottomImageLabel.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
            )

    def set_placeholders(self):
        """Sets placeholder text for all combo boxes."""
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
        self.transmissionComboBox.addItem("Select transmission")
        self.transmissionComboBox.setCurrentIndex(0)

    def populate_manufacturers(self):
        """Populates the manufacturer combo box with data from the database."""
        manufacturers = database.get_unique_manufacturers("boots.db")
        self.manufacturerComboBox.addItems(manufacturers)
