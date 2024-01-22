import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit

from utils import format_lots_input
from workflow import Workflow, start_process



class MyDesktopApp(QWidget):
    """Class to define all layout of main user interface application

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self):
        super().__init__()

        # Create widgets
        self.label_instructions = QLabel('Ingresa los lotes a buscar separados por un ";": ')
        
        #TextBox Input
        self.text_input = QTextEdit()
        self.text_input.setFixedSize(300,100)
        self.text_input.setCursor
        self.text_input = self.text_input

        self.start_button = QPushButton('Buscar')
        self.start_button.setFixedSize(100,30)
        self.start_button.setGeometry(50, 50, 200, 50)

        self.format_button = QPushButton('Formatear')
        self.format_button.setFixedSize(100,30)

        # Connect the button click event to the method
        self.start_button.clicked.connect(self.on_start_button_click)
        self.format_button.clicked.connect(self.on_format_button_click)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_instructions)
        layout.addWidget(self.text_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.format_button)

        # Set the layout for the main window
        self.setLayout(layout)

    def on_start_button_click(self):
        """Starts the workflow to search for lots in the specific paths of ICOS and Vitrox.
        """
        Workflow.flow(self)

    def on_format_button_click(self):
        
        self.text_input.setPlainText(format_lots_input(self.text_input.toPlainText()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyDesktopApp()
    window.setWindowTitle('AOI Lots Searcher')
    window.show()
    sys.exit(app.exec_())
