from pathlib import Path
import pandas as pd

def find_and_write_duplicates(input_file, output_file):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Find duplicates
    duplicates = df[df.duplicated(keep=False)]
    
    # Tabla - Column1 Org data Column2 Duplicated Data
    result = pd.DataFrame({
        'Original Data': df.iloc[:, 0],
        'Duplicate Data': df.iloc[:, 0].where(df.duplicated(keep=False))
    })
    
    # Write the result to a new Excel file
    result.to_excel(output_file, index=False)

# input // output files
input_file = r'C:\\Users\\millane\\Documents\\aoi-reports\\report_app\\2D.xlsx'
output_file = r'C:\\Users\\millane\\Documents\\aoi-reports\\report_app\\output_with_duplicates.xlsx'

# resultsssss
find_and_write_duplicates(input_file, output_file)
