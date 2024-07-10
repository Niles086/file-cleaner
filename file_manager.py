import os
import shutil
from collections import defaultdict

class FileManager:
    def __init__(self, download_folder):
        self.download_folder = download_folder
        self.files = defaultdict(list)
        self.file_sizes = {}  # Initialize file_sizes attribute

    def scan_files(self):
        for root, _, files in os.walk(self.download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                file_size = os.path.getsize(file_path)
                self.files[file_ext].append(file_path)
                self.file_sizes[file_path] = file_size

    def organize_files(self):
        for ext, files in self.files.items():
            files.sort()

    def move_file(self, file_path, dest_folder):
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        shutil.move(file_path, dest_folder)
        if file_path in self.file_sizes:
            del self.file_sizes[file_path]

    def delete_file(self, file_path):
        os.remove(file_path)
        if file_path in self.file_sizes:
            del self.file_sizes[file_path]
