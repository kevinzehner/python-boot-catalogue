import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow 

if __name__ == "__main__":
    # Create indexes (if they don't exist)
    from create_indexes import create_indexes

    create_indexes("boots.db")

    # Start the application
    app = QApplication(sys.argv)
    
    # Apply the stylesheet
    try:
        with open("style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except Exception as e:
        print(f"Error loading stylesheet: {e}")

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
