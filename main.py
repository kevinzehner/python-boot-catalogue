import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow  # Ensure you're importing the correct MainWindow class

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    # Apply the stylesheet
    with open("style.qss", "r") as style_file:
        style_content = style_file.read()
        print(style_content)  # Debug statement to print the content of the stylesheet
        app.setStyleSheet(style_content)

    window.show()
    sys.exit(app.exec_())
