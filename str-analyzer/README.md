# STR Analyzer

Desktop application for filtering STR information from Excel files and generating a summarized report.

## Requirements

- Windows
- Python 3.14
- [uv](https://docs.astral.sh/uv/)

## 1. Create the project

Create a new project with `uv`:

```powershell
uv init
```

Enter the project folder:

```powershell
cd aoi-reports
```

Create the virtual environment and install the dependencies:

```powershell
uv sync
```

## 2. Install dependencies

Install the required Python packages:

```powershell
uv add pandas openpyxl PySide6
```

Install PyInstaller as a development dependency:

```powershell
uv add --dev pyinstaller
```

## 3. Project structure

The project should have the following structure:

```text
aoi-reports/
│
├── app.py
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

### `main.py`

Contains the Excel processing and report generation logic.

### `app.py`

Contains the PySide6 desktop application interface.

## 4. Run the application

To run the application directly from the source code:

```powershell
uv run python app.py
```

The application will open the **STR Analyzer** desktop window.

## 5. Using the application

### Select the Excel file

Click **Select Excel File** and select the input Excel file.

The application expects:

- **Sheet 1:** Contains `STR#` and `Lot`.
- **Sheet 2:** Contains `STR` and the failure information.
- Failure-mode columns start at column `I`.

### Enter STR values

Enter one or multiple STR values separated by commas.

Example:

```text
315779, 315780, 315781
```

### Generate the report

Click **Generate Report**.

The application will:

1. Search the requested STR values.
2. Find the corresponding `Lot`.
3. Keep all matching STR/Lot rows.
4. Add a `TOTAL` row.
5. Identify the failure modes with the highest number of failures.
6. Keep the Top 10 failure modes.
7. Generate a new Excel report.

The output file will have a name similar to:

```text
filtered_results_2026-09-08_11-42-35.xlsx
```

## 6. Create the Windows executable

Once the application is working correctly, generate the Windows executable with PyInstaller.

Run:

```powershell
uv run pyinstaller --noconfirm --clean --onefile --windowed --name "STR Analyzer" app.py
```

### Generated files

PyInstaller will create:

```text
build/
dist/
STR Analyzer.spec
```

The executable will be located at:

```text
dist\STR Analyzer.exe
```

## 7. Run the executable

Open:

```text
dist\STR Analyzer.exe
```

The application can now be used without running:

```powershell
uv run python app.py
```

The Python source code and development environment are not required by the end user.

## 8. If PyInstaller shows `WinError 5`

If you receive an error similar to:

```text
PermissionError: [WinError 5] Access is denied
```

PyInstaller is usually trying to access a file that is locked by Windows.

Close:

- VS Code
- Python processes
- The STR Analyzer application
- Any terminal currently running the application

Then remove the `build` folder:

```powershell
Remove-Item -Recurse -Force ".\build"
```

If the `.spec` file is also causing problems, remove it:

```powershell
Remove-Item -Force ".\STR Analyzer.spec"
```

Then run PyInstaller again:

```powershell
uv run pyinstaller --noconfirm --clean --onefile --windowed --name "STR Analyzer" app.py
```

## 9. Verify Python version

The project uses Python 3.14.

Check the version used by `uv`:

```powershell
uv run python --version
```

Expected output:

```text
Python 3.14.x
```

You can also check the Python versions managed by `uv`:

```powershell
uv python list
```

## 10. Development workflow

When modifying the application:

Run the source code:

```powershell
uv run python app.py
```

After confirming the changes work, rebuild the executable:

```powershell
uv run pyinstaller --noconfirm --clean --onefile --windowed --name "STR Analyzer" str-analyzer/app.py
```

The updated executable will be available at:

```text
dist\STR Analyzer.exe
```