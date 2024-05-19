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

        # Set the text of the QLabel to "Hello Rosie"
        self.messageLabel.setText("Hello Rosie")

        # Find the QComboBox widgets by their objectNames set in Qt Designer
        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")
        self.modelComboBox = self.findChild(QComboBox, "modelComboBox")

        # Populate the manufacturerComboBox with unique manufacturers from the database
        self.populateManufacturers()

        # Connect the signal for manufacturer selection to the update models function
        self.manufacturerComboBox.currentIndexChanged.connect(self.updateModels)

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

            # Clear the current items in the modelComboBox
            self.modelComboBox.clear()

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
        else:
            print("Error: QComboBox with objectName 'modelComboBox' not found")

if __name__ == "__main__":
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow
    window = MainWindow()

    # Show the main window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec_())