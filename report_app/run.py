from datetime import datetime
import os
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit

PATHS_TO_SEARCH = [
    '//mex6vtrx01/Texas/Report/ICPLUS',
    '//mex6vtrx02/Texas/Report/ICPLUS',
    ]

# Initialize an empty DataFrame to store the extracted data
COLUMNS = ['Lot', 
           'Vitrox ID',
           'Recipe',
           'Yield', 
           'Total Inspected', 
           'Total Reject', 
           'Invalid',
           'Rayon en el pad-NE',
           'Contam. en pad-93',
           'Contam en pad 93 C',
           'BX',
           'BY',
           'Contaminacion metal',
           'Tablero despostillado',
           'Residuo metalico-80',
           'Mark Invalid Device',
           'Pin1',
           'Despostillado-84',
           'Contaminacion-93',
           'Marking 1',]  # Cause of defect

# Function to read text files and extract values
def process_text_file(file_path) -> dict:
    with open(file_path, 'r') as file:
        content = file.read()
    
    #split file by rows
    content = content.split('\n')

    #Extract the needed fields
    dictionary = dict()
    for row in content:
        start, end = "",""
        if 'LOT' in row and '.LOT' not in row:
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Lot"] = value
            #print(value)
        if 'START TIME' in row: 
            start = row.find(':', 50)+2
            value = row[start: len(row)]
            dictionary["start_time"] = value
            #print(value)
        if 'RECIPE' in row: 
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Recipe"] = value
            #print(value)
        if 'MACHINE' in row:
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end].split(' | ')
            dictionary["Vitrox ID"] = value[0]
            #print(value)
        if 'Total Yield' in row:
            start = row.find(':', 45)+2
            value = row[start: len(row)]
            dictionary["Yield"] = value
            #print(value)
        if 'TOTAL INSPECTED' in row:
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Total Inspected"] = value
            #print(value)
        if 'TOTAL REJECT' in row:
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Total Rejected"] = value
            #print(value)
        
        # DEFECTS    
        if 'Invalid      ' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Invalid"] = value
            #print(value)
        if 'Rayon en el pad-NE' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Rayon en el pad-NE"] = value
            #print(value)
        if 'Contam. en pad-93' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Contam en pad-93"] = value
            #print(value)
        if 'Contam. en pad-93' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Contam en pad-93"] = value
            #print(value)
        if 'BX' in row and 'micron' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["BX"] = value
            #print(value)
        if 'BY' in row and 'micron' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["BY"] = value
            #print(value)
        if 'Contaminacion metalica-90' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Contaminacion metalica"] = value
            #print(value)
        if 'Tablero despostillado-84' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Tablero despostillado"] = value
            #print(value)
        if 'Residuo metalico-80' in row and 'edge' not in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Tablero despostillado"] = value
            #print(value)
        if 'Mark Invalid Device' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Mark Invalid Device"] = value
            #print(value)
        if 'Pin1' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Pin1"] = value
            #print(value)
        if 'Despostillado-84' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Despostillado-84"] = value
            #print(value)
        if 'Contaminacion-93' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Contaminacion-93"] = value
            #print(value)
        if 'Marking 1' in row: 
            start = row.find('  ',len(row)-10) 
            value = row[start:len(row)]
            dictionary["Marking 1"] = value
            print(value)
    
    dictionary["File Name"]= os.path.basename(file_path)
    #print(dictionary)
    return dictionary


def format_lots_input(self: QTextEdit):
    text = self.text_input.toPlainText().replace("\n", ";")
    self.text_input.setPlainText(text)

class ReportApp(QWidget):
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

        self.start_button = QPushButton('Generar Reporte')
        self.start_button.setFixedSize(125,30)
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
        pass

    def on_format_button_click(self):
        format_lots_input(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReportApp()
    window.setWindowTitle('Report App')
    window.show()
    sys.exit(app.exec_())

    # Define the time range
    start_date_str = '2024-03-01'
    end_date_str = '2024-03-07'

    # Convert start and end dates to Unix timestamps
    start_date = int(datetime.strptime(start_date_str, '%Y-%m-%d').timestamp())
    end_date = int(datetime.strptime(end_date_str, '%Y-%m-%d').timestamp())
    print(start_date)
    print(end_date)
    
    ###
    dictionary = process_text_file('emilia/4756640.1.txt')

    df = pd.DataFrame(dictionary,columns=COLUMNS, index=[0])
    
    #remove whitespaces
    #df = df.map(lambda x: x.strip() if isinstance(x, str) else x)    
    
    #Export dataframe
    df.to_csv('output.csv', index=False)