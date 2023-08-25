from PIL import Image, ImageTk
from texture import texture
import tkinter as tk
from impossibleFigure import impossibleFigure



window = tk.Tk()
window.geometry('600x600')

myFigure = impossibleFigure()

Lbox_list =[[0,0,0,0,0,0],
            [0,0,0,0,1,0],
            [0,0,1,0,1,0],
            [0,0,2,0,2,0],
            [0,0,0,0,0,0],
            [1,1,1,1,1,0]]

Rbox_list =[[0,0,0,0,1,0],
            [0,0,0,1,1,0],
            [0,0,1,0,1,0],
            [0,0,1,0,1,0],
            [0,0,0,0,0,1],
            [0,0,0,0,1,0]]

Tbox_list =[[0,0,0,0,1,0],
            [0,0,0,1,0,0],
            [0,0,1,0,0,0],
            [0,0,0,0,0,0],
            [0,1,0,1,0,1],
            [1,1,1,1,1,0]]

myArray = myFigure.getFigure(Lbox_list,Rbox_list,Tbox_list)



im = Image.fromarray(myArray)
tkimage = ImageTk.PhotoImage(im)

label = tk.Label(window , image = tkimage)

label.pack()

window.mainloop()
