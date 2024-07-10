# File-Cleaner
Python program to clean downloads folder and help you delete or move files
Explanation of diferent PY files
file_manager.py
Imports:

import os: Provides a way of using operating system dependent functionality like reading or writing to the file system.
import shutil: Allows file operations such as copying and moving files.
from collections import defaultdict: Provides a dictionary-like class that defaults missing keys to a default value (in this case, a list).
FileManager Class:

class FileManager:: Defines a class named FileManager to encapsulate file management operations.
def __init__(self, download_folder):: Constructor method that initializes the class with a download_folder and a files attribute.
self.files = defaultdict(list): Initializes files as a dictionary where each key maps to a list of file paths.
scan_files Method:

for root, _, files in os.walk(self.download_folder):: Walks through the directory tree starting at download_folder.
for file in files:: Iterates over each file in the current directory.
file_path = os.path.join(root, file): Joins the directory path and file name to get the full file path.
file_ext = os.path.splitext(file)[1].lower(): Extracts the file extension and converts it to lowercase.
self.files[file_ext].append(file_path): Adds the file path to the list for the corresponding file extension.
organize_files Method:

for ext, files in self.files.items():: Iterates over each file extension and its corresponding list of files.
files.sort(): Sorts the list of files in place.
move_file Method:

if not os.path.exists(dest_folder):: Checks if the destination folder exists.
os.makedirs(dest_folder): Creates the destination folder if it does not exist.
shutil.move(file_path, dest_folder): Moves the file to the destination folder.
delete_file Method:

os.remove(file_path): Deletes the specified file.

gui.py
Imports:

import tkinter as tk: Imports the tkinter module for creating the GUI.
from tkinter import filedialog, messagebox: Imports specific components from tkinter for file dialogs and message boxes.
from file_manager import FileManager: Imports the FileManager class from file_manager.py.
from PIL import Image, ImageTk: Imports the Pillow library for handling images in the GUI.
FileOrganizerApp Class:

class FileOrganizerApp:: Defines a class named FileOrganizerApp to encapsulate the GUI application.
def __init__(self, root):: Constructor method that initializes the class with a root window and calls create_widgets.
self.root = root: Sets the root attribute to the passed-in root window.
self.file_manager = None: Initializes file_manager to None.
self.create_widgets(): Calls the method to create the GUI widgets.
create_widgets Method:

self.root.title("File Organizer"): Sets the window title.
self.root.geometry("600x400"): Sets the window size.
self.label = tk.Label(self.root, text="Select Download Folder"): Creates a label widget.
self.label.pack(pady=20): Packs the label with padding.
self.select_button = tk.Button(self.root, text="Browse", command=self.browse_folder): Creates a button widget for browsing folders.
self.select_button.pack(pady=10): Packs the button with padding.
self.listbox = tk.Listbox(self.root): Creates a listbox widget to display files.
self.listbox.pack(pady=20, fill=tk.BOTH, expand=True): Packs the listbox with padding and allows it to expand.
self.move_button = tk.Button(self.root, text="Move Selected File", command=self.move_file): Creates a button widget for moving files.
self.move_button.pack(side=tk.LEFT, padx=10, pady=10): Packs the button with padding and aligns it to the left.
self.delete_button = tk.Button(self.root, text="Delete Selected File", command=self.delete_file): Creates a button widget for deleting files.
self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10): Packs the button with padding and aligns it to the right.
browse_folder Method:

folder = filedialog.askdirectory(): Opens a dialog to select a directory.
if folder:: Checks if a folder was selected.
self.file_manager = FileManager(folder): Initializes file_manager with the selected folder.
self.file_manager.scan_files(): Scans files in the selected folder.
self.file_manager.organize_files(): Organizes the scanned files.
self.populate_listbox(): Populates the listbox with the scanned files.
populate_listbox Method:

self.listbox.delete(0, tk.END): Clears the listbox.
for ext, files in self.file_manager.files.items():: Iterates over each file extension and its corresponding list of files.
for file in files:: Iterates over each file in the list.
self.listbox.insert(tk.END, file): Inserts the file path into the listbox.
move_file Method:

selected = self.listbox.curselection(): Gets the currently selected file in the listbox.
if selected:: Checks if a file is selected.
file_path = self.listbox.get(selected): Gets the file path of the selected file.
dest_folder = filedialog.askdirectory(): Opens a dialog to select a destination folder.
if dest_folder:: Checks if a destination folder was selected.
self.file_manager.move_file(file_path, dest_folder): Moves the selected file to the destination folder.
self.populate_listbox(): Updates the listbox after moving the file.
delete_file Method:

selected = self.listbox.curselection(): Gets the currently selected file in the listbox.
if selected:: Checks if a file is selected.
file_path = self.listbox.get(selected): Gets the file path of the selected file.
confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this file?"): Opens a confirmation dialog.
if confirm:: Checks if the user confirmed the deletion.
self.file_manager.delete_file(file_path): Deletes the selected file.
self.populate_listbox(): Updates the listbox after deleting the file.
Main Script:

if __name__ == "__main__":: Checks if the script is being run directly.
root = tk.Tk(): Creates the root window.
app = FileOrganizerApp(root): Initializes the FileOrganizerApp with the root window.
root.mainloop(): Starts the tkinter main event loop.
main.py
Imports:

from gui import FileOrganizerApp: Imports the FileOrganizerApp class from gui.py.
import tkinter as tk: Imports the tkinter module for creating the GUI.
Main Script:

if __name__ == "__main__":: Checks if the script is being run directly.
root = tk.Tk(): Creates the root window.
app = FileOrganizerApp(root): Initializes the FileOrganizerApp with the root window.
root.mainloop(): Starts the tkinter main event loop.
