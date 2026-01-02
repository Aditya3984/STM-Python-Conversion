from tkinter import *
import tkinter as tk
import subprocess
import sys


root = tk.Tk()
root.title("STM_View4")
root.geometry("300x200")
menu= tk.Menu(root)
root.config(menu=menu)


loaddatamenu = tk.Menu(menu, tearoff=0)
copydatamenu = tk.Menu(menu, tearoff=0)


#User Defined Function That Opens "Open_File.py"
def open_stm1():
    subprocess.Popen([sys.executable, "Open_file.py"])


#Making Submenu for the menu Load_data
menu.add_cascade(label='Load Data', menu=loaddatamenu)
loaddatamenu.add_command(label='Open File' , command=open_stm1)
loaddatamenu.add_command(label='Load From Workspace')
loaddatamenu.add_command(label='TBD')


#Making Menu CopyData
menu.add_cascade(label='Copy Data', menu=copydatamenu)

root.mainloop()
