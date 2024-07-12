import tkinter as tk
from tkinter import filedialog, messagebox
from file_manager import FileManager
from PIL import Image, ImageTk
import fitz  # PyMuPDF
import io
import os
import shutil
import zipfile
import time
from system_monitor import SystemMonitor  # Import the system monitor

class FileOrganizerApp:
    def __init__(self, root, logo_path):
        self.root = root
        self.file_manager = None
        self.img = None  # To keep a reference to the displayed image
        self.logo_path = logo_path  # Path to the logo image
        self.create_widgets()

    def create_widgets(self):
        self.root.title("File Organizer")
        self.root.geometry("900x700")
        self.root.configure(bg='#2e2e2e')  # Set the background color of the root window to dark

        self.top_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.top_frame.pack(pady=10)

        self.label = tk.Label(self.top_frame, text="Select Download Folder", bg='#2e2e2e', fg='white')
        self.label.pack(side=tk.LEFT, padx=10)

        self.select_button = tk.Button(self.top_frame, text="Browse", command=self.browse_folder, bg='#3e3e3e', fg='white')
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.refresh_button = tk.Button(self.top_frame, text="Refresh", command=self.refresh_screen, bg='#3e3e3e', fg='white')
        self.refresh_button.pack(side=tk.LEFT, padx=10)

        self.system_monitor_button = tk.Button(self.top_frame, text="System Monitor", command=self.open_system_monitor, bg='#3e3e3e', fg='white')
        self.system_monitor_button.pack(side=tk.LEFT, padx=10)

        self.action_var = tk.StringVar(value="Rename")
        self.action_menu = tk.OptionMenu(self.top_frame, self.action_var, "Rename", "Move", "Copy", "Delete", "Search", "Zip")
        self.action_menu.config(bg='#3e3e3e', fg='white')
        menu = self.action_menu.nametowidget(self.action_menu.menuname)
        menu.config(bg='#3e3e3e', fg='white')
        self.action_menu.pack(side=tk.LEFT, padx=10)

        self.input_entry = tk.Entry(self.top_frame, width=40, bg='#3e3e3e', fg='white', insertbackground='white')
        self.input_entry.pack(side=tk.LEFT, padx=10)

        self.action_button = tk.Button(self.top_frame, text="Perform Action", command=self.perform_action, bg='#3e3e3e', fg='white')
        self.action_button.pack(side=tk.LEFT, padx=10)

        self.frame = tk.Frame(self.root, bg='#2e2e2e')
        self.frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(self.frame, width=80, bg='#3e3e3e', fg='white', selectbackground='#555555', selectforeground='white')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_file_select)  # Bind the listbox selection to the on_file_select method

        self.scrollbar = tk.Scrollbar(self.frame, command=self.listbox.yview, bg='#2e2e2e')
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.logo_frame = tk.Frame(self.root, bg='#2e2e2e')
        self.logo_frame.pack(pady=10, side=tk.BOTTOM)

        self.logo_label = tk.Label(self.logo_frame, bg='#2e2e2e')
        self.logo_label.pack()

        self.load_logo()

    def load_logo(self):
        if os.path.exists(self.logo_path):
            logo_image = Image.open(self.logo_path)
            logo_image = logo_image.resize((600, 100), Image.LANCZOS)  # Adjust size as needed
            self.logo_img = ImageTk.PhotoImage(logo_image)
            self.logo_label.config(image=self.logo_img)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.file_manager = FileManager(folder)
            self.file_manager.scan_files()
            self.file_manager.organize_files()
            self.populate_listbox()

    def refresh_screen(self):
        # Refresh the screen by repopulating the listbox
        if self.file_manager:
            self.file_manager.scan_files()
            self.file_manager.organize_files()
            self.populate_listbox()

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for ext, files in self.file_manager.files.items():
            for file in files:
                file_size = self.file_manager.file_sizes.get(file, 0)
                display_text = f"{file} ({self.format_size(file_size)})"
                self.listbox.insert(tk.END, display_text)

    def format_size(self, size):
        # Helper function to format file sizes
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024

    def show_preview(self, event):
        selected = self.listbox.curselection()
        if selected:
            file_info = self.listbox.get(selected)
            file_path = file_info.split(" (")[0]
            ext = file_path.lower().split('.')[-1]

            if ext in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                image = Image.open(file_path)
                image = image.resize((600, 400), Image.LANCZOS)
                self.img = ImageTk.PhotoImage(image)
                self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            elif ext == 'pdf':
                doc = fitz.open(file_path)
                page = doc.load_page(0)  # Load the first page
                pix = page.get_pixmap()
                img_data = pix.tobytes("ppm")
                image = Image.open(io.BytesIO(img_data))
                image = image.resize((600, 400), Image.LANCZOS)
                self.img = ImageTk.PhotoImage(image)
                self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
            else:
                messagebox.showinfo("Preview not available", "Preview not available for this file type.")
            
            # Display file properties
            self.show_file_properties(file_path)

    def perform_action(self):
        action = self.action_var.get()
        if action == "Rename":
            self.rename_file()
        elif action == "Move":
            self.move_file()
        elif action == "Copy":
            self.copy_file()
        elif action == "Delete":
            self.delete_file()
        elif action == "Search":
            self.search_files()
        elif action == "Zip":
            self.zip_files()

    def move_file(self):
        selected = self.listbox.curselection()
        if selected:
            dest_folder = self.input_entry.get()
            if dest_folder:
                for index in selected:
                    file_info = self.listbox.get(index)
                    file_path = file_info.split(" (")[0]
                    self.file_manager.move_file(file_path, dest_folder)
                self.populate_listbox()

    def delete_file(self):
        selected = self.listbox.curselection()
        if selected:
            confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected files?")
            if confirm:
                for index in selected:
                    file_info = self.listbox.get(index)
                    file_path = file_info.split(" (")[0]
                    self.file_manager.delete_file(file_path)
                self.populate_listbox()

    def rename_file(self):
        selected = self.listbox.curselection()
        if selected:
            new_name = self.input_entry.get()
            if new_name:
                file_info = self.listbox.get(selected)
                file_path = file_info.split(" (")[0]
                new_path = os.path.join(os.path.dirname(file_path), new_name)
                os.rename(file_path, new_path)
                self.populate_listbox()

    def copy_file(self):
        selected = self.listbox.curselection()
        if selected:
            dest_folder = self.input_entry.get()
            if dest_folder:
                for index in selected:
                    file_info = self.listbox.get(index)
                    file_path = file_info.split(" (")[0]
                    shutil.copy(file_path, dest_folder)
                self.populate_listbox()

    def search_files(self):
        query = self.input_entry.get().lower()
        if self.file_manager and query:
            self.listbox.delete(0, tk.END)
            for ext, files in self.file_manager.files.items():
                for file in files:
                    if query in file.lower():
                        file_size = self.file_manager.file_sizes.get(file, 0)
                        display_text = f"{file} ({self.format_size(file_size)})"
                        self.listbox.insert(tk.END, display_text)

    def zip_files(self):
        selected = self.listbox.curselection()
        if selected:
            zip_filename = self.input_entry.get()
            if zip_filename:
                if not zip_filename.endswith('.zip'):
                    zip_filename += '.zip'
                zip_destination = filedialog.askdirectory()
                if zip_destination:
                    zip_filepath = os.path.join(zip_destination, zip_filename)  # Save the zip file to the selected directory
                    try:
                        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                            for index in selected:
                                file_info = self.listbox.get(index)
                                file_path = file_info.split(" (")[0]
                                zipf.write(file_path, os.path.basename(file_path))
                        messagebox.showinfo("Zip Files", f"Files zipped successfully to {zip_filepath}!")
                    except Exception as e:
                        messagebox.showerror("Error", f"An error occurred while zipping files: {e}")

    def toggle_dark_mode(self):
        if self.root["bg"] == "black":
            self.root.config(bg="white")
            self.preview_canvas.config(bg="white")
        else:
            self.root.config(bg="black")
            self.preview_canvas.config(bg="black")

    def apply_filter(self):
        filter_type = self.filter_var.get()
        self.listbox.delete(0, tk.END)
        for ext, files in self.file_manager.files.items():
            for file in files:
                if filter_type == "All" or (filter_type == "Images" and ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']) or (filter_type == "PDFs" and ext == '.pdf'):
                    file_size = self.file_manager.file_sizes.get(file, 0)
                    display_text = f"{file} ({self.format_size(file_size)})"
                    self.listbox.insert(tk.END, display_text)

    def show_file_properties(self, file_path):
        file_size = os.path.getsize(file_path)
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        properties = f"Size: {self.format_size(file_size)}\nCreated: {time.ctime(creation_time)}\nModified: {time.ctime(modification_time)}"
        messagebox.showinfo("File Properties", properties)

    def on_file_select(self, event):
        selected = self.listbox.curselection()
        if selected:
            file_info = self.listbox.get(selected)
            file_path = file_info.split(" (")[0]
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, os.path.basename(file_path))

    def open_system_monitor(self):
        SystemMonitor(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    logo_path = r"P:\personalPythonProjects\fileCleaner\logo.png"  # Path to your company logo
    app = FileOrganizerApp(root, logo_path)
    root.mainloop()
