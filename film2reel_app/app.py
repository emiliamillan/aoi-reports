from datetime import datetime
from logging import root
import os
from pathlib import Path
import subprocess
import pandas as pd
import tkinter as tk
from tkinter import ttk
import io

PATHS_TO_SEARCH = [
    #'\\\\mexhome03\\Data\\MC Back End\\Generic\\Molding and Singulation\\Emilia M\\mi28 reportes'
    Path.cwd() / 'in_reports' / 'Mi02', # Local tests
    ]

OUTPUT_COLUMNS = [
    ('', 'Lot'),
    ('', 'Equip ID'),
    ('', 'Date'),

    ('Lot Summary', 'Qty Insp DP1'),
    ('Lot Summary', 'Total Reject'),
    ('Lot Summary', 'Yield'),

    ('', 'Tape & Reel B Total'),
    ('', 'Reel 1'),
    ('', 'Reel 2'),
    ('', 'Reel 3'),

    ('Die Position 1 Vision Yield', 'Passed'),
    ('Die Position 1 Vision Yield', 'Empty Failed'),
    ('Die Position 1 Vision Yield', 'Others Failed'),
    ('Die Position 1 Vision Yield', 'Angle Failed'),
    ('Die Position 1 Vision Yield', 'TOTAL'),

    ('Die Position 2 Vision Yield', 'Passed'),
    ('Die Position 2 Vision Yield', 'Empty Failed'),
    ('Die Position 2 Vision Yield', 'Others Failed'),
    ('Die Position 2 Vision Yield', 'Angle Failed'),
    ('Die Position 2 Vision Yield', 'TOTAL'),

    ('Die Position 3 Vision Yield', 'Passed'),
    ('Die Position 3 Vision Yield', 'Empty Failed'),
    ('Die Position 3 Vision Yield', 'Others Failed'),
    ('Die Position 3 Vision Yield', 'Angle Failed'),
    ('Die Position 3 Vision Yield', 'TOTAL'),

    ('Die Position 4 Vision Yield', 'Passed'),
    ('Die Position 4 Vision Yield', 'Empty Failed'),
    ('Die Position 4 Vision Yield', 'Others Failed'),
    ('Die Position 4 Vision Yield', 'Angle Failed'),
    ('Die Position 4 Vision Yield', 'TOTAL'),

    ('Die Position 5 Vision Yield', 'Passed'),
    ('Die Position 5 Vision Yield', 'Empty Failed'),
    ('Die Position 5 Vision Yield', 'Others Failed'),
    ('Die Position 5 Vision Yield', 'Angle Failed'),
    ('Die Position 5 Vision Yield', 'TOTAL'),

    #Bump Vision Yield
    ('Bump Vision Yield', 'Passed'),
    ('Bump Vision Yield', 'Empty Failed'),
    ('Bump Vision Yield', 'Others Failed'),
    ('Bump Vision Yield', 'Angle Failed'),
    ('Bump Vision Yield', 'Die Sawn Failed'),
    ('Bump Vision Yield', 'Chip In Failed'),
    ('Bump Vision Yield', 'Chip Out Failed'),
    ('Bump Vision Yield', 'Contamination Failed'),
    ('Bump Vision Yield', 'Crack Failed'),
    ('Bump Vision Yield', 'Die Size Failed'),
    ('Bump Vision Yield', 'SubROI Failed'),
    ('Bump Vision Yield', 'Spec Failed'),
    ('Bump Vision Yield', 'Bump Failed'),
    ('Bump Vision Yield', 'Pad Failed'),
    ('Bump Vision Yield', 'TOTAL'),

    # 5S Sidewall Vision Yield
    ('5S Sidewall Vision Yield', 'Passed'),
    ('5S Sidewall Vision Yield', 'Empty Failed'),
    ('5S Sidewall Vision Yield', 'Others Failed'),
    ('5S Sidewall Vision Yield', 'Angle Failed'),
    ('5S Sidewall Vision Yield', 'Chip Failed'),
    ('5S Sidewall Vision Yield', 'Contamination Failed'),
    ('5S Sidewall Vision Yield', 'Crack Failed'),
    ('5S Sidewall Vision Yield', 'Bump Failed'),
    ('5S Sidewall Vision Yield', 'TOTAL'),

    # Pocket Position B Vision Yield
    ('Pocket Position B Vision Yield', 'Passed'),
    ('Pocket Position B Vision Yield', 'Others Failed'),
    ('Pocket Position B Vision Yield', 'TOTAL'),

    #In Pocket B Vision Yield
    ('In Pocket B Vision Yield', 'Passed'),
    ('In Pocket B Vision Yield', 'Empty Failed'),
    ('In Pocket B Vision Yield', 'Others Failed'),
    ('In Pocket B Vision Yield', 'Angle Failed'),
    ('In Pocket B Vision Yield', 'Chip In Failed'),
    ('In Pocket B Vision Yield', 'Chip Out Failed'),
    ('In Pocket B Vision Yield', 'Contamination Failed'),
    ('In Pocket B Vision Yield', 'Crack Failed'),
    ('In Pocket B Vision Yield', 'Adhesive Failed'),
    ('In Pocket B Vision Yield', 'Edge Failed'),
    ('In Pocket B Vision Yield', 'Die Size Failed'),
    ('In Pocket B Vision Yield', 'SubROI Failed'),
    ('In Pocket B Vision Yield', 'Marking Failed'),
    ('In Pocket B Vision Yield', 'Orientation Failed'),
    ('In Pocket B Vision Yield', 'No Mark Failed'),
    ('In Pocket B Vision Yield', '2D Code Failed'),
    ('In Pocket B Vision Yield', 'Copper Exposed Failed'),
    ('In Pocket B Vision Yield', 'TOTAL'),

    # Post Seal B Vision Yield
    ('Post Seal B Vision Yield', 'Empty Failed'),
    ('Post Seal B Vision Yield', 'Others Failed'),
    ('Post Seal B Vision Yield', 'Angle Failed'),
    ('Post Seal B Vision Yield', 'Chip Failed'),
    ('Post Seal B Vision Yield', 'Crack Failed'),
    ('Post Seal B Vision Yield', 'Contamination Failed'),
    ('Post Seal B Vision Yield', 'Marking Failed'),
    ('Post Seal B Vision Yield', 'Top Layer Seal Broken'),
    ('Post Seal B Vision Yield', 'Bottom Layer Seal Broken'),
    ('Post Seal B Vision Yield', 'Both Layer Seal Broken'),
    ('Post Seal B Vision Yield', 'Top Layer Seal Limit Exceeded'),
    ('Post Seal B Vision Yield', 'Bottom Layer Seal Limit Exceeded'),
    ('Post Seal B Vision Yield', 'Both Layer Seal Limit Exceeded'),
    ('Post Seal B Vision Yield', 'Top Layer Seal Width Inconsistency'),
    ('Post Seal B Vision Yield', 'Bottom Layer Seal Width Inconsistency'),
    ('Post Seal B Vision Yield', 'Both Layer Seal Width Inconsistency'),
    ('Post Seal B Vision Yield', 'Relative Seal Width Inconsistency'),
    ('Post Seal B Vision Yield', 'TOTAL'),

    # TopVision Vision Yield
    ('TopVision Vision Yield', 'Passed'),
    ('TopVision Vision Yield', 'Empty Failed'),
    ('TopVision Vision Yield', 'Others Failed'),
    ('TopVision Vision Yield', 'Chip Failed'),
    ('TopVision Vision Yield', 'Contamination Failed'),
    ('TopVision Vision Yield', 'Crack Failed'),
    ('TopVision Vision Yield', 'Marking Failed'),
    ('TopVision Vision Yield', 'Discolouration Failed'),
    ('TopVision Vision Yield', 'Copper Exposed Failed'),
    ('TopVision Vision Yield', 'TOTAL'),

    # 3D Vision Yield
    ('3D Vision Yield', 'Passed'),
    ('3D Vision Yield', 'Empty Failed'),
    ('3D Vision Yield', 'Others Failed'),
    ('3D Vision Yield', 'Bump Height Failed'),
    ('3D Vision Yield', 'Warpage Failed'),
    ('3D Vision Yield', 'Slanted Failed'),
    ('3D Vision Yield', 'TOTAL'),

    # Infrared Ray Vision Yield
    ('Infrared Ray Vision Yield', 'Passed'),
    ('Infrared Ray Vision Yield', 'Empty Failed'),
    ('Infrared Ray Vision Yield', 'Others Failed'),
    ('Infrared Ray Vision Yield', 'Angle Failed'),
    ('Infrared Ray Vision Yield', 'Chip Failed'),
    ('Infrared Ray Vision Yield', 'Contamination Failed'),
    ('Infrared Ray Vision Yield', 'Crack Failed'),
    ('Infrared Ray Vision Yield', 'Marking Failed'),
    ('Infrared Ray Vision Yield', 'Delamination'),
    ('Infrared Ray Vision Yield', 'TOTAL'),
]

COL_NAMES = {
    "first_col_names": [ "Input Wafer Vision Yield", "Die Position 1 Vision Yield", "Die Position 2 Vision Yield", 
    "Die Position 3 Vision Yield", "Die Position 4 Vision Yield", "Die Position 5 Vision Yield", "Bump Vision Yield", 
    "5S Sidewall Vision Yield", "Pocket Position B Vision Yield", "In Pocket B Vision Yield", "Post Seal B Vision Yield", "TopVision Vision Yield",
    "3D Vision Yield", "Infrared Ray Vision Yield"],
    
    "table_names": [ "Wafer Information,"]
}


def load_tables_from_csv(file_path):
    """Split CSV with multiple tables separated by empty rows"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Split by double newlines (empty rows)
        csv_tables = content.split('\n\n')
        
        dataframes = dict()
        for i, section in enumerate(csv_tables):
            if not section.strip(): continue  # Skip empty sections
            try:
                if i == 0: # First Table | Edge case
                    report_info = pd.Series(section.strip().split('\n')[:3]).to_frame()
                    dataframes["report_info"] = report_info

                    df = pd.read_csv(io.StringIO(section), 
                        sep=',',
                        skiprows=3,
                        engine='python',        # More flexible than C engine
                        on_bad_lines='skip',    # Skip problematic lines
                        dtype=str,              # Read everything as strings first
                        header=None)
                    dataframes["general_data"] = df
                if section.split('\n')[0] in COL_NAMES["table_names"]: # Tables with table name
                    df = pd.read_csv(io.StringIO(section), 
                        sep=',',
                        skiprows=1,
                        engine='python',        
                        on_bad_lines='skip',    
                        dtype=str,              
                        header=0)
                    dataframes[section.split('\n')[0]] = df
                if section.split(',')[0] in COL_NAMES["first_col_names"]: # Tables where name is on first col
                    df = pd.read_csv(io.StringIO(section), 
                        sep=',',
                        engine='python',        
                        on_bad_lines='skip',    
                        dtype=str,              
                        header=0)
                    dataframes[section.split(',')[0]] = df
                print(df.head())
            except Exception as e:
                print(f"Error reading table: {e}")
                continue
        #print(f"Extracted {len(dataframes)} tables from {file_path}")
        return dataframes
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []

def add_values(in_tables: dict[str, pd.DataFrame], out_table: pd.DataFrame, next_index: int) -> pd.DataFrame:
    report_info = in_tables['report_info']

    die_position_1 = in_tables['Die Position 1 Vision Yield'].T # Transposed
    die_position_1.columns = die_position_1.iloc[0] # First row as header
    die_position_1 = die_position_1.iloc[1:] # Remove first row

    die_position_2 = in_tables['Die Position 2 Vision Yield'].T
    die_position_2.columns = die_position_2.iloc[0]
    die_position_2 = die_position_2.iloc[1:]

    die_position_3 = in_tables['Die Position 3 Vision Yield'].T
    die_position_3.columns = die_position_3.iloc[0]
    die_position_3 = die_position_3.iloc[1:]
    
    die_position_4 = in_tables['Die Position 4 Vision Yield'].T
    die_position_4.columns = die_position_4.iloc[0]
    die_position_4 = die_position_4.iloc[1:]

    die_position_5 = in_tables['Die Position 5 Vision Yield'].T
    die_position_5.columns = die_position_5.iloc[0]
    die_position_5 = die_position_5.iloc[1:]

    bump_vision = in_tables['Bump Vision Yield'].T
    bump_vision.columns = bump_vision.iloc[0]
    bump_vision = bump_vision.iloc[1:]

    sidewall_vision = in_tables['5S Sidewall Vision Yield'].T
    sidewall_vision.columns = sidewall_vision.iloc[0]
    sidewall_vision = sidewall_vision.iloc[1:]

    pocket_b_position = in_tables['Pocket Position B Vision Yield'].T
    pocket_b_position.columns = pocket_b_position.iloc[0]
    pocket_b_position = pocket_b_position.iloc[1:]

    in_pocket_b_position = in_tables['In Pocket B Vision Yield'].T
    in_pocket_b_position.columns = in_pocket_b_position.iloc[0]
    in_pocket_b_position = in_pocket_b_position.iloc[1:]

    post_seal_b = in_tables['Post Seal B Vision Yield'].T
    post_seal_b.columns = post_seal_b.iloc[0]
    post_seal_b = post_seal_b.iloc[1:]

    top_vision = in_tables['TopVision Vision Yield'].T
    top_vision.columns = top_vision.iloc[0]
    top_vision = top_vision.iloc[1:]

    vision_3d = in_tables['3D Vision Yield'].T
    vision_3d.columns = vision_3d.iloc[0]
    vision_3d = vision_3d.iloc[1:]

    infrared_ray_vision = in_tables['Infrared Ray Vision Yield'].T
    infrared_ray_vision.columns = infrared_ray_vision.iloc[0]
    infrared_ray_vision = infrared_ray_vision.iloc[1:]

    wafer_info = in_tables['Wafer Information,']

    # Add values
    out_table.loc[next_index,('', 'Lot')] = report_info.iloc[1, 0]      # Row 1, Column 0
    out_table.loc[next_index,('', 'Equip ID')] = report_info.iloc[0, 0]  # Row 0, Column 0
    out_table.loc[next_index,('', 'Date')] = report_info.iloc[2, 0]      # Row 2, Column 0

    out_table.loc[next_index, 'Die Position 1 Vision Yield'] = die_position_1.iloc[0].values
    out_table.loc[next_index, 'Die Position 2 Vision Yield'] = die_position_2.iloc[0].values
    out_table.loc[next_index, 'Die Position 3 Vision Yield'] = die_position_3.iloc[0].values
    out_table.loc[next_index, 'Die Position 4 Vision Yield'] = die_position_4.iloc[0].values
    out_table.loc[next_index, 'Die Position 5 Vision Yield'] = die_position_5.iloc[0].values
    out_table.loc[next_index, 'Bump Vision Yield'] = bump_vision.iloc[0].values
    out_table.loc[next_index, '5S Sidewall Vision Yield'] = sidewall_vision.iloc[0].values
    out_table.loc[next_index, 'Pocket Position B Vision Yield'] = pocket_b_position.iloc[0].values
    out_table.loc[next_index, 'In Pocket B Vision Yield'] = in_pocket_b_position.iloc[0].values
    out_table.loc[next_index, 'Post Seal B Vision Yield'] = post_seal_b.iloc[0].values
    out_table.loc[next_index, 'TopVision Vision Yield'] = top_vision.iloc[0].values
    out_table.loc[next_index, '3D Vision Yield'] = vision_3d.iloc[0].values
    out_table.loc[next_index, 'Infrared Ray Vision Yield'] = infrared_ray_vision.iloc[0].values

    # Calculate 'Total Rejects'
    columns_to_exclude = ['Passed', 'TOTAL']

    columns_to_sum = [col for col in die_position_1.columns if col not in columns_to_exclude]
    die_position_1_sum = die_position_1.iloc[0][columns_to_sum].astype(int).sum()
    columns_to_sum = [col for col in die_position_2.columns if col not in columns_to_exclude]
    die_position_2_sum = die_position_2.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in die_position_3.columns if col not in columns_to_exclude]
    die_position_3_sum = die_position_3.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in die_position_4.columns if col not in columns_to_exclude]
    die_position_4_sum = die_position_4.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in die_position_5.columns if col not in columns_to_exclude]
    die_position_5_sum = die_position_5.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in bump_vision.columns if col not in columns_to_exclude]
    bump_vision_sum = bump_vision.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in sidewall_vision.columns if col not in columns_to_exclude]
    sidewall_vision_sum = sidewall_vision.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in pocket_b_position.columns if col not in columns_to_exclude]
    pocket_b_position_sum = pocket_b_position.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in in_pocket_b_position.columns if col not in columns_to_exclude]
    in_pocket_b_position_sum = in_pocket_b_position.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in post_seal_b.columns if col not in columns_to_exclude]
    post_seal_b_sum = post_seal_b.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in top_vision.columns if col not in columns_to_exclude]
    top_vision_sum = top_vision.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in vision_3d.columns if col not in columns_to_exclude]
    vision_3d_sum = vision_3d.iloc[0][columns_to_sum].astype(int).sum()

    columns_to_sum = [col for col in infrared_ray_vision.columns if col not in columns_to_exclude]
    infrared_ray_vision_sum = infrared_ray_vision.iloc[0][columns_to_sum].astype(int).sum()

    # Add main summary values
    out_table.loc[next_index, ('Lot Summary','Qty Insp DP1')] = die_position_1['Passed'].iloc[0]
    out_table.loc[next_index, ('Lot Summary','Total Reject')] = (
        die_position_1_sum +
        die_position_2_sum +
        die_position_3_sum +
        die_position_4_sum +
        die_position_5_sum +
        bump_vision_sum +
        sidewall_vision_sum +
        pocket_b_position_sum +
        in_pocket_b_position_sum +
        post_seal_b_sum +
        top_vision_sum +
        vision_3d_sum +
        infrared_ray_vision_sum
    )
    passed = float(out_table.loc[next_index, ('Lot Summary','Qty Insp DP1')])
    failed = float(out_table.loc[next_index, ('Lot Summary','Total Reject')])
    out_table.loc[next_index, ('Lot Summary','Yield')] = str((( passed - failed)/passed*100).__round__(2)) + '%'

    # Reel counts
    r1 = wafer_info[wafer_info['Reel No'] == '1']['Unit Count'].astype(int).sum()
    r2 = wafer_info[wafer_info['Reel No'] == '2']['Unit Count'].astype(int).sum()
    r3 = wafer_info[wafer_info['Reel No'] == '3']['Unit Count'].astype(int).sum()

    out_table.loc[next_index,('', 'Reel 1')] = r1
    out_table.loc[next_index,('', 'Reel 2')] = r2
    out_table.loc[next_index,('', 'Reel 3')] = r3
    out_table.loc[next_index,('', 'Tape & Reel B Total')] = r1+r2+r3

    return out_table

def fix_column_names(df: pd.DataFrame) -> pd.DataFrame:
    "Removes duplicate category headers from MultiIndex columns"
    # Clean up MultiIndex columns - remove duplicate category headers
    new_columns = []
    prev_category = None

    for category, column in df.columns:
        if category != prev_category:
            new_columns.append((category, column))
            prev_category = category
        else:
            new_columns.append(('', column))  # Empty string for duplicate categories

    df.columns = pd.MultiIndex.from_tuples(new_columns)
    return df

def get_last_modified_time(file_path):
    try:
        modification_time = os.path.getmtime(file_path)
        last_modified_datetime = datetime.fromtimestamp(modification_time)
        return last_modified_datetime.date()
    except FileNotFoundError:
        return None

def main(start_date: datetime.date, end_date: datetime.date) -> str | None:
    """Main function to process files and generate report"""
    files = list()
    out_df = pd.DataFrame(columns=pd.MultiIndex.from_tuples(OUTPUT_COLUMNS), dtype=str)

    #Select files we will process, only .txt files within the range dates
    print('Searching for files in Paths...')
    for path in PATHS_TO_SEARCH:
        os.walk(path)
        for filename in os.listdir(path):
            if 'csv' not in filename.split(".")[-1]:
                continue
            file_path = os.path.join(path, filename)
            last_modified_time = get_last_modified_time(file_path)
            if start_date <= last_modified_time <= end_date:
                files.append(file_path)

    print('Extracting info from files...')
    if not files:
        print("No files found in the specified date range.")
        return None, 0
    
    for file in files:
        try:
            print(f"Processing file: {file}")
            file_path = Path(file)
            in_tables = load_tables_from_csv(file_path)
            
            if in_tables:
                #print(f"Tables: {len(in_tables)} | File: {file_path.name}")
                #print(f'Adding values...')
                out_df = add_values(in_tables, out_df, len(out_df))
            else:
                print(f"No tables found in {file_path.name}")
                        
        except Exception as e:
            print(f"Error while processing {file}. Will not include that file.") 
            print(f"Error: {e}") 
            continue 
    
    # Check if we have any data to export
    if out_df is None or out_df.empty:
        print("No data to export. Check your date range or file contents.")
        return None, len(files)
    
    # Remove whitespaces
    out_df = out_df.map(lambda x: x.strip() if isinstance(x, str) else x)

    # Fix column names
    out_df = fix_column_names(out_df)

    #Export dataframe
    output_dir = Path.cwd() / 'report_app_MI-28'
    output_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    
    new_filename = output_dir / f'report_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv'
    
    print(f"Data shape: {out_df.shape}")

    out_df.to_csv(new_filename, index=False)
    print(f'Created at: {new_filename}')
    
    try:
        subprocess.Popen(['start', 'excel', str(new_filename)], shell=True)
    except Exception as e:
        print(f"Could not open Excel: {e}")
    
    return str(new_filename), len(files)


def create_gui():
    """Create and run the GUI application"""
    root = tk.Tk()
    root.geometry('300x200')
    root.title('Film2Reel App')

    name_label = ttk.Label(root, text='Start Date (yyyy-mm-dd):')
    name_label.pack(pady=2)

    start_entry = ttk.Entry(root)
    #start_entry.insert(0, '2025-10-05') # For testing
    start_entry.pack(pady=5)
    start_entry.focus()

    date_label = ttk.Label(root, text='End Date (yyyy-mm-dd):')
    date_label.pack(pady=2)

    end_entry = ttk.Entry(root)
    #end_entry.insert(0, '2025-10-07') # For testing
    end_entry.pack(pady=5)

    def entryhandler():
        try:
            start, end = start_entry.get(), end_entry.get()
            result = main(datetime.strptime(start, "%Y-%m-%d").date(), datetime.strptime(end, "%Y-%m-%d").date())
            if result:
                print("Report generated successfully!")
            else:
                print("No report generated. Check your date range.")
        except ValueError as e:
            print(f"Invalid date format: {e}")
        except Exception as e:
            print(f"Error generating report: {e}")

    run_button = ttk.Button(
        root,
        text='Run',
        command=entryhandler
    )

    run_button.pack(
        ipadx=5,
        ipady=5,
        expand=True
    )

    # Create a frame for bottom labels
    bottom_frame = ttk.Frame(root)
    bottom_frame.pack(side='bottom', fill='x', padx=10, pady=5)

    # Add author and date labels stacked vertically in the bottom frame
    author_label = ttk.Label(bottom_frame, text='Author: Emilia Millan')
    author_label.pack(side='top', anchor='w')
    
    creation_date_label = ttk.Label(bottom_frame, text='October, 2025')
    creation_date_label.pack(side='top', anchor='w')

    root.mainloop()

if __name__ == '__main__':
    create_gui()