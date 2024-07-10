"""
This module defines the UiLogic class, which contains the logic for handling user interactions 
and dynamic updates to the UI components. It includes methods to update combo boxes based on 
user selections, reset the UI, search for parts based on criteria, and display the results. 
The logic is separated from the UI component initialization to ensure modularity and maintainability.
"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import database
import os


class UiLogic:
    def setup_ui_logic(self):
        """Connects signals to the appropriate slots for updating the UI based on user interactions."""
        self.manufacturerComboBox.currentIndexChanged.connect(self.update_models)
        self.modelComboBox.currentIndexChanged.connect(self.update_engine_sizes)
        self.engineSizeComboBox.currentIndexChanged.connect(self.update_mark_series)
        self.markSeriesComboBox.currentIndexChanged.connect(self.update_drive_types)
        self.driveTypeComboBox.currentIndexChanged.connect(self.update_positions)
        self.positionComboBox.currentIndexChanged.connect(self.update_transmissions)
        self.searchButton.clicked.connect(self.search_parts)
        self.resetButton.clicked.connect(self.reset_dropdowns)

    def update_models(self):
        """Updates the model combo box based on the selected manufacturer."""
        self.clear_combo_box(self.modelComboBox, "Select model")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        if selected_manufacturer == "Select manufacturer":
            self.clear_all_combo_boxes(except_boxes=["manufacturer"])
            return
        models = database.get_models("boots.db", selected_manufacturer)
        self.modelComboBox.addItems(models)
        self.update_engine_sizes()  # Avoiding recursion issues by ensuring order of operations

    def update_engine_sizes(self):
        """Updates the engine size combo box based on the selected model."""
        self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        if selected_model == "Select model":
            self.clear_all_combo_boxes(except_boxes=["manufacturer", "model"])
            return
        engine_sizes = database.get_engine_sizes(
            "boots.db", selected_manufacturer, selected_model
        )
        self.engineSizeComboBox.addItems(engine_sizes)
        self.update_mark_series()

    def update_mark_series(self):
        """Updates the mark series combo box based on the selected engine size."""
        self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        if selected_engine_size == "Select engine size":
            self.clear_all_combo_boxes(
                except_boxes=["manufacturer", "model", "engine_size"]
            )
            return
        mark_series = database.get_mark_series(
            "boots.db", selected_manufacturer, selected_model, selected_engine_size
        )
        self.markSeriesComboBox.addItems(mark_series)
        self.update_drive_types()

    def update_drive_types(self):
        """Updates the drive type combo box based on the selected mark series."""
        self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        selected_mark_series = self.markSeriesComboBox.currentText()
        if selected_mark_series == "Select mark series":
            self.clear_all_combo_boxes(
                except_boxes=["manufacturer", "model", "engine_size", "mark_series"]
            )
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
        """Updates the position combo box based on the selected drive type."""
        self.clear_combo_box(self.positionComboBox, "Select position")
        selected_manufacturer = self.manufacturerComboBox.currentText()
        selected_model = self.modelComboBox.currentText()
        selected_engine_size = self.engineSizeComboBox.currentText()
        selected_mark_series = self.markSeriesComboBox.currentText()
        selected_drive_type = self.driveTypeComboBox.currentText()
        if selected_drive_type == "Select drive type":
            self.clear_all_combo_boxes(
                except_boxes=[
                    "manufacturer",
                    "model",
                    "engine_size",
                    "mark_series",
                    "drive_type",
                ]
            )
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
        """Updates the transmission combo box based on the selected position."""
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
        """Clears the given combo box and sets a placeholder item."""
        combo_box.clear()
        combo_box.addItem(placeholder)

    def clear_all_combo_boxes(self, except_boxes=None):
        """Clears all combo boxes except those specified."""
        if except_boxes is None:
            except_boxes = []
        if "model" not in except_boxes:
            self.clear_combo_box(self.modelComboBox, "Select model")
        if "engine_size" not in except_boxes:
            self.clear_combo_box(self.engineSizeComboBox, "Select engine size")
        if "mark_series" not in except_boxes:
            self.clear_combo_box(self.markSeriesComboBox, "Select mark series")
        if "drive_type" not in except_boxes:
            self.clear_combo_box(self.driveTypeComboBox, "Select drive type")
        if "position" not in except_boxes:
            self.clear_combo_box(self.positionComboBox, "Select position")
        if "transmission" not in except_boxes:
            self.clear_combo_box(self.transmissionComboBox, "Select transmission")

    def reset_dropdowns(self):
        """Resets all dropdowns to their initial state and repopulates manufacturers."""
        self.clear_all_combo_boxes()
        self.clear_combo_box(self.manufacturerComboBox, "Select manufacturer")
        self.populate_manufacturers()

        # Clear the results layout
        self.clear_results()

    def clear_results(self):
        """Clears the results area in the UI."""
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
        """Searches for parts based on selected criteria and displays the results."""
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
        """Displays the search results in the results area."""
        self.clear_results()
        layout = self.resultsLayout

        row = 0
        col = 0
        max_columns = 4  # Change the number of columns to 4

        card_width = 250
        card_height = 350

        for part in parts:
            part_number, part_size, mod_ind = part

            # Create a layout to hold the text and image
            part_layout = QVBoxLayout()

            # Display the part number with larger font size
            part_number_label = QLabel(f"<b>{part_number}</b>")
            part_number_label.setAlignment(Qt.AlignCenter)
            part_number_label.setStyleSheet(
                "font-size: 16px; padding: 5px;"
            )  # Adjust font size and padding
            part_layout.addWidget(part_number_label)

            # Display the part size on multiple lines
            part_size_lines = part_size.split(
                " x "
            )  # Assuming ' x ' is the delimiter in part_size
            part_size_text = "\n".join(part_size_lines)
            part_size_label = QLabel(part_size_text)
            part_size_label.setAlignment(Qt.AlignCenter)
            part_size_label.setStyleSheet("padding: 5px;")  # Add padding
            part_layout.addWidget(part_size_label)

            # Load and display the image
            image_label = QLabel()
            if mod_ind is None:
                image_file = "generic.jpg"  # Use a generic image if ModInd is None
            else:
                image_file = mod_ind

            base_path = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(base_path, "..", "boots-images", image_file)
            if not os.path.exists(image_path):
                image_path = os.path.join(
                    base_path, "..", "boots-images", "generic.jpg"
                )

            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(
                150, 150, Qt.KeepAspectRatio
            )  # Adjust the size as needed
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.mousePressEvent = (
                lambda event, path=image_path: self.show_image_modal(path)
            )
            part_layout.addWidget(image_label)

            # Create a widget to hold the part layout and add it to the grid layout
            part_widget = QWidget()
            part_widget.setLayout(part_layout)
            part_widget.setFixedSize(card_width, card_height)  # Set fixed size
            part_widget.setStyleSheet(
                """
                background-color: #E74C3C;  /* Orange/red background */
                color: #FFFFFF;  /* White text */
                padding: 10px;
                border-radius: 10px;  /* Rounded corners */
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);  /* Shadow effect */
            """
            )
            layout.addWidget(
                part_widget, row, col, alignment=Qt.AlignTop | Qt.AlignLeft
            )

            col += 1
            if col >= max_columns:  # Change the number of columns as needed
                col = 0
                row += 1

        self.resultsWidget.setLayout(layout)
        self.resultsWidget.update()
        self.resultsScrollArea.update()

    def show_image_modal(self, image_path):
        """Shows a modal dialog with a larger view of the clicked image."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Image Preview")
        dialog.setModal(True)
        layout = QVBoxLayout()

        pixmap = QPixmap(image_path)
        label = QLabel()
        label.setPixmap(pixmap)
        layout.addWidget(label)

        dialog.setLayout(layout)
        dialog.exec_()
