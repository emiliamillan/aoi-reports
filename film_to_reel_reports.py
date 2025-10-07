from datetime import datetime
import os
from pathlib import Path
import subprocess
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk
import io


PATHS_TO_SEARCH = [
    #'\\\\mexhome03\\Data\\MC Back End\\Generic\\Molding and Singulation\\Emilia M\\mi28 reportes'
    Path.cwd() / 'in_reports' / 'Mi02', # Local tests
    ]


VISION_COLUMNS = [
    'LOT', 'FROM', 
    #Lot Summary
    #remover -- for correct data matrix, -- is only foe lot summary correct data
    '-','Input Wafer Total','Rejected Dice','Tape & Reel B Total','Reject Tray Total',
    
    # Input Wafer Vision Yield
    'Passed','Empty Failed','Others Failed','Angle Failed','Pitch Failed','Chip Failed',
    'Contamination Failed''Crack Failed','Bump Failed','Pad Failed','Probe Mark Failed', '-','TOTAL', 

    # Die Position 1 Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','TOTAL',

    #Die Position 2 Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','TOTAL',

    #Die Position 3 Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','TOTAL',

    #Die Position 4 Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','TOTAL',

    #Die Position 5 Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','TOTAL',

    #Bump Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','Die Sawn Failed','Chip In Failed',
    'Chip Out Failed','Contamination Failed','Crack Failed','Die Size Failed','SubROI Failed','Spec Failed',
    'Bump Failed','Pad Failed','TOTAL',

    #5S Sidewall Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','Chip Failed','Contamination Failed',
    'Crack Failed','Bump Failed','TOTAL',

    #Pocket Position B Vision Yield
    '-','Passed','Others Failed','TOTAL',

    #In Pocket B Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','Chip In Failed','Chip Out Failed',
    'Contamination Failed','Crack Failed','Adhesive Failed','Edge Failed','Die Size Failed',
    'SubROI Failed','Marking Failed','Orientation Failed','No Mark Failed','2D Code Failed',
    'Copper Exposed Failed','TOTAL',

    #Post Seal B Vision Yield
    '-','Empty Failed','Others Failed','Angle Failed','Chip Failed','Crack Failed','Contamination Failed',
    'Marking Failed','Top Layer Seal Broken','Bottom Layer Seal Broken','Both Layer Seal Broken',
    'Top Layer Seal Limit Exceeded','Bottom Layer Seal Limit Exceeded','Both Layer Seal Limit Exceeded',
    'Top Layer Seal Width Inconsistency','Bottom Layer Seal Width Inconsistency',
    'Both Layer Seal Width Inconsistency','Relative Seal Width Inconsistency','TOTAL',

    #TopVision Vision Yield
    '-','Passed','Empty Failed','Others Failed','Chip Failed','Contamination Failed','Crack Failed',
    'Marking Failed','Discolouration Failed','Die Size Failed','TOTAL',

    #3D Vision Yield
    '-','Passed','Empty Failed','Others Failed','Bump Height Failed','Warpage Failed','Slanted Failed','TOTAL',

    #Infrared Ray Vision Yield
    '-','Passed','Empty Failed','Others Failed','Angle Failed','Chip Failed','Contamination Failed','Crack Failed',
    'Marking Failed','Delamination','TOTAL',

    #Reels 
    'Reel 1', 'Count 1', 'Reel 2', 'Count 2',
    ]

OUTPUT_COLUMNS = [
    "Lot", "Equip ID", "Date", 
    "Qty Insp DP1", "Total Reject", "Yield", # Lot summary 
    "Tape & Reel B Total", "Reel 1", "Reel 2", "Reel 3", 
    
    "Passed", "Empty Failed", "Others Failed", "Angle Failed", "TOTAL",	# Die Position 1 Vision Yield
    "Passed", "Empty Failed", "Others Failed", "Angle Failed", "TOTAL",	# Die Position 2 Vision Yield
    "Passed", "Empty Failed", "Others Failed", "Angle Failed", "TOTAL",	# Die Position 3 Vision Yield
    "Passed", "Empty Failed", "Others Failed", "Angle Failed", "TOTAL",	# Die Position 4 Vision Yield
    "Passed", "Empty Failed", "Others Failed", "Angle Failed", "TOTAL",	# Die Position 5 Vision Yield
    
    #Bump Vision Yield
    'Passed', 'Empty Failed', 'Others Failed','Angle Failed','Die Sawn Failed','Chip In Failed','Chip Out Failed',
    'Contamination Failed', 'Crack Failed','Die Size Failed','SubROI Failed','Spec Failed','Bump Failed',
    'Pad Failed','TOTAL',

    # 5S Sidewall Vision Yield
    'Passed','Empty Failed','Others Failed','Angle Failed','Chip Failed','Contamination Failed','Crack Failed',
    'Bump Failed','TOTAL',

    # Pocket Position B Vision Yield
    'Passed','Others Failed','TOTAL',

    #In Pocket B Vision Yield
    'Passed','Empty Failed','Others Failed','Angle Failed','Chip In Failed','Chip Out Failed',
    'Contamination Failed','Crack Failed','Adhesive Failed','Edge Failed','Die Size Failed','SubROI Failed',
    'Marking Failed','Orientation Failed','No Mark Failed','2D Code Failed','Copper Exposed Failed','TOTAL',

    # Post Seal B Vision Yield
    'Empty Failed','Others Failed','Angle Failed','Chip Failed','Crack Failed','Contamination Failed',
    'Marking Failed', 'Top Layer Seal Broken', 'Bottom Layer Seal Broken','Both Layer Seal Broken',
    'Top Layer Seal Limit Exceeded','Bottom Layer Seal Limit Exceeded','Both Layer Seal Limit Exceeded',
    'Top Layer Seal Width Inconsistency','Bottom Layer Seal Width Inconsistency',
    'Both Layer Seal Width Inconsistency','Relative Seal Width Inconsistency','TOTAL',

    # TopVision Vision Yield
    'Passed','Empty Failed','Others Failed','Chip Failed','Contamination Failed',
    'Crack Failed','Marking Failed','Discolouration Failed','Copper Exposed Failed','TOTAL',

    # 3D Vision Yield
    'Passed','Empty Failed','Others Failed','Bump Height Failed','Warpage Failed','Slanted Failed','TOTAL',

    # Infrared Ray Vision Yield
    'Passed','Empty Failed','Others Failed','Angle Failed','Chip Failed','Contamination Failed',
    'Crack Failed','Marking Failed','Delamination','TOTAL',
]

FIRST_COL_NAMES = [ "Lot Summary","Input Wafer Vision Yield", "Die Position 1 Vision Yield", "Die Position 2 Vision Yield", 
    "Die Position 3 Vision Yield", "Die Position 4 Vision Yield", "Die Position 5 Vision Yield", "Bump Vision Yield", 
    "5S Sidewall Vision Yield", "Pocket Position B Vision Yield", "In Pocket B Vision Yield", "Post Seal B Vision Yield", "TopVision Vision Yield",
    "3D Vision Yield", "Infrared Ray Vision Yield"
]

TABLE_NAMES = [
    "Tape & Reel - Reel A Summary", "Wafer Information", "Alarm List", ""
]

def split_csv_by_empty_rows(file_path):
    """Split CSV with multiple tables separated by empty rows"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split by double newlines (empty rows)
        table_sections = content.split('\n\n')
        
        dataframes = []
        for i, section in enumerate(table_sections):
            if section.strip():  # Skip empty sections
                try:
                    if i == 0: # First Table
                        report_info = section.strip().split('\n')[:3]
                        df = pd.read_csv(io.StringIO(section), 
                            sep=',',
                            skiprows=3,
                            engine='python',        # More flexible than C engine
                            on_bad_lines='skip',    # Skip problematic lines
                            dtype=str,              # Read everything as strings first
                            header=None)
                    if section.split('\n')[0] in TABLE_NAMES: # Tables with name
                        df = pd.read_csv(io.StringIO(section), 
                            sep=',',
                            skiprows=1,
                            engine='python',        
                            on_bad_lines='skip',    
                            dtype=str,              
                            header=0)
                    if section.split(',')[0] in FIRST_COL_NAMES: # Tables with different first col name
                        df = pd.read_csv(io.StringIO(section), 
                            sep=',',
                            engine='python',        
                            on_bad_lines='skip',    
                            dtype=str,              
                            header=0)
                    if not df.empty:
                        dataframes.append(df)
                    print(df.head())
                except Exception as e:
                    print(f"Error processing section {i}: {e}")
                    continue
        
        print(f"Extracted {len(dataframes)} tables from {file_path}")
        return dataframes
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

# Function to read text files and extract values
def process_csv_file(file_path) -> pd.DataFrame:
    with open(file_path, 'r', encoding = 'utf-8') as file:
        content = file.read()

    #turn csv into dataframe
    boundary1 = "Alarm Type Selection,Failure"
    index1 = content.find(boundary1)
    section1 = content[:index1]
    #LOT
    wanted1 = re.findall(r'-\s(\w+.?\w+)\s-', section1)
    #FROM
    wanted2 = re.findall(r'\d{1,2}\/\d{1,2}\/\d{4}\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M.*$', section1)

    holder = pd.Series(wanted1)
    holder2 = pd.Series(wanted2)
    
    #Rest of columns
    ## use #boundary2 = "Input Wafer Vision Yield,Quantity,Yield (%),Overall Yield (%)" for correct data info
    boundary2 = "Input Wafer Vision Yield,Quantity,Yield (%),Overall Yield (%)"

     ## use #boundary2 for onlu lot summary correct data
    ##boundary2 = " ,Quantity,Overall Yield,Previous Lot Dice"
    index2 = content.find(boundary2)
    section2 = content[index2:]


    initial = pd.read_csv(io.StringIO(section2))
    #print(initial)
    filtered = initial.iloc[:, 1:2]
    #print(filtered)
    rotated = filtered.T.reset_index(drop=True)
    #print(rotated)
    semifinal = pd.concat([holder, holder2, rotated], ignore_index=True, axis=1)
    semifinal = pd.DataFrame(semifinal)
    #print(semifinal)
    return semifinal

def get_last_modified_time(file_path):
    try:
        modification_time = os.path.getmtime(file_path)
        # Convert the timestamp to a datetime object
        last_modified_datetime = datetime.fromtimestamp(modification_time)
        return last_modified_datetime.date()
    except FileNotFoundError:
        return None

def main(start_date: datetime.date, end_date: datetime.date) -> str | None:
    print('Starting Film2Reel App...')
    print('By: Emilia Millan ')
    print('October, 2025')

    list_files = list()
    
    #Select files we will process, only .txt files within the range dates
    print('Retrieving files from paths...')
    for path in PATHS_TO_SEARCH:
        os.walk(path)
        for filename in os.listdir(path):
            if 'csv' not in filename.split(".")[-1]:
                continue
            file_path = os.path.join(path, filename)
            last_modified_time = get_last_modified_time(file_path)
            if start_date <= last_modified_time <= end_date:
                list_files.append(file_path)

    print('Generating report...')
    all_dataframes = []  # Store all dataframes from all files
    
    if not list_files:
        print("No files found in the specified date range.")
        return None, 0
    
    for file in list_files:
        try:
            print(f"Processing file: {file}")
            file_path = Path(file)
            
            # Use split_csv_by_empty_rows to get all tables from this file
            tables_from_file = split_csv_by_empty_rows(file_path)
            
            if tables_from_file:
                print(f"Found {len(tables_from_file)} tables in {file_path.name}")
                
                # Process each table from this file
                for i, table_df in enumerate(tables_from_file):
                    print(f"  Table {i+1}: {table_df.shape} (rows × columns)")
                    print(f"  Columns: {list(table_df.columns)}")
                    
                    # Add source info to the dataframe
                    table_df = table_df.copy()
                    table_df['source_file'] = file_path.name
                    table_df['table_number'] = i + 1
                    
                    all_dataframes.append(table_df)
            else:
                print(f"No valid tables found in {file_path.name}")
                        
        except Exception as e:
            print(f"There was an error while processing {file}. Don't worry, will not include that file.") 
            print(f"Error is {e}") 
            continue 
    
    # Check if we have any data to export
    if df is None or df.empty:
        print("No data to export. Check your date range or file contents.")
        return None, len(list_files)
    
    #remove whitespaces
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)    

    #Export dataframe
    output_dir = Path.cwd() / 'report_app_MI-28'
    output_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    
    new_filename = output_dir / f'report_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv'
    
    # Only apply column headers if we have the expected structure
    try:
        if len(df.columns) >= 147:
            num = 147
            col_names = df.columns.to_list()
            df.columns = VISION_COLUMNS[:num-1] + col_names[num-1:]
            
            # Data cleaning
            df = df.iloc[:, :num-1]
            df = df.drop(columns=[col for col in df.columns if col == '-'], errors='ignore')
    except Exception as e:
        print(f"Warning: Could not apply standard column headers: {e}")
    
    print("Data preview:")
    print(df.head())
    print(f"Data shape: {df.shape}")
    
    df.to_csv(new_filename, index=False)
    print(f'Created at: {new_filename}')
    
    try:
        subprocess.Popen(['start', 'excel', str(new_filename)], shell=True)
    except Exception as e:
        print(f"Could not open Excel: {e}")
    
    return str(new_filename), len(list_files)

#if __name__ == '__main__':
    #Enter your dates here
    
    start_date = datetime.strptime('2025-06-15', "%Y-%m-%d").date()
    end_date = datetime.strptime('2025-06-20', "%Y-%m-%d").date()
    try:
        path, file_count= main(start_date, end_date) 
        print(f'Report created. Located at: {path}')  
        print(f'Included {file_count} files in the report')  
    except Exception as e:
        print("Hubo un error. Corre de nuevo la app.", e)
    
root = tk.Tk()
root.geometry('300x200')
root.title('Reporte MI-28')

name_label = ttk.Label(root, text='Start Date (yyyy-mm-dd):')
name_label.pack(pady=2)

start_entry = ttk.Entry(root)
start_entry.insert(0, '2025-10-05')
start_entry.pack(pady=5)
start_entry.focus()

date_label = ttk.Label(root, text='End Date (yyyy-mm-dd):')
date_label.pack(pady=2)

end_entry = ttk.Entry(root)
end_entry.insert(0, '2025-10-07')
end_entry.pack(pady=5)

def entryhandler():
        start, end = start_entry.get(), end_entry.get()
        main(datetime.strptime(start, "%Y-%m-%d").date(), datetime.strptime(end, "%Y-%m-%d").date())

run_button = ttk.Button(
    root,
    text='Run',
    command=lambda: entryhandler()
)

run_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

root.mainloop()