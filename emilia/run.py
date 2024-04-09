import os
import pandas as pd

# Define the paths where your text files are located
VTRX1 = '//mex6vtrx01/Texas/Report/ICPLUS'
VTRX2 = '//mex6vtrx02/Texas/Report/ICPLUS'

# Initialize an empty DataFrame to store the extracted data
COLUMNS = ['Lot', 
           'Vitrox ID',
           'Th ID',
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
           'Tablero despostilla',
           'Residuo metalico-80',
           'Residuo metalico-80',
           'Mark Invalid Device',
           'Pin1',
           'Despostillado-84',
           'Contaminacion-93',
           'Marking 1',
           'Pin1',]  # Cause of defect

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
            #print(value)
            dictionary["recipe"] = value
        if 'MACHINE' in row:
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end].split(' | ')
            dictionary["Vitrox ID"] = value[0]
            dictionary["Th ID"] = value[1]
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
    
    dictionary["File Name"]= os.path.basename(file_path)
    #print(dictionary)
    return dictionary
    
def main():
    pass


if __name__ == '__main__':
    dictionary = process_text_file('emilia/4756640.1.txt')
    df = pd.DataFrame(dictionary,columns=COLUMNS, index=[0])
    
    print(df.columns)
    #Export it
    df.to_csv('output.csv', index=False)
    print(df)
