import os
#Import os Provides a way of using operating system dependent functionality like reading or writing to the file system.
import shutil
#Import shutil Allows file operations such as copying and moving files.
from collections import defaultdict
#from collections import defaultdict Provides a dictionary-like class that defaults missing keys to a default value (in this case, a list).


#Class to handle file management class

class FileManager:
    def __init__(self, download_folder):
        self.download_folder = download_folder
        self.files = defaultdict(list)
<<<<<<< HEAD
        self.file_sizes = {}  # Initialize file_sizes attribute
=======
        self.file_sizes = {}

# Method to scan all files in the download folder
>>>>>>> da2b3503fa7027b94b0321b9a607baea5e9ab7c6

    def scan_files(self):
        for root, _, files in os.walk(self.download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                file_size = os.path.getsize(file_path)
                self.files[file_ext].append(file_path)
                self.file_sizes[file_path] = file_size

<<<<<<< HEAD
=======
#Method to organize files by their extensions

>>>>>>> da2b3503fa7027b94b0321b9a607baea5e9ab7c6
    def organize_files(self):
        for ext, files in self.files.items():
            files.sort()

    def move_file(self, file_path, dest_folder):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(file_path, dest_folder)
<<<<<<< HEAD
        if file_path in self.file_sizes:
            del self.file_sizes[file_path]

    def delete_file(self, file_path):
        os.remove(file_path)
        if file_path in self.file_sizes:
            del self.file_sizes[file_path]
=======

# Method to delete files
    def delete_file(self, file_path):
        os.remove(file_path)
        if file_path in self.file_sizes:
            del self.file_sizes[file_path]
>>>>>>> da2b3503fa7027b94b0321b9a607baea5e9ab7c6
