import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from client import (
    upload_file,
    download_file,
    delete_file,
    list_directory,
    create_subfolder,
    delete_subfolder,
)
import socket
import threading


class View:
    def __init__(self, root):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 3300))

        # File vars
        self.file_path = ""
        self.file_name = "None"

        # GUI initialization
        self.root = root
        self.root.title("File Manager GUI")
        self.root.geometry("400x300")

        # Selected file label
        self.file_label = tk.Label(root, text="No file selected.")
        self.file_label.pack(pady=5)

        # Status label for feedback
        self.status_label = tk.Label(root, text="", fg="green")
        self.status_label.pack(pady=5)

        # Buttons for file operations
        self.load_button = tk.Button(root, text="Select File to Upload", command=self.load_file)
        self.load_button.pack(pady=5)

        self.upload_button = tk.Button(root, text="Upload Selected File", command=self.upload_file)
        self.upload_button.pack(pady=5)

        self.download_button = tk.Button(root, text="Download File", command=self.download_file)
        self.download_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete File", command=self.delete_file)
        self.delete_button.pack(pady=5)

        self.dir_button = tk.Button(root, text="View Directory", command=self.view_directory)
        self.dir_button.pack(pady=5)

        self.create_folder_button = tk.Button(root, text="Create Subfolder", command=self.create_folder)
        self.create_folder_button.pack(pady=5)

        self.delete_folder_button = tk.Button(root, text="Delete Subfolder", command=self.delete_folder)
        self.delete_folder_button.pack(pady=5)

    def update_status(self, message, error=False):
        """Update the status message in the GUI (run on the main thread)."""
        self.root.after(0, self._update_status, message, error)

    def _update_status(self, message, error=False):
        """Actual status update method (to be called on the main thread)."""
        self.status_label.config(text=message, fg="red" if error else "green")

    def load_file(self):
        """Load a file from the system to be uploaded."""
        self.file_path = askopenfilename(
            initialdir="/",
            title="Select File",
            filetypes=(("All Files", "*.*"), ("Text Files", "*.txt"), ("Video Files", "*.mp4"), ("Audio Files", "*.mp3")),
        )
        if self.file_path:
            self.file_name = self.file_path.split("/")[-1]
            self.file_label.config(text=f"Selected File: {self.file_name}")
            print(f"Selected File: {self.file_name}")
        else:
            self.file_label.config(text="No file selected.")
            print("No file selected.")

    def upload_file(self):
        """Upload file to server in a separate thread."""
        if self.file_path:
            # Start a background thread for uploading the file
            upload_thread = threading.Thread(target=self.upload_file_thread)
            upload_thread.start()
        else:
            self.update_status("No file selected to upload.", error=True)

    def upload_file_thread(self):
        """Background thread for uploading the file."""
        upload_file(self.client, self.file_path, self)

    def download_file(self):
        """Download file from the server in a separate thread."""
        file_name = simpledialog.askstring("Download File", "Enter the file name to download:")
        if not file_name:
            return
        save_path = asksaveasfilename(
            initialdir="/", title="Save File As", filetypes=(("All Files", "*.*"),)
        )
        if save_path:
            # Start a background thread for downloading the file
            download_thread = threading.Thread(target=self.download_file_thread, args=(file_name, save_path))
            download_thread.start()

    def download_file_thread(self, file_name, save_path):
        """Background thread for downloading the file."""
        download_file(self.client, file_name, save_path)

    def delete_file(self):
        """Delete a file from the server in a separate thread."""
        file_name = simpledialog.askstring("Delete File", "Enter the file name to delete:")
        if not file_name:
            return
        # Start a background thread for deleting the file
        delete_thread = threading.Thread(target=self.delete_file_thread, args=(file_name,))
        delete_thread.start()

    def delete_file_thread(self, file_name):
        """Background thread for deleting the file."""
        delete_file(self.client, file_name)

    def view_directory(self):
        """View the directory structure of the server in a separate thread."""
        # Start a background thread for viewing the directory
        dir_thread = threading.Thread(target=self.view_directory_thread)
        dir_thread.start()

    def view_directory_thread(self):
        """Background thread for viewing the directory."""
        list_directory(self.client)
        response = self.client.recv(4096).decode()
        self.root.after(0, messagebox.showinfo, "Server Directory", response)

    def create_folder(self):
        """Create a subfolder on the server in a separate thread."""
        folder_name = simpledialog.askstring("Create Subfolder", "Enter the subfolder path to create:")
        if not folder_name:
            return
        # Start a background thread for creating the subfolder
        create_folder_thread = threading.Thread(target=self.create_folder_thread, args=(folder_name,))
        create_folder_thread.start()

    def create_folder_thread(self, folder_name):
        """Background thread for creating the subfolder."""
        create_subfolder(self.client, folder_name)

    def delete_folder(self):
        """Delete a subfolder on the server in a separate thread."""
        folder_name = simpledialog.askstring("Delete Subfolder", "Enter the subfolder path to delete:")
        if not folder_name:
            return
        # Start a background thread for deleting the subfolder
        delete_folder_thread = threading.Thread(target=self.delete_folder_thread, args=(folder_name,))
        delete_folder_thread.start()

    def delete_folder_thread(self, folder_name):
        """Background thread for deleting the subfolder."""
        delete_subfolder(self.client, folder_name)


>>>>>>> Stashed changes
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

        #OptionMenu for
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