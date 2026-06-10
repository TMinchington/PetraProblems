import subprocess
import os 
# import imagej
import numpy as np

class FijiWorker():
    def __init__(self, pathToFiji):
        self.fijiPath = pathToFiji
        
        
        
    def checkFijiPath(self):
        
        if self.fijiPath == None:
            return "No fiji path set"
        
        fijiEndPath = os.path.split(self.fijiPath)[1]
        print(fijiEndPath)
        if fijiEndPath != "Fiji.app" and fijiEndPath != "fiji-windows-x64.exe":
            return "FijiPath incorrect"
            
        else:
            
            return 0
        
    def run_fiji_macro_headless(self, macro_path, macro_args=None):
        if self.checkFijiPath() != 0:
            exit("fiji error")
            
        fiji_command = [
        self.fijiPath+"/Contents/MacOS/ImageJ-macosx",
        "--headless",
        "--console",
        "-macro",
        macro_path,
    ]

        if macro_args:
            fiji_command.append(",".join(macro_args))
            print("appending arguments")
        try:
            result = subprocess.run(fiji_command, check=True, capture_output=True, text=True)
            print("Fiji macro executed successfully.")
            print("Output:\n", result.stdout)
        except FileNotFoundError:
            print(f"Error: Fiji executable not found at '{self.fijiPath}'")
        except subprocess.CalledProcessError as e:
            print("Error executing Fiji macro:")
            print("Return code:", e.returncode)
            print("Output:\n", e.stdout)
            print("Error output:\n", e.stderr)
            
    def run_fiji_macro_headed(self, macro_path, macro_args=None):
        if self.checkFijiPath() != 0:
            exit("fiji error")
        if self.fijiPath.endswith(".app"):
            fixed_path = self.fijiPath+"/Contents/MacOS/ImageJ-macosx"
        else:
            fixed_path = self.fijiPath
        fiji_command = [fixed_path
        ,
        # "--headless",
        "--console",
        "-macro",
        
        # "--run",
        macro_path,
    ]

        if macro_args:
            fiji_command.append(",".join(macro_args))
            print("appending arguments")
        try:
            fiji_directory = os.path.dirname(self.fijiPath)
            print("Fiji directory:", fiji_directory)
            result = subprocess.run(fiji_command, check=True, capture_output=True, text=True, cwd=fiji_directory)
            print("Fiji macro executed successfully.")
            print("Output:\n", result.stdout)
        except FileNotFoundError:
            print(f"Error: Fiji executable not found at '{self.fijiPath}'")
        except subprocess.CalledProcessError as e:
            print("Error executing Fiji macro:")
            print("Return code:", e.returncode)
            print("Output:\n", e.stdout)
            print("Error output:\n", e.stderr)

    def run_fiji_pyimagje():
        pass

    def run_fiji_direct():
        exit()
    
    def set_path(self, new_path):
        self.fijiPath = new_path
        
        

if __name__ == "__main__":
    f1 = FijiWorker(pathToFiji=None)
    
    f1.checkFijiPath()
    f1.set_path("/Applications/Fiji.app")
    f1.run_fiji_macro_headed("petraProblems/fiji_scripts/convert_images.ijm", ["/Users/thomas.minchington/Documents/petraCodeCheck", "czi"])
    # f1.run_fiji_macro_headed("petraProblems/fiji_scripts/drawLinesForDistance.ijm")
    
    




    