import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
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
