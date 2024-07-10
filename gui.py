import tkinter as tk
from tkinter import filedialog, messagebox
from file_manager import FileManager
from PIL import Image, ImageTk

class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.file_manager = None
        self.create_widgets()

    def create_widgets(self):
        self.root.title("File Organizer")
        self.root.geometry("800x600")

        self.label = tk.Label(self.root, text="Select Download Folder")
        self.label.pack(pady=20)

        self.select_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.select_button.pack(pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame, width=80)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.move_button = tk.Button(self.root, text="Move Selected File", command=self.move_file)
        self.move_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Selected File", command=self.delete_file)
        self.delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.file_manager = FileManager(folder)
            self.file_manager.scan_files()
            self.file_manager.organize_files()
            self.populate_listbox()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for ext, files in self.file_manager.files.items():
            for file in files:
                file_size = self.file_manager.file_sizes[file]
                display_text = f"{file} ({self.format_size(file_size)})"
                self.listbox.insert(tk.END, display_text)

    def format_size(self, size):
        # Helper function to format file sizes
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    def move_file(self):
        selected = self.listbox.curselection()
        if selected:
            file_info = self.listbox.get(selected)
            file_path = file_info.split(" (")[0]
            dest_folder = filedialog.askdirectory()
            if dest_folder:
                self.file_manager.move_file(file_path, dest_folder)
                self.populate_listbox()

    def delete_file(self):
        selected = self.listbox.curselection()
        if selected:
            file_info = self.listbox.get(selected)
            file_path = file_info.split(" (")[0]
            confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this file?")
            if confirm:
                self.file_manager.delete_file(file_path)
                self.populate_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
