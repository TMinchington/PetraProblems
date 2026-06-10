"""
Extra functions to make petra problems work
"""
import os 
import json

JSON_PATH = "petraProblems/.data/path.json"

def paths_json_saver(json_dic):
    with open(JSON_PATH, "w") as jout:
        json.dump(json_dic, jout)
    

def paths_json_loader():
    if not os.path.isfile(JSON_PATH):
        paths_json_saver({"fiji": "None"})
    with open(JSON_PATH) as j_in:
        return json.load(j_in)

def check_files_tiff(path):
    all_files = os.listdir(path)
    tiffs = [x for x in all_files if x.endswith("tif")]
    czi = [x.replace(".czi", ".tif") for x in all_files if x.endswith("czi")]
    
    czi_missing_tif = [x for x in czi if x not in tiffs]
    have_tiffs = [x for x in czi if x in tiffs]
    
    return {"total_files": len(tiffs) + len(czi),
            "have_tiffs": len(have_tiffs),
            "missing_tiffs":len(czi_missing_tif)}
    
    
def check_files_lines(path):
    all_files = os.listdir(path)
    tiffs = [x for x in all_files if x.endswith("tif")]
    path_line = os.path.join(path, "data/lines")
    line_files = [x for x in os.listdir(path_line) if x.endswith("-line.txt")]
    have_lines = [x for x in tiffs if x.replace(".tif", "-line.txt") in line_files] 
    missing_lines = [x for x in tiffs if x.replace(".tif", "-line.txt") not in line_files]
    return {
            "have_lines": len(have_lines),
            "missing_lines":len(missing_lines)}
    
    
def check_files_masks(path):
    all_files = os.listdir(path)
    tiffs = [x for x in all_files if x.endswith("tif")]
    path_mask = os.path.join(path, "data/masks")
    mask_files = [x for x in os.listdir(path_mask) if x.endswith("-masks.tif")]
    have_lines = [x for x in tiffs if x.replace(".tif", "-masks.tif") in mask_files]
    missing_lines = [x for x in tiffs if x.replace(".tif", "-masks.tif") not in mask_files]
    return {
            "have_masks": len(have_lines),
            "missing_masks":len(missing_lines)}

if __name__ == "__main__":
    pass