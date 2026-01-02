import tkinter as tk
from tkinter import filedialog
import subprocess
import sys

root = tk.Tk()
root.withdraw()   # Hide empty Tk window

#Selects file with extension .TFR , .1FL , .2FL , .1FR
file_path = filedialog.askopenfilename(
    title="Select data file",
    filetypes=(("All File", "*.*"),
        ("TFR Files", "*.TFR"),
        ("1FL Files", "*.1FL"),
        ("2FL Files", "*.2FL"),
        ("FR Files", "*.1FR")
    )
)


#Passes the selected file to "STM_image_viewer"
def selected_file(file_path):
    subprocess.Popen([
        sys.executable,
        "untitled10.py",
        file_path
    ])

if file_path:          # Important safety check
    selected_file(file_path)
  

