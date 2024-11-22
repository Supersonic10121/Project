import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import StringVar, OptionMenu

class View:
    def __init__(self, root):

        
        #Drop Down menu options - this is gonna be filled with files from the server
        self.options = [
        'Select a file',
        ] 

        #File Vars
        self.file_path = ""
        self.file_name = "None"

        #GUI initialization
        self.root = root
        self.root.title("Directory of GUI")
        self.root.geometry("300x200")
        
                
        self.file_label = tk.Label(root,text="Selected file to load:")
        self.file_label.pack(pady=2)
        
        #Button for loading the file
        self.load_button = tk.Button(root, text="Load File", command=self.load_file)
        self.load_button.pack(pady=2)
        
        #Button for sending the file
        self.load_button = tk.Button(root, text="Send File")
        self.load_button.pack(pady=2)

        #OptionMenu for selecting the day of the week
        self.selected_day = StringVar(root)
        self.selected_day.set(self.options[0])  #Default selection
        self.day_menu = OptionMenu(root, self.selected_day, *self.options)
        self.day_menu.pack(pady=2)

    def load_file(self):
        #Clears any previous files
        self.file_path = ""
        self.file_name = ""
        
        #Call file finder and name getter methods
        self.file_finder()
        if self.file_path:
            
            #Insert Code to send the file off here
            
            self.name_getter()
            self.file_label.config(text="Selected file: " + self.file_name)
            print(f"Selected file: {self.file_name}")
        else:
            print("No file selected.")
        
    def file_finder(self):
        #Opens file dialog and gets the file path
        self.file_path = askopenfilename(initialdir="/", title="Select File", filetypes=(
       ("Text Files", "*.txt"), ("MP4 Files", "*.mp4"), ("MP3 Files", "*.mp3")))
        
    def name_getter(self):
        #Extracts the file name from the file path
        if self.file_path:
            self.file_name = self.file_path.split("/")[-1]

if __name__ == "__main__":
    root = tk.Tk()
    app = View(root)
    root.mainloop()