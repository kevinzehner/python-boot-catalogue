import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox
from PyQt5 import uic

# Suppress macOS warning about secure coding
os.environ['QT_MAC_WANTS_LAYER'] = '1'

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

        # Find the QComboBox by its objectName set in Qt Designer
        self.manufacturerComboBox = self.findChild(QComboBox, "manufacturerComboBox")

        # Debugging: Print to check if the QComboBox is found
        print(f"manufacturerComboBox: {self.manufacturerComboBox}")

        # Populate the QComboBox with unique manufacturers from the database
        self.populateManufacturers()

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

# Check if the script is run directly (not imported as a module)
if __name__ == "__main__":
    # Create an instance of the QApplication
    app = QApplication(sys.argv)

    # Create an instance of the MainWindow
    window = MainWindow()

    # Show the main window
    window.show()

    # Start the application's event loop
    sys.exit(app.exec_())