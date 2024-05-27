import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Load and apply the QSS file
    with open("style.qss", "r") as file:
        app.setStyleSheet(file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
