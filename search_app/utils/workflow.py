from pathlib import Path
from search_app.utils.utils import aggregate_new_path, get_list_of_lots, select_folder


class Workflow():
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
    def flow(self):
        list_of_lots = get_list_of_lots(self)
        
        Workflow.look_up_for_lots(
            list_of_lots,
            Workflow.VITROX_PATHS_LIST,
            Workflow.VITROX_VARIANTS_LIST,
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
                        lot_path = path + "\\" + lot + variant + Workflow.EXTENSIONS[key_process];
                    elif "icos" in key_process:
                        print("Icos")
                        lot_path = path + "\\" + lot + variant + Workflow.GLOBAL + Workflow.EXTENSIONS[key_process];

                    if Path(lot_path).is_file():
                        print("It exists")
                        folder = select_folder(path_list, path, key_process)
                        folder = aggregate_new_path(folder, lot, key_process, variant, Workflow.GLOBAL)


if __name__ == '__main__':
    parameters = {
        "global_path": Workflow.GLOBAL_PATH,
        "icos_paths_list" : Workflow.ICOS_PATHS_LIST,
        "icos_variant_list" : Workflow.ICOS_VARIANTS_LIST,
        "vitrox_paths_list" : Workflow.VITROX_PATHS_LIST,
        "extensions" : Workflow.EXTENSIONS,
        "global" : Workflow.GLOBAL, 
    } 