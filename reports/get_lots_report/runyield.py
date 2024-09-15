from datetime import datetime
import os
from pathlib import Path
import pandas as pd

PATHS_TO_SEARCH = [
    '\\\\mex6vtrx01\\Texas\\Report\\ICPLUS',
    '\\\\mex6vtrx02\\Texas\\Report\\ICPLUS',
    ]

# Initialize an empty DataFrame to store the extracted data
COLUMNS = ['Lot', 
           'Vitrox ID',
           'Recipe',
           'Start Time',
           'End Time',
           'Yield', 
           'Total Inspected', 
           'Total Reject']  # Cause of defect

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
        if 'START TIME' in row: #a
            start = row.find(':', 50)+2
            value = row[start: len(row)]
            dictionary["Start Time"] = value
            #print(value)
        if 'END TIME' in row: #a
            start = row.find(':', 50)+2
            value = row[start: len(row)]
            dictionary["End Time"] = value
            #print(value)            
        if 'RECIPE' in row: #b
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
        if 'TOTAL INSPECTED' in row: #b
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Total Inspected"] = value
            #print(value)
        if 'TOTAL REJECT' in row: #b
            start = row.find(':')+2 
            end = row.find('    ',25)
            value = row[start:end]
            dictionary["Total Reject"] = value
            #print(value)
    dictionary["File Name"]= os.path.basename(file_path)
    return dictionary

def get_last_modified_time(file_path):
    try:
        modification_time = os.path.getmtime(file_path)
        # Convert the timestamp to a datetime object
        last_modified_datetime = datetime.fromtimestamp(modification_time)
        return last_modified_datetime.date()
    except FileNotFoundError:
        return None

def main(start_date: datetime.date, end_date: datetime.date) -> str | None:
    print('Starting Report App... ')
    print('By: Emilia Millan ')
    list_files = list()
    
    #Select files we will process, only .txt files within the range dates
    for path in PATHS_TO_SEARCH:
        os.walk(path)
        for filename in os.listdir(path):
            if 'txt' not in filename.split(".")[-1]:
                continue
            file_path = os.path.join(path, filename)
            last_modified_time = get_last_modified_time(file_path)
            if start_date <= last_modified_time <= end_date:
                list_files.append(file_path)
        #---- DEBUG PURPOSES, DON´T REVOVE ----
            #if len(list_files) == 2:
            #    break
        #break
        #--------------------------------------

    print('Generating report...')
    df = None
    for file in list_files:
        file = Path(file)
        try:
            dictionary = process_text_file(file)
            if df is None: 
                df = pd.DataFrame(dictionary, columns=COLUMNS, index=[0])
            else: 
                new_df = pd.DataFrame(dictionary, columns=COLUMNS, index=[0])
                df = pd.concat([df,new_df], ignore_index=True)
        except Exception as e:
            print(f"There was an error while processing {file}. Don't worry, will not include that file.") 
            print(f"Error is {e}" ) 
            continue

    #remove whitespaces
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)    

    #Export dataframe
    new_filename = os.path.join(os.getcwd(),'report_app', f'report_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv')
    df.to_csv(new_filename, index=False)
    return new_filename, len(list_files)

if __name__ == '__main__':
    #Enter your dates here
    start_date = datetime.strptime('2024-04-02', "%Y-%m-%d").date()
    end_date = datetime.strptime('2024-04-08', "%Y-%m-%d").date()
    try:
        path, file_count= main(start_date, end_date) 
        print(f'Report created. Located at: {path}')  
        print(f'Included {file_count} files in the report')  
    except Exception as e:
        print("Hubo un error. Corre de nuevo la app.", e)