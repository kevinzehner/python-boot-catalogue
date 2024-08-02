import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow  # Ensure you're importing the correct MainWindow class

if __name__ == "__main__":
    # Create indexes (if they don't exist)
    from create_indexes import create_indexes

    create_indexes("boots.db")

    # Start the application
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
