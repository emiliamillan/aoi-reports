import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit

from utils import format_lots_input

GLOBAL_PATH = "\\\\mexhome03\\Data\\MC Back End\\Generic\\Molding and Singulation\\AOI REPORTS"

ICOS_PATHS_LIST = [
    "\\\\MEX6ICOS01\\_results\\ascii\\global",
    "\\\\MEX6ICOS02\\_results\\ascii\\global",
    "\\\\MEX6ICOS03\\_results\\ascii\\global",
    "\\\\mex6icos04\\_results\\ascii\\global",
    "\\\\mex6icos05\\_results\\ascii\\global",
    "\\\\mex6icos06\\_results\\ascii\\global",
    "\\\\mex6icos07\\_results\\ascii\\global",
    "\\\\mex6icos08\\_Results\\ascii\\global",
    "\\\\mex6icos09\\_results\\ascii\\global",
    "\\\\mex6icos10\\_results\\ascii\\global",
    "\\\\mex6icos11\\_results\\ascii\\global",
    "\\\\mex6icos12\\_results\\ascii\\global",
    "\\\\mex6icos13\\_results\\ascii\\global",
    "\\\\mex6icos14\\_results\\ascii\\global",
    "\\\\mex6icos15\\_results\\ascii\\global",
    "\\\\mex6icos16\\_results\\ascii\\global"
]

ICOS_VARIANTS_LIST = [
    ".1",
    ".2",
    ".3",
    ".1_R1",
    ".1_R2",
    ".1_R3"
]

VITROX_PATHS_LIST = [
    "\\\\mex6vtrx01\\d\\Texas\\Report\\ICPLUS",
    "\\\\mex6vtrx02\\D\\Texas\\Report\\ICPLUS",
]

VITROX_VARIANTS_LIST = [
    "\\\\mex6vtrx01\\d\\Texas\\Report\\ICPLUS",
    "\\\\mex6vtrx02\\D\\Texas\\Report\\ICPLUS",
]
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
        entered_text = self.text_input.toPlainText()
        self.label_instructions.setText(f'Entered text: {entered_text}')

        lots_input = self.text_input.toPlainText()
        list_of_lots = lots_input.split(";")

        print(type(list_of_lots))
        print(list_of_lots)


    def on_format_button_click(self):
        format_lots_input(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyDesktopApp()
    window.setWindowTitle('AOI Lots Searcher')
    window.show()
    sys.exit(app.exec_())
