from tkinter import *
import tkinter as tk
import subprocess
import sys


root = tk.Tk()
root.title("Choose STM")
root.geometry("400x150")
root.resizable(False,False) # Prevents the window from Maximizing/Resizing


#Creating and writing Label for the window
label = tk.Label(root,
                         text="With which STM was the data taken? (assuming you did \nnot change the filetype manually)",
                         font=("Arial", 9),
                         fg="black")
label.grid(row=0, column=0, columnspan=3, padx=30,pady=10)



def Cancel():
    root.destroy()   #Destroys the window if "Cancel" button is pressed
    
    
#Opens the file "Select_File.py"
def Select_file():
    subprocess.Popen([sys.executable, "Select_File.py"])
    

#Creates Buttons
btn1 = tk.Button(root, text="STM1")
btn2 = tk.Button(root, text="STM2", command=Select_file)
btn3 = tk.Button(root, text="Cancel", command= Cancel)

#Defines the row and column in which buttons are placed
btn1.grid(row=1, column=0, padx=50, pady=20)
btn2.grid(row=1, column=1, padx=40, pady=20)
btn3.grid(row=1, column=2, padx=40, pady=20)


root.mainloop()
