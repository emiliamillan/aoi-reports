import pandas as pd

# Path to your Excel file
file_path = "sample_data/STRsYieldRawData_20260907_0432.xlsx"

try:
    # Read Sheet2
    df = pd.read_excel(
        file_path,
        sheet_name="Sheet2",
        header=2
    )
    
    print("\nSuccessfully loaded Excel file!")
    print("\nRows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nFirst 5 rows:")
    print(df.head())

except Exception as e:
    print("\nERROR:")
    print(e)