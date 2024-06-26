import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QTextEdit, 
    QRadioButton, 
    QDateEdit, 
)
from PyQt5.QtCore import QDate

from reports_app.utils import generate_reports
from search_app.utils.utils import format_lots_input
from search_app.utils.workflow import Workflow

class MyDesktopApp(QWidget):
    """Class to define all layout of main user interface application

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        # Create widgets
        self.label_instructions = QLabel('Ingresa los lotes a buscar separados por un ";": ')
        self.radioButton1 = QRadioButton('Buscar Lotes')
        self.radioButton1.setChecked(True)
        self.radioButton2 = QRadioButton('Generar Reportes')

        #TextBox Input
        self.text_input = QTextEdit()
        self.text_input.setFixedSize(300,100)
        self.text_input.setCursor
        self.text_input = self.text_input

        self.start_button = QPushButton('Correr')
        self.start_button.setFixedSize(100,30)
        self.start_button.setGeometry(50, 50, 200, 50)

        self.format_button = QPushButton('Formatear')
        self.format_button.setFixedSize(100,30)

        # Start Date Component
        self.label_start_date = QLabel('Start Date:')
        self.start_dateEdit = QDateEdit()
        self.start_dateEdit.setDate(QDate.currentDate())
        self.start_dateEdit.setCalendarPopup(True)
        self.label_start_date.setEnabled(False)
        self.start_dateEdit.setEnabled(False)

        # End Date Component
        self.label_end_date = QLabel('End Date:')
        self.end_dateEdit = QDateEdit()
        self.end_dateEdit.setDate(QDate.currentDate())
        self.end_dateEdit.setCalendarPopup(True)
        self.label_end_date.setEnabled(False)
        self.end_dateEdit.setEnabled(False)

        # Connect the button click event to the method
        self.start_button.clicked.connect(self._on_start_button_click)
        self.format_button.clicked.connect(self._on_format_button_click)

        # Connect a slot to handle radio button change
        self.radioButton1.toggled.connect(self._check_radioButtons_state)
        self.radioButton2.toggled.connect(self._check_radioButtons_state)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_instructions)
        layout.addWidget(self.text_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.format_button)
        layout.addWidget(self.radioButton1)
        layout.addWidget(self.radioButton2)
        layout.addWidget(self.label_start_date)
        layout.addWidget(self.start_dateEdit)
        layout.addWidget(self.label_end_date)
        layout.addWidget(self.end_dateEdit)

        # Set the layout for the main window
        self.setLayout(layout)

    def _on_start_button_click(self):
        """Starts the workflow to search for lots in the specific paths of ICOS and Vitrox equipments."""
        Workflow.flow(self)
        if self.radioButton1.isChecked():
            print('Inicia Buscando Lotes...')
        else: 
            print('Inicia Generando Reportes...')
            
        start_date = self.start_dateEdit.date()
        end_date = self.end_dateEdit.date()
        generate_reports(start_date,end_date)


    def _on_format_button_click(self):
        format_lots_input(self)

    def _check_radioButtons_state(self):
        if self.radioButton1.isChecked():
            print("Modo Activado: Buscar Lotes")
            self._update_gui(True)
        
        elif self.radioButton2.isChecked():
            print("Modo Activado: Generar Reportes")
            self._update_gui(False)

    def _update_gui(self, bool):
        """Updates user interfaces according to the function that will perform.

        Args:
            bool (_type_): _description_
        """
        if bool:
            self.text_input.setEnabled(True)
            self.label_instructions.setEnabled(True)
            self.format_button.setEnabled(True)

            self.label_start_date.setEnabled(False)
            self.start_dateEdit.setEnabled(False)
            self.label_end_date.setEnabled(False)
            self.end_dateEdit.setEnabled(False)

        else:
            self.text_input.setEnabled(False)
            self.label_instructions.setEnabled(False)
            self.format_button.setEnabled(False)
            
            self.label_start_date.setEnabled(True)
            self.start_dateEdit.setEnabled(True)
            self.label_end_date.setEnabled(True)
            self.end_dateEdit.setEnabled(True)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MyDesktopApp()
        window.setWindowTitle('AOI App')
        window.show()
        sys.exit(app.exec_())

    finally: 
        pass

