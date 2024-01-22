from pathlib import Path

from utils import EXTENSIONS, VITROX_PATHS_LIST, VITROX_VARIANTS_LIST, aggregate_new_path, get_list_of_lots, select_folder

class Workflow:
    
    @staticmethod
    def vitrox_process():
        return 0
    
    @staticmethod
    def icos_process():
        return 0
    
    @staticmethod
    def start_process():
        return 0
    
    @staticmethod
    def flow(text_input:str):
        list_of_lots = get_list_of_lots(text_input)
        
        Workflow.look_up_for_lots(
            list_of_lots,
            VITROX_PATHS_LIST,
            VITROX_VARIANTS_LIST,
            "vitrox"
        )
        
        Workflow.icos_process()

    @staticmethod
    def look_up_for_lots(list_of_lots: list|str=None, path_list: list|str=None, variants_list: list|str=None, key_process:str=None):
        lot_path = None
        #look for lots
        for lot in list_of_lots:
            for path in path_list:
                for variant in variants_list:
                    if "vitrox" in key_process:
                        print("Vitrox")
                        lot_path = path + "\\" + lot + variant + EXTENSIONS[key_process];
                    elif "icos" in key_process:
                        print("Icos")
                        lot_path = path + "\\" + lot + variant + Workflow.GLOBAL + Workflow.EXTENSIONS[key_process];

                    if Path(lot_path).is_file():
                        print("It exists")
                        folder = select_folder(path_list, path, key_process)
                        folder = aggregate_new_path(folder, lot, key_process, variant, Workflow.GLOBAL)






                            

        

