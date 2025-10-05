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
    #"C:\\Users\\millane\\Documents\\F2R_Reports\\Mi02"
    "C:\Users\millane\Documents\aoi-reports\in_reports\Mi02"
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

# Previous Columns
"""
'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'Pitch Failed', 'Chip Failed',
    'Contamination Failed', 'Crack Failed', 'Bump Failed', 'Pad Failed', 'Probe Mark Failed', 'TOTAL',
    'Die Position 1 Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'TOTAL',
    'Die Position 2 Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'TOTAL',
    'Die Position 3 Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'TOTAL',
    'Die Position 4 Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'TOTAL',
    'Die Position 5 Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'TOTAL',
    'Bump Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'Die Sawn Failed',
    'Chip In Failed', 'Chip Out Failed', 'Contamination Failed', 'Crack Failed', 'Die Size Failed',
    'SubROI Failed', 'Spec Failed', 'Bump Failed', 'Pad Failed', 'TOTAL',
    '5S Sidewall Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'Chip Failed',
    'Contamination Failed', 'Crack Failed', 'Bump Failed', 'TOTAL',
    'Pocket Position B Vision Yield', 'Passed', 'Others Failed', 'TOTAL',
    'In Pocket B Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed', 'Chip In Failed',
    'Chip Out Failed', 'Contamination Failed', 'Crack Failed', 'Adhesive Failed', 'Edge Failed',
    'Die Size Failed', 'SubROI Failed', 'Marking Failed', 'Orientation Failed', 'No Mark Failed',
    '2D Code Failed', 'Copper Exposed Failed', 'TOTAL',
    'Post Seal B Vision Yield', 'Empty Failed', 'Others Failed', 'Angle Failed', 'Chip Failed',
    'Crack Failed', 'Contamination Failed', 'Marking Failed', 'Top Layer Seal Broken',
    'Bottom Layer Seal Broken', 'Both Layer Seal Broken', 'Top Layer Seal Limit Exceeded',
    'Bottom Layer Seal Limit Exceeded', 'Both Layer Seal Limit Exceeded',
    'Top Layer Seal Width Inconsistency', 'Bottom Layer Seal Width Inconsistency',
    'Both Layer Seal Width Inconsistency', 'Relative Seal Width Inconsistency', 'TOTAL',
    'TopVision Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Chip Failed',
    'Contamination Failed', 'Crack Failed', 'Marking Failed', 'Discolouration Failed',
    'Die Size Failed', 'TOTAL',
    '3D Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Bump Height Failed',
    'Warpage Failed', 'Slanted Failed', 'TOTAL',
    'Infrared Ray Vision Yield', 'Passed', 'Empty Failed', 'Others Failed', 'Angle Failed',
    'Chip Failed', 'Contamination Failed', 'Crack Failed', 'Marking Failed', 'Delamination', 'TOTAL', 'NAN',
    'Tape & Reel - Reel A Summary', 'Reel No.', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'Total Reel: 3',
    'Wafer Information', 'Wafer ID', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'NAN', 'Total Wafer: 3',
    'Alarm List', 'Frequency', 'NAN', 'NAN', 'NAN', 'NAN'
""" 

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
    print('Starting Report App... ')
    print('By: Emilia Millan ')
    list_files = list()
    
    #Select files we will process, only .txt files within the range dates
    for path in PATHS_TO_SEARCH:
        os.walk(path)
        for filename in os.listdir(path):
            if 'csv' not in filename.split(".")[-1]:
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
            dictionary = process_csv_file(file)
            if df is None: 
                #df = pd.DataFrame(dictionary, columns=COLUMNS, index=[0])
                df = dictionary
            else: 
                #new_df = pd.DataFrame(dictionary, columns=COLUMNS, index=[0])
                new_df = dictionary
                #df = pd.concat([df,new_df], ignore_index=True)
                df = pd.concat([df, new_df], ignore_index=True)
        except Exception as e:
            print(f"There was an error while processing {file}. Don't worry, will not include that file.") 
            print(f"Error is {e}" ) 
            continue

    #remove whitespaces
    #df = df.map(lambda x: x.strip() if isinstance(x, str) else x)    

    #Export dataframe
    new_filename = os.path.join(os.getcwd(),'report_app_MI-28', f'report_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv')
    new_filename = "C:\Users\millane\Documents\aoi-reports\report_app_MI-28\report"
    #df.columns = VISION_COLUMNS

    #Add headers
    num = 147
    col_names = df.columns.to_list()
    df.columns = VISION_COLUMNS[:num-1] + col_names[num-1:]

    # Data cleaning
    df = df.iloc[:, :num-1]
    df = df.drop(columns=[col for col in df.columns if col == '-'])
    
    print(df.head())
    df.to_csv(new_filename, index=False)
    print(f'Created at: {new_filename}')
    subprocess.Popen(['start', 'excel', new_filename], shell=True)
    return new_filename, len(list_files)

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
start_entry.pack(pady=5)
start_entry.focus()

date_label = ttk.Label(root, text='End Date (yyyy-mm-dd):')
date_label.pack(pady=2)

end_entry = ttk.Entry(root)
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