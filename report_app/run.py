from datetime import datetime
import os
import pandas as pd

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

def find_dates_within_range(date_list, start_date, end_date):
    # Convert start_date and end_date to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Convert date_list elements to datetime objects
    date_list = [datetime.strptime(date, "%Y-%m-%d") for date in date_list]

    # Filter dates within the range
    dates_within_range = [date for date in date_list if start_date <= date <= end_date]

    return dates_within_range

if __name__ == '__main__':
    # Define the time range
    start_date_str = '2024-03-01'
    end_date_str = '2024-03-07'

    # Example usage
    dates = ['2022-01-01', '2022-01-05', '2022-01-10', '2022-01-15', '2022-01-20']
    start_date = '2022-01-03'
    end_date = '2022-01-15'

    dates_within_range = find_dates_within_range(dates, start_date, end_date)
    print("Dates within the range:", dates_within_range)    
    raise
    ###
    dictionary = process_text_file('emilia/4756640.1.txt')

    df = pd.DataFrame(dictionary,columns=COLUMNS, index=[0])
    
    #remove whitespaces
    #df = df.map(lambda x: x.strip() if isinstance(x, str) else x)    
    
    #Export dataframe
    df.to_csv('output.csv', index=False)