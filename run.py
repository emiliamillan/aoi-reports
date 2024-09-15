import sys
from PyQt5.QtWidgets import (
    QApplication, 
)
from view.app import App

def start_app():
        app = QApplication(sys.argv)
        window = App()
        window.setWindowTitle('AOI App')
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        start_app()
    finally: 
        pass