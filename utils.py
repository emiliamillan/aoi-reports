import datetime
from pathlib import Path

GLOBAL_PATH = "\\\\mexhome03\\Data\\MC Back End\\Generic\\Molding and Singulation\\AOI REPORTS"

ICOS_PATHS_LIST = [
    "\\\\MEX6ICOS01\\_results\\ascii\\global",
    "\\\\MEX6ICOS02\\_results\\ascii\\global",
    "\\\\MEX6ICOS03\\_results\\ascii\\global",
    "\\\\mex6icos04\\_results\\ascii\\global",
    "\\\\mex6icos05\\_results\\ascii\\global",
    "\\\\mex6icos06\\_results\\ascii\\global",
    "\\\\mex6icos07\\_results\\ascii\\global",
    "\\\\mex6icos08\\_Results\\ascii\\global",
    "\\\\mex6icos09\\_results\\ascii\\global",
    "\\\\mex6icos10\\_results\\ascii\\global",
    "\\\\mex6icos11\\_results\\ascii\\global",
    "\\\\mex6icos12\\_results\\ascii\\global",
    "\\\\mex6icos13\\_results\\ascii\\global",
    "\\\\mex6icos14\\_results\\ascii\\global",
    "\\\\mex6icos15\\_results\\ascii\\global",
    "\\\\mex6icos16\\_results\\ascii\\global"
]

ICOS_VARIANTS_LIST = [
    ".1",
    ".2",
    ".3",
    ".1_R1",
    ".1_R2",
    ".1_R3"
]

VITROX_PATHS_LIST = [
    "\\\\mex6vtrx01\\d\\Texas\\Report\\ICPLUS",
    "\\\\mex6vtrx02\\D\\Texas\\Report\\ICPLUS",
]

VITROX_VARIANTS_LIST = [
    "\\\\mex6vtrx01\\d\\Texas\\Report\\ICPLUS",
    "\\\\mex6vtrx02\\D\\Texas\\Report\\ICPLUS",
]

EXTENSIONS = {
    "vitrox":".txt",
    "icos":".mht",
}

GLOBAL = "_global"

def select_folder(path_list:list|str, path: str, key_process:str):
    folder = ""
    if path_list.index(path)+1>9:
        folder = GLOBAL_PATH 
        + "\\" 
        + key_process.upper() 
        + "0" 
        + (path_list.index(path)+1) 
        + "_" 
        + datetime.date.strftime("%Y-%m-%d");
    else: 
        folder = GLOBAL_PATH 
        + "\\" 
        + key_process.upper() 
        + (path_list.index(path)+1) 
        + "_" 
        + datetime.date.strftime("%Y-%m-%d");
    
    folder = Path(folder)

    if not folder.is_dir():
        folder.mkdir(parents=True)
    return folder

def format_lots_input(text:str):
    text = text.replace(".1\n", ";")
    text = text.replace(".1\r\n", ";")
    text = text.replace(".1","")
    return text

def get_list_of_lots(lots_input: str):
    list_of_lots = lots_input.split(";")
    print(list_of_lots)
    return list_of_lots

def aggregate_new_path(full_path:str, lot:str, key_process:str, variant:str, global_word:str):
    if "vitrox" in key_process:
        full_path = full_path + "\\" + lot + variant + EXTENSIONS["vitrox"]
    if "icos" in key_process:
        full_path = full_path + "\\" + lot + variant + global_word + EXTENSIONS["icos"]
    return full_path




