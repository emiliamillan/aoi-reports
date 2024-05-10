import sys
from PyQt5.QtWidgets import (
    QApplication, 
)
from gui.my_desktop_app import MyDesktopApp

def start_app():
        app = QApplication(sys.argv)
        window = MyDesktopApp()
        window.setWindowTitle('AOI App')
        window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    try:
        start_app()
    finally: 
        pass