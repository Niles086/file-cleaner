# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 11:53:07 2024

@author: NilesThompson
"""

import tkinter as tk
from gui import FileOrganizerApp  

if __name__ == "__main__":
    root = tk.Tk()
    logo_path = r"P:\personalPythonProjects\fileCleaner\logo.png"  # Path to company logo
    app = FileOrganizerApp(root, logo_path)
    root.mainloop()

