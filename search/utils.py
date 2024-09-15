import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QTextEdit, 
)

GLOBAL_PATH = "\\\\mexhome03\\Data\\MC Back End\\Generic\\Molding and Singulation\\AOI REPORTS"

EXTENSIONS = {
    "vitrox":".txt",
    "icos":".mht",
}

GLOBAL = "_global"

def format_input(self: QTextEdit):
    """Change the format of the input from string to list(str).

    Args:
        self (QTextEdit): _description_
    """
    text = self.text_input.toPlainText().replace(".1\n", ";")
    text = text.replace(".1\r\n", ";")
    text = text.replace(".1","")
    self.text_input.setPlainText(text)

def get_lots(self) -> list[str]:
    """
    Returns a list with the lots in string.
    """
    lots_input = self.text_input.toPlainText()
    list_of_lots = lots_input.split(";")
    print(list_of_lots)
    return list_of_lots

def select_destination_folder(path_list:list|str, path: str, key_process:str, parameters:dict):
    """Builds the folder in which the existing files will be moved.
    """
    folder = ""
    if path_list.index(path)+1>9:
        folder = parameters["global_path"]
        + "\\" 
        + key_process.upper() 
        + "0" 
        + (path_list.index(path)+1) 
        + "_" 
        + datetime.date.strftime("%Y-%m-%d");
    else: 
        folder = parameters["global_path"]
        + "\\" 
        + key_process.upper() 
        + (path_list.index(path)+1) 
        + "_" 
        + datetime.date.strftime("%Y-%m-%d");
    
    folder = Path(folder)

    if not folder.is_dir():
        folder.mkdir(parents=True)
    return folder

def aggregate_new_path(full_path:str, lot:str, key_process:str, variant:str, global_word:str, workflow_parameters:dict):
    if "vitrox" in key_process:
        full_path = full_path + "\\" + lot + variant + workflow_parameters["extensions"]["vitrox"]
    if "icos" in key_process:
        full_path = full_path + "\\" + lot + variant + global_word + workflow_parameters["extensions"]["icos"]
    return full_path

def search_lots(lots, path_list, variants_list, key_process):
    """Searches for the lots on the paths of each machine icos and vitrox and makes a copy in a new folder.
    """
    lot_path = None
    stored_files = list()
    for lot in lots:
        for path in path_list:
            for variant in variants_list:
                if "vitrox" in key_process:
                    lot_path = path + "\\" + lot + variant + EXTENSIONS[key_process]
                if "icos" in key_process:
                    lot_path = path + "\\" + lot + variant + GLOBAL + EXTENSIONS[key_process]
                print(f'Searching for {lot_path}')

                if Path(lot_path).is_file():
                    print("It exists")
                    folder = select_destination_folder(path_list, path, key_process)
                    folder = aggregate_new_path(folder, lot, key_process, variant, GLOBAL)
                    stored_files.add(folder)
                else:
                    print("Doesn't exist")
            
    