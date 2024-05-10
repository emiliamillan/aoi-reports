import datetime
from pathlib import Path
from PyQt5.QtWidgets import (
    QTextEdit, 
)

def format_lots_input(self: QTextEdit):
    text = self.text_input.toPlainText().replace(".1\n", ";")
    text = text.replace(".1\r\n", ";")
    text = text.replace(".1","")
    self.text_input.setPlainText(text)

def get_list_of_lots(self):
    lots_input = self.text_input.toPlainText()
    list_of_lots = lots_input.split(";")
    print(list_of_lots)

def select_folder(path_list:list|str, path: str, key_process:str, parameters:dict):
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