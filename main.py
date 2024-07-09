import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow  # Ensure you're importing the correct MainWindow class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Apply the stylesheet
    with open("style.qss", "r") as style_file:
        app.setStyleSheet(style_file.read())

    window.show()
    sys.exit(app.exec_())
