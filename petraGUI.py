import customtkinter as ctk
from petraProblems.folderOperations import FolderFunctions
from petraProblems import fijiOperations
from petraProblems.misc_functions import paths_json_loader, paths_json_saver, check_files_tiff, check_files_lines, check_files_masks
import os
from petraProblems.cellPoseFunctions import run3Dbase
# from petraProblems.calculate_data import *
from petraProblems.newAnalysis.m1_data_extraction import main as mainAnalysis
from PIL import Image

class WelcomeWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.pathHolder = "User/Documents/prettyPictures"
        
        # self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        
        # self.mainTitle = ctk.CTkLabel(self, text="Welcome to", text_color="white",font=("SignPainter", 30))
        # 
        self.image = ctk.CTkImage(Image.open("petraProblems/.data/ss_logo@4x.png"), size=(224*1.2, 236*1.2))
        self.subTitle = ctk.CTkLabel(self, image=self.image, text="")
        self.version = ctk.CTkLabel(self, text="Thomas Minchington (2025)", text_color="white",font=("helvetica", 12))
        self.startButton = ctk.CTkButton(self, text="Start",
                                                    text_color=app_pallet["spaceCad"],
                                                    fg_color=app_pallet["pink"],
                                                    hover_color=app_pallet["green"],
                                                    font=("helvetica", 15), command=self.startButtonPress)
        
        self.instructions = ctk.CTkLabel(self, text="Select the directory containing the TIFF of the images to process, then click start.", text_color="white")
        
        # self.mainTitle.grid(row=0, column=0, pady=(140,0), sticky="sew", rowspan=1)
        self.subTitle.grid(row=0, column=0, columnspan=3, pady=(80,20), sticky="sew", rowspan=1)
        self.version.grid(row=5, column=0, columnspan=3, sticky="s", pady=10)
        self.instructions.grid(row=1, column=0, columnspan=3, sticky="s", pady=10)
        self.startButton.grid(row=4, column=0, columnspan=3, sticky="n", pady=20)
        
        self.pathWarning = ctk.CTkLabel(self, text=" ", text_color="red",font=("helvetica", 14, "bold"))
        self.pathWarning.grid(row=3, column=0, columnspan=3, sticky="ns")
        
        self.filePath = ctk.CTkTextbox(self, height=30)
        self.filePath.insert("0.0", self.pathHolder)
        self.filePath.grid(column=0, row=2, pady=20, padx=(20, 10), sticky="ew", columnspan=2)
        
        self.browseButton = ctk.CTkButton(self, text="browse", command=self.browseButtonPress,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
        
        self.browseButton.grid(column=2, row=2, pady=20, padx=(0, 20), sticky="ew")
        
        
    def browseButtonPress(self):

        self.getFileLocation = ctk.filedialog.askdirectory()
        print(self.getFileLocation)
        self.getFileLocationName = self.getFileLocation
        # self.getFileLocation.close()
        self.filePath.delete("0.0","end")
        self.filePath.insert("0.0", self.getFileLocationName)
        
        
    def startButtonPress(self):
        currentText = self.filePath.get("0.0", "end").strip()

        if currentText == self.pathHolder:
            print("Select new path to continue....")
            self.pathWarning = ctk.CTkLabel(self, text="Set new path to continue", text_color="red",font=("helvetica", 14, "bold"))
            self.pathWarning.forget()
            self.pathWarning.grid(row=3, column=0, columnspan=3, sticky="ns")
        
        else:
            app.workpath = FolderFunctions(path=currentText)
            pathCheck = app.workpath.checkPathExists()
            
            if pathCheck == "Selected path does not exist":
                self.pathWarning = ctk.CTkLabel(self, text=pathCheck, text_color="red",font=("helvetica", 14, "bold"))
                self.pathWarning.forget()
                self.pathWarning.grid(row=3, column=0, columnspan=3, sticky="ns")
            
            else:
                app.loadWorkWindow()
            
            print(f"Path is: {pathCheck}")

class workFlowWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        
        self.fileCheckDic = check_files_tiff(app.workpath.return_path())
        print(self.fileCheckDic)
        
        if self.fileCheckDic["missing_tiffs"] == 0:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.fileCheckDic['missing_tiffs']} files are missing tifs", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet["green"], text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=2)

            
        elif self.fileCheckDic["missing_tiffs"] == 1:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.fileCheckDic['missing_tiffs']} file is missing a tif", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            
            self.update_button.grid(column=0, row=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=3)
            
        else:
            
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.fileCheckDic['missing_tiffs']} file are missing tifs", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            self.update_button.grid(column=0, row=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=3)
            
            
    
    def update_button_pressed(self):
        print("Doodles!")
        fboy = fijiOperations.FijiWorker(app.paths_dic['fiji'])
        fboy.run_fiji_macro_headed(os.path.join(os.getcwd(), "petraProblems/fiji_scripts/convert_images.ijm"), [app.workpath.return_path(), "czi"])
        
        
        app.loadWorkWindow()
        
        
    def continue_button_pressed(self):
        print("Time to pose")

        app.loadWorkWindowLines()


class workFlowWindow_lines(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        
        self.lines_dic = check_files_lines(app.workpath.return_path())
        
        print(self.lines_dic)
        
        
        if self.lines_dic['missing_lines'] == 0:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_lines']} files are missing lines", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet["green"], text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=2)

            
        elif self.lines_dic['missing_lines'] == 1:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_lines']} file is missing a line file", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            
            self.update_button.grid(column=0, row=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=3)
            
        else:
            
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_lines']} file are missing lines", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            self.update_button.grid(column=0, row=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=3)
            
            
    
    def update_button_pressed(self):
        print("I shall convert all!")
        fboy = fijiOperations.FijiWorker(app.paths_dic['fiji'])
        # fboy.run_fiji_macro_headed("petraProblems/fiji_scripts/convert_images.ijm", [app.workpath.return_path(), "czi"])
        fboy.run_fiji_macro_headed(os.path.join(os.getcwd(), "petraProblems/fiji_scripts/drawLines.ijm"), [app.workpath.return_path()])
        
        app.loadWorkWindowLines()
        
        
    def continue_button_pressed(self):
        print("The line will be drawn here")

        app.loadWorkWindowCellpose()
        

class workFlowWindow_cellpose(ctk.CTkFrame):
    """
    
    Window for running cellpose operations


    """
    def __init__(self, master):
        super().__init__(master)
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        
        self.lines_dic = check_files_masks(app.workpath.return_path())
        
        print(self.lines_dic)
        
        
        if self.lines_dic['missing_masks'] == 0:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_masks']} files are missing masks", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1, columnspan=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet["green"], text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=2, columnspan=2)

            
        elif self.lines_dic['missing_masks'] == 1:
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_masks']} file is missing a mask file", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1, columnspan=2)
            
            self.dapi_text = ctk.CTkLabel(self, text="DAPI channel:", text_color="white",font=("helvetica", 20, "bold"))
            self.dapi_text.grid(column=0, row=2, columnspan=1, sticky="e")
            self.dapi_drop = ctk.CTkOptionMenu(self, width=80, height=28, values=["1", "2", "3", "4"])
            self.dapi_drop.grid(column=1, row=2, sticky="w")
            
            self.cyto_text = ctk.CTkLabel(self, text="Cyto channel:", text_color="white",font=("helvetica", 20, "bold"))
            self.cyto_text.grid(column=0, row=3, columnspan=1, sticky="e")
            self.cyto_drop = ctk.CTkOptionMenu(self, width=80, height=28, values=["1", "2", "3", "4"])
            self.cyto_drop.set("3")
            self.cyto_drop.grid(column=1, row=3, sticky="w")
            
            
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            self.update_button.grid(column=0, row=4, columnspan=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=5, columnspan=2)
            
        else:
            
            self.missingTiffs = ctk.CTkLabel(self, text=f"{self.lines_dic['missing_masks']} file are missing masks", text_color="white",font=("helvetica", 20, "bold"))
            self.missingTiffs.grid(column=0, row=1)
            self.update_button = ctk.CTkButton(self, text="update", command=self.update_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
            
            self.dapi_text = ctk.CTkLabel(self, text="DAPI channel:", text_color="white",font=("helvetica", 20, "bold"))
            self.dapi_text.grid(column=0, row=2, columnspan=1, sticky="e")
            self.dapi_drop = ctk.CTkOptionMenu(self, width=80, height=28, values=["1", "2", "3", "4"])
            self.dapi_drop.grid(column=1, row=2, sticky="w")
            
            self.cyto_text = ctk.CTkLabel(self, text="Cyto channel:", text_color="white",font=("helvetica", 20, "bold"))
            self.cyto_text.grid(column=0, row=3, columnspan=1, sticky="e")
            self.cyto_drop = ctk.CTkOptionMenu(self, width=80, height=28, values=["1", "2", "3", "4"])
            self.cyto_drop.set("3")
            self.cyto_drop.grid(column=1, row=3, sticky="w")
            
            self.update_button.grid(column=0, row=4, columnspan=2)
            
            self.continue_button = ctk.CTkButton(self, text="continue", command=self.continue_button_pressed,
                                                    fg_color=app_pallet['pink'], hover_color="red", text_color=app_pallet['spaceCad'])
            
            self.continue_button.grid(column=0, row=5, columnspan=2)
            
            
    
    def update_button_pressed(self):
        print("Segmentation time!")
        dapi = int(self.dapi_drop.get())-1
        cyto = int(self.cyto_drop.get())-1
        run3Dbase(app.workpath.return_path(), dapi, cyto)
               
        app.loadWorkWindowCellpose()
        
        
    def continue_button_pressed(self):
        print("No more masks for you.")

        app.loadFinish()
        
        
class pick_fiji(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        print("pick_fiji")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        self.pathHolder = "fiji.app / fiji.exe"
        self.pickFijiText = ctk.CTkLabel(self, text="Please find your fiji program:", text_color="white",font=("helvetica", 25))
        self.pickFijiText.grid(column=0, columnspan = 3, row=1, sticky="s")
        
        self.filePath = ctk.CTkTextbox(self, height=30)
        self.filePath.insert("0.0", self.pathHolder)
        self.filePath.grid(column=0, row=2, pady=20, padx=(20, 10), sticky="ew", columnspan=2)
        
        self.browseButton = ctk.CTkButton(self, text="browse", command=self.browseButtonPress,
                                                    fg_color=app_pallet['pink'], hover_color=app_pallet['blue'], text_color=app_pallet['spaceCad'])
        
        self.browseButton.grid(column=2, row=2, pady=20, padx=(0, 20), sticky="ew")
        
        

    def browseButtonPress(self):
        
        self.getFileLocation = ctk.filedialog.askopenfilename()

        print(self.getFileLocation)
        self.getFileLocationName = self.getFileLocation
        # self.getFileLocation.close()
        self.filePath.delete("0.0","end")
        self.filePath.insert("0.0", self.getFileLocationName)
        if os.path.exists(self.getFileLocationName):
            app.fijiWorker = fijiOperations.FijiWorker(self.getFileLocation)
            app.paths_dic['fiji'] = self.getFileLocation
            paths_json_saver(app.paths_dic)
            
        else:
            
            self.raiseError = ctk.CTkLabel(self, text="FIJI not found", text_color="red")
            self.raiseError.grid(column=0, columnspan=3, row=3)
            
        app.loadWorkWindow()
        


class FinWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        mainAnalysis(app.workpath.return_path())
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.configure(bg_color=app_pallet["spaceCad"], fg_color=app_pallet["spaceCad"])
        
        self.fileCheckDic = check_files_tiff(app.workpath.return_path())
        print(self.fileCheckDic)
        
        self.missingTiffs = ctk.CTkLabel(self, text=f"Fin", text_color="white",font=("helvetica", 20, "bold"))
        # run_all_files(app.workpath.return_path())
        
        self.missingTiffs.grid(column=0, row=1)
        
        

            




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Petra v1.0")
        self.page_header_font = ctk.CTkFont("helvetica", 30, weight="bold")
        self.paths_dic = paths_json_loader()
        self.configure(bg_color = app_pallet["spaceCad"],  fg_color = app_pallet["spaceCad"])
        self.minsize(600, 800)
        self.geometry("600x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.workpath = ""
        self.switch_to_open()
        self.fijiWorker = None
        
    def switch_to_open(self):
        self.current_window = WelcomeWindow(self)
        self.current_window.grid(column=0, sticky="nsew")
        

    def loadWorkWindow(self):
        print(self.workpath.path)
        print(self.check_fiji(), "Fiji")
        if self.check_fiji():
            self.current_window.forget()
            self.current_window.grid_forget()
            self.current_window = pick_fiji(self)
            self.current_window.grid(column=0, sticky="nsew")
        else:    
            self.current_window.forget()
            self.current_window.grid_forget()
            self.current_window = workFlowWindow(self)
            self.current_window.grid(column=0, sticky="nsew")
        # exit()
    
    def loadWorkWindowLines(self):
        self.current_window.forget()
        self.current_window.grid_forget()
        self.current_window = workFlowWindow_lines(self)
        self.current_window.grid(column=0, sticky="nsew")
        
    def loadWorkWindowCellpose(self):
        self.current_window.forget()
        self.current_window.grid_forget()
        self.current_window = workFlowWindow_cellpose(self)
        self.current_window.grid(column=0, sticky="nsew")
    
    def loadFinish(self):
        self.current_window.forget()
        self.current_window.grid_forget()
        self.current_window = FinWindow(self)
        self.current_window.grid(column=0, sticky="nsew")
    
    def check_fiji(self):
        
        if self.paths_dic["fiji"] =="None":
            return 1
        
        else:
            if os.path.exists(self.paths_dic['fiji']):
                return 0 
            else:
                return 1
            
if __name__ == "__main__":
    
    
    app_pallet = {"spaceCad":"#25283d",
                  "plum":"#8f3985",
                  "blue":"#98dfea",
                  "green":"#07BEB8",
                  "pink":"#EFD9CE"}
    
    
    app = App()
    app.mainloop()
    
    
    
    