import os 

class FolderFunctions():
    def __init__(self, path):
        self.path = path
        
        if os.path.isdir(self.path):
            self.setup_paths()
    
    def checkPathExists(self):
        if not os.path.isdir(self.path):
            return "Selected path does not exist"
        
        else:
            return self.path
        
    
    def setup_paths(self):
        path_list = ["data",
                     "data/masks",
                     "data/lines",
                     "data/positions",
                     "data/measurements",
                     "data/graphs"]
        print("My path", self.path)
        for n, p in enumerate(path_list):
            full_path = os.path.join(self.path, p)
            print(full_path)
            print(self.path)
            if not os.path.isdir(full_path):
                if n == 0:
                    print("New experiment")
            # try:    
                os.makedirs(full_path)
                print(f"Made path: {full_path}")    
        
            # except OSError:
            #     print(f"Couldn't make path: {full_path}")
            #     exit()
            
            
                
    def return_path(self):
        return self.path