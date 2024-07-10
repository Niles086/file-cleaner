# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:37:28 2024

@author: NilesThompson
"""

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

# Method to scan all files in the download folder

    def scan_files(self):
        for root, _, files in os.walk(self.download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                self.files[file_ext].append(file_path)

#Method to organize files by their extensions

    def organize_files(self):
        for ext, files in self.files.items():
            files.sort()

#Method to move files to a new destination
    def move_file(self, file_path, dest_folder):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(file_path, dest_folder)

# Method to delete files
    def delete_file(self, file_path):
        os.remove(file_path)