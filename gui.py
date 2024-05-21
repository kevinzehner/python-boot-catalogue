import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox
from PyQt5 import uic

# Define a class that inherits from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        # Call the parent class (QMainWindow) constructor
        super(MainWindow, self).__init__()

        # Load the UI file created with Qt Designer
        uic.loadUi("main_window.ui", self)

        # Call the method to initialize additional UI components
        self.initializeUI()

    def initializeUI(self):
        # Find the QLabel widget by its objectName set in Qt Designer
        self.messageLabel = self.findChild(QLabel, "messageLabel")


        self.messageLabel.setText("Wheel Bearing Catalogue")

        # Find the QComboBox widgets by their objectNames set in Qt Designer
        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")
        self.engineSizeComboBox = self.findChild(QComboBox, "engineSizeComboBox")
        self.markSeriesComboBox = self.findChild(QComboBox, "markSeriesComboBox")
        self.driveTypeComboBox = self.findChild(QComboBox, "driveTypeComboBox")
        self.positionComboBox = self.findChild(QComboBox, "positionComboBox")

        # Set placeholders for the combo boxes
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

        # Populate the manufacturerComboBox with unique manufacturers from the database
        self.populateManufacturers()

        # Connect signals to update the dependent combo boxes
        self.manufacturerComboBox.currentIndexChanged.connect(self.updateModels)
        self.modelComboBox.currentIndexChanged.connect(self.updateEngineSizes)
        self.engineSizeComboBox.currentIndexChanged.connect(self.updateMarkSeries)
        self.markSeriesComboBox.currentIndexChanged.connect(self.updateDriveTypes)
        self.driveTypeComboBox.currentIndexChanged.connect(self.updatePositions)

    def populateManufacturers(self):
        if self.manufacturerComboBox is not None:
            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get unique manufacturers
            cursor.execute("SELECT DISTINCT Manuf FROM wheelbearing")
            manufacturers = [row[0] for row in cursor.fetchall()]

            # Populate the QComboBox with the retrieved manufacturers
            self.manufacturerComboBox.addItems(manufacturers)

            # Close the database connection
            conn.close()
        else:
            print("Error: QComboBox with objectName 'manufacturerComboBox' not found")

    def updateModels(self):
        if self.modelComboBox is not None:
            # Get the selected manufacturer
            selected_manufacturer = self.manufacturerComboBox.currentText()

            if selected_manufacturer == "Select manufacturer":
                self.modelComboBox.clear()
                self.modelComboBox.addItem("Select model")
                self.engineSizeComboBox.clear()
                self.engineSizeComboBox.addItem("Select engine size")
                self.markSeriesComboBox.clear()
                self.markSeriesComboBox.addItem("Select mark series")
                self.driveTypeComboBox.clear()
                self.driveTypeComboBox.addItem("Select drive type")
                self.positionComboBox.clear()
                self.positionComboBox.addItem("Select position")
                return

            # Clear the current items in the modelComboBox
            self.modelComboBox.clear()
            self.modelComboBox.addItem("Select model")

            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get models for the selected manufacturer
            cursor.execute("SELECT DISTINCT Model FROM wheelbearing WHERE Manuf = ?", (selected_manufacturer,))
            models = [row[0] for row in cursor.fetchall()]

            # Populate the modelComboBox with the retrieved models
            self.modelComboBox.addItems(models)

            # Close the database connection
            conn.close()

            # Trigger update for engine sizes
            self.updateEngineSizes()
        else:
            print("Error: QComboBox with objectName 'modelComboBox' not found")

    def updateEngineSizes(self):
        if self.engineSizeComboBox is not None:
            # Get the selected manufacturer and model
            selected_manufacturer = self.manufacturerComboBox.currentText()
            selected_model = self.modelComboBox.currentText()

            if selected_model == "Select model":
                self.engineSizeComboBox.clear()
                self.engineSizeComboBox.addItem("Select engine size")
                self.markSeriesComboBox.clear()
                self.markSeriesComboBox.addItem("Select mark series")
                self.driveTypeComboBox.clear()
                self.driveTypeComboBox.addItem("Select drive type")
                self.positionComboBox.clear()
                self.positionComboBox.addItem("Select position")
                return

            # Clear the current items in the engineSizeComboBox
            self.engineSizeComboBox.clear()
            self.engineSizeComboBox.addItem("Select engine size")

            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get engine sizes for the selected manufacturer and model
            cursor.execute("SELECT DISTINCT EngineSize FROM wheelbearing WHERE Manuf = ? AND Model = ?", 
                           (selected_manufacturer, selected_model))
            engine_sizes = [str(row[0]) for row in cursor.fetchall()]

            # Populate the engineSizeComboBox with the retrieved engine sizes
            self.engineSizeComboBox.addItems(engine_sizes)

            # Close the database connection
            conn.close()

            # Trigger update for mark series
            self.updateMarkSeries()
        else:
            print("Error: QComboBox with objectName 'engineSizeComboBox' not found")

    def updateMarkSeries(self):
        if self.markSeriesComboBox is not None:
            # Get the selected manufacturer, model, and engine size
            selected_manufacturer = self.manufacturerComboBox.currentText()
            selected_model = self.modelComboBox.currentText()
            selected_engine_size = self.engineSizeComboBox.currentText()

            if selected_engine_size == "Select engine size":
                self.markSeriesComboBox.clear()
                self.markSeriesComboBox.addItem("Select mark series")
                self.driveTypeComboBox.clear()
                self.driveTypeComboBox.addItem("Select drive type")
                self.positionComboBox.clear()
                self.positionComboBox.addItem("Select position")
                return

            # Clear the current items in the markSeriesComboBox
            self.markSeriesComboBox.clear()
            self.markSeriesComboBox.addItem("Select mark series")

            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get mark series for the selected manufacturer, model, and engine size
            cursor.execute("SELECT DISTINCT MarkSeries FROM wheelbearing WHERE Manuf = ? AND Model = ? AND EngineSize = ?", 
                           (selected_manufacturer, selected_model, selected_engine_size))
            mark_series = [row[0] for row in cursor.fetchall()]

            # Populate the markSeriesComboBox with the retrieved mark series
            self.markSeriesComboBox.addItems(mark_series)

            # Close the database connection
            conn.close()

            # Trigger update for drive types
            self.updateDriveTypes()
        else:
            print("Error: QComboBox with objectName 'markSeriesComboBox' not found")

    def updateDriveTypes(self):
        if self.driveTypeComboBox is not None:
            # Get the selected manufacturer, model, engine size, and mark series
            selected_manufacturer = self.manufacturerComboBox.currentText()
            selected_model = self.modelComboBox.currentText()
            selected_engine_size = self.engineSizeComboBox.currentText()
            selected_mark_series = self.markSeriesComboBox.currentText()

            if selected_mark_series == "Select mark series":
                self.driveTypeComboBox.clear()
                self.driveTypeComboBox.addItem("Select drive type")
                self.positionComboBox.clear()
                self.positionComboBox.addItem("Select position")
                return

            # Clear the current items in the driveTypeComboBox
            self.driveTypeComboBox.clear()
            self.driveTypeComboBox.addItem("Select drive type")

            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get drive types for the selected manufacturer, model, engine size, and mark series
            cursor.execute("SELECT DISTINCT TransDrive FROM wheelbearing WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND MarkSeries = ?", 
                           (selected_manufacturer, selected_model, selected_engine_size, selected_mark_series))
            drive_types = [row[0] for row in cursor.fetchall()]

            # Populate the driveTypeComboBox with the retrieved drive types
            self.driveTypeComboBox.addItems(drive_types)

            # Close the database connection
            conn.close()

            # Trigger update for positions
            self.updatePositions()
        else:
            print("Error: QComboBox with objectName 'driveTypeComboBox' not found")

    def updatePositions(self):
        if self.positionComboBox is not None:
            # Get the selected manufacturer, model, engine size, mark series, and drive type
            selected_manufacturer = self.manufacturerComboBox.currentText()
            selected_model = self.modelComboBox.currentText()
            selected_engine_size = self.engineSizeComboBox.currentText()
            selected_mark_series = self.markSeriesComboBox.currentText()
            selected_drive_type = self.driveTypeComboBox.currentText()

            if selected_drive_type == "Select drive type":
                self.positionComboBox.clear()
                self.positionComboBox.addItem("Select position")
                return

            # Clear the current items in the positionComboBox
            self.positionComboBox.clear()
            self.positionComboBox.addItem("Select position")

            # Connect to the SQLite database
            conn = sqlite3.connect('wheelbearings.db')
            cursor = conn.cursor()

            # Execute a query to get positions for the selected manufacturer, model, engine size, mark series, and drive type
            cursor.execute("SELECT DISTINCT MPos FROM wheelbearing WHERE Manuf = ? AND Model = ? AND EngineSize = ? AND MarkSeries = ? AND TransDrive = ?", 
                           (selected_manufacturer, selected_model, selected_engine_size, selected_mark_series, selected_drive_type))
            positions = [row[0] for row in cursor.fetchall()]

            # Populate the positionComboBox with the retrieved positions
            self.positionComboBox.addItems(positions)

            # Close the database connection
            conn.close()
        else:
            print("Error: QComboBox with objectName 'positionComboBox' not found")

if __name__ == "__main__":
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow
    window = MainWindow()

    # Show the main window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec_())