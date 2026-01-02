from tkinter import *
import tkinter as tk
from tkinter import filedialog
import numpy as np
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




#===========================================================================
#              POLYNOMIAL FITTING/BACKGROUND SUBSTRACTION
#===========================================================================

#sy = number of pixels along y-direction (rows)
#sx = number of pixels along x-direction (columns)
#np.arange(1, sy + 1) = Create an array from 1 to sy
#np.repeat(... , sx) = Repeats each y value sx times i.e. y becomes a 1D array of length sy * sx .Each pixel now has a corresponding row index
#np.title(... , sy) = Repeats the entire array sy times i.e. x is also a 1D array of length sy * sx

def prep_topo(topo):    #It takes one argument: topo → a 2D NumPy array representing a topography image (e.g., STM height data)
    sy, sx = topo.shape      #topo.shape returns (number_of_rows, number_of_columns)
    
    #-----------Create Y-coordinate array----------
    y = np.repeat(np.arange(1, sy + 1), sx)   
    
    #-----------Create X-coordinate array----------
    x = np.tile(np.arange(1, sx + 1), sy)     
    z = topo.reshape(-1)

    A = np.column_stack([
        np.ones_like(x),
        x,
        y,
        x * y,
        x**2,
        y**2,
        x**3,
        y**3
    ])

    coeffs, _, _, _ = np.linalg.lstsq(A, z, rcond=None)
    z_corr = z - (A @ coeffs)
    return z_corr.reshape(sy, sx)   #.reshape changes the 1D array into sy*sx matrix






#=============================================================
#                         LOAD FILE
#=============================================================
def open_file(path):
    global orig_xlim, orig_ylim, cbar , current_data
    
    if not path:
        return

    topo = np.loadtxt(path)
    topo_corr = prep_topo(topo)
    current_data = topo_corr 


    ax.clear()
    im = ax.imshow(topo_corr, cmap="gray", origin="lower")
    ax.set_title("Polynomial Fitted STM Image" , size=10)
   
    # Remove old colorbar
    if cbar is not None:
        cbar.remove()

    cbar = fig.colorbar(im, ax=ax, label="Height")

    # Store original limits AFTER plotting
    orig_xlim = (0, topo.shape[1])
    orig_ylim = (0, topo.shape[0])


    ax.set_xlim(orig_xlim)
    ax.set_ylim(orig_ylim)

    canvas.draw_idle()
    
    
    


#==============================================================
#                   ZOOM FUNCTION (CLAMPED) 
#==============================================================
def zoom(event):
    ax = event.inaxes   #Identifies which axis the mouse is currently over
    if ax is None:      #If the mouse is not inside the image, do nothing
        return

    x_min, x_max = ax.get_xlim()   #Gets the currently visible region
    y_min, y_max = ax.get_ylim()

    scale_factor = 1.1  #It increases zoom size by 10%
    if event.button == 'up':      # zoom in
        scale_factor = 1 / scale_factor
    elif event.button == 'down':  # zoom out
        scale_factor = scale_factor
    else:
        return

    xdata = event.xdata        #These are data coordinates under the mouse, Zoom occurs around the cursor
    ydata = event.ydata

    new_xmin = xdata + (x_min - xdata) * scale_factor
    new_xmax = xdata + (x_max - xdata) * scale_factor
    new_ymin = ydata + (y_min - ydata) * scale_factor
    new_ymax = ydata + (y_max - ydata) * scale_factor

    # -------- CLAMP TO ORIGINAL IMAGE SIZE --------
    new_xmin = max(new_xmin, orig_xlim[0])   #Prevents zooming left past the original image
    new_xmax = min(new_xmax, orig_xlim[1])   #Prevents zooming right past the original image
    new_ymin = max(new_ymin, orig_ylim[0])   #Prevents zooming upward beyond the image
    new_ymax = min(new_ymax, orig_ylim[1])  

    ax.set_xlim(new_xmin, new_xmax)
    ax.set_ylim(new_ymin, new_ymax)
    canvas.draw_idle()
    
    
    
    
    
#===========================================================
#                MOUSE COORDINATE DISPLAY 
#===========================================================
def on_mouse_move(event):
      if event.inaxes != ax or current_data is None:
          return

      x = int(event.xdata)
      y = int(event.ydata)

      if (x < 0 or y < 0 or
          x >= current_data.shape[1] or
          y >= current_data.shape[0]):
          return

      z = current_data[y, x]

      coord_label.config( text=f"x: {x}   y: {y}   z: {z:.3f}" )  
    
    
    
    


#=======================================================================
#                              RESET VIEW
#=======================================================================
def reset_view():
    ax.set_xlim(orig_xlim)
    ax.set_ylim(orig_ylim)
    canvas.draw_idle()




#========================================================================
#                                 GUI
#========================================================================
fig = Figure(figsize=(6, 6))
ax = fig.add_subplot(111)
root = tk.Tk()
root.title("STM Image Viewer")
root.geometry("400x300")
menu= tk.Menu(root)
root.config(menu=menu)


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
coord_label = tk.Label(root, text="x: -, y: -, z: -", anchor="w")
coord_label.pack(fill=tk.X)

# ------------------ Event Connections ------------------
canvas.mpl_connect("scroll_event", zoom)
canvas.mpl_connect("motion_notify_event", on_mouse_move)
last_x, last_y = None, None


# ------------------ Reset Button ------------------
btn = tk.Button(root, text="Reset Zoom", command=reset_view)
btn.pack(pady=5)


# Globals
orig_xlim = (0, 1)
orig_ylim = (1, 0)
cbar = None
current_data = None

# -------- Load file from command line --------
open_file(sys.argv[1])







#-----------------Defining all the required menu-----------------------
filemenu = tk.Menu(menu, tearoff=0)
dispmenu = tk.Menu(menu, tearoff=0)
processmenu = tk.Menu(menu, tearoff=0)
averagemenu= tk.Menu(processmenu, tearoff=0)
cropmenu= tk.Menu(menu, tearoff=0)
bgsubsmenu= tk.Menu(menu, tearoff=0)
filtmenu= tk.Menu(menu, tearoff=0)
mathmenu= tk.Menu(menu, tearoff=0)
imgmanimenu= tk.Menu(menu, tearoff=0)
copydatamenu= tk.Menu(menu, tearoff=0)
analysismenu= tk.Menu(menu, tearoff=0)
correlmenu= tk.Menu(analysismenu, tearoff=0)
bsccomenu= tk.Menu(analysismenu, tearoff=0)
nemamenu= tk.Menu(analysismenu, tearoff=0)

#Making the Save Menu
menu.add_cascade(label='Save', menu=filemenu)
filemenu.add_cascade(label='Put On Workspace')
filemenu.add_cascade(label='Save Layer To Workspace')
filemenu.add_cascade(label='Save Zoomed Layer To Workspace')
filemenu.add_cascade(label='Export Movie')
filemenu.add_cascade(label='Export Images')

#Making the Display Menu
menu.add_cascade(label='Display', menu=dispmenu)
dispmenu.add_cascade(label='Select Pallete')
dispmenu.add_cascade(label='Plot Color Bar')
dispmenu.add_cascade(label='Adjust Histogram')
dispmenu.add_cascade(label='Invert Color Scale')
dispmenu.add_cascade(label='Spectrum Viewer')
dispmenu.add_cascade(label='Line Cut Viewer')
dispmenu.add_cascade(label='Dynes Fit Viewer')
dispmenu.add_cascade(label='Gap Viewer')
dispmenu.add_cascade(label='Show Average Spectrum')


#Making the Process Menu
menu.add_cascade(label='Process', menu=processmenu)
processmenu.add_cascade(label='Averaging', menu=averagemenu)
averagemenu.add_command(label='Energy Car-Box Average')
averagemenu.add_command(label='4 Pixel Average')

#Making Nested Crop Menu
processmenu.add_cascade(label='Crop', menu=cropmenu)
cropmenu.add_command(label='Crop By Coordinates')
cropmenu.add_command(label='Crop Current FOV')

#Making Nested CPD Menu 
processmenu.add_cascade(label='Change Pixel Dimension')
processmenu.add_cascade(label='Rotate Map')
processmenu.add_cascade(label='Line Cut')

#Making Nestd BGS Menu
processmenu.add_cascade(label='Background Substraction', menu=bgsubsmenu)
bgsubsmenu.add_command(label='0')
bgsubsmenu.add_command(label='1')
bgsubsmenu.add_command(label='2')
bgsubsmenu.add_command(label='3')
bgsubsmenu.add_command(label='4')
bgsubsmenu.add_command(label='5')
bgsubsmenu.add_command(label='6')

#Making Nested Filtering Menu
processmenu.add_cascade(label='Filtering', menu=filtmenu)
filtmenu.add_command(label='Bilateal Filter')
filtmenu.add_command(label='Gaussian Filter')

#Making Nested Math Menu
processmenu.add_cascade(label='Math', menu=mathmenu)
mathmenu.add_command(label='Add/Subtract')
mathmenu.add_command(label='Multiply/Divide')
mathmenu.add_command(label='d/dE')

#Making Nestd IMGM Menu
processmenu.add_cascade(label='Image Manipulation', menu=imgmanimenu)
imgmanimenu.add_command(label='Shear Correct')
imgmanimenu.add_command(label='Symmetrize')
imgmanimenu.add_command(label='(x,y) Gaussian Blur')
imgmanimenu.add_command(label='Remove FT Center')
imgmanimenu.add_command(label='Register')
imgmanimenu.add_command(label='Local Register')

#Making IDO Menu
processmenu.add_cascade(label='Inter-Data Operations')

#Making Nested CDF Menu
processmenu.add_cascade(label='Copy Data From...', menu=copydatamenu)
copydatamenu.add_command(label='GUI Object')
copydatamenu.add_command(label='Workspace')

#Making EL Menu
processmenu.add_cascade(label='Extract Layer')

#Making Analysis Menu
menu.add_cascade(label='Analysis', menu=analysismenu)
analysismenu.add_cascade(label='Centre Of Mass')
analysismenu.add_cascade(label='2D Histogram')
analysismenu.add_cascade(label='Fourier Transform')

#Making Nested Correlation Menu
analysismenu.add_cascade(label='Correlations',menu= correlmenu)
correlmenu.add_command(label='Autocorrelaton')
correlmenu.add_command(label='Cross Correlation')

analysismenu.add_cascade(label='Z-Map')
analysismenu.add_cascade(label='S-Map')

#Making Nested BSCCO Menu
analysismenu.add_cascade(label='BSCCO', menu=bsccomenu)
bsccomenu.add_command(label='Gap Map')
bsccomenu.add_command(label='Omega Map')
bsccomenu.add_command(label='Rescale Energy By Gap')
bsccomenu.add_command(label='Gap Sorted Spectra')
bsccomenu.add_command(label='SM Phase Extraction')
bsccomenu.add_command(label='LF Correct')
bsccomenu.add_command(label='DFF Phase')
bsccomenu.add_command(label='Generate Cu Ox Oy Index')
bsccomenu.add_command(label='LF Correct Map')
bsccomenu.add_command(label='Sublattice Segregration')
bsccomenu.add_command(label='BSCCO Index')

#Making Nested NA Menu
analysismenu.add_cascade(label='Nematicity Analysis', menu=nemamenu)
nemamenu.add_command(label='MNR(r)-r-Space Derived')
nemamenu.add_command(label='MNQ(r)-k-Space Derived')
nemamenu.add_command(label='MNQ(E)')
nemamenu.add_command(label='Nematic Tile 1')
nemamenu.add_command(label='Nematic Tile 2')
nemamenu.add_command(label='Nematic Domain Mean Substraction')
nemamenu.add_command(label='Binary View of Domains')
nemamenu.add_command(label='Average Domain Spectra')



# Start the Tkinter event loop
root.mainloop()