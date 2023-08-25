from PIL import Image, ImageTk
import random
import numpy as np
import math
from texture import texture
import tkinter as tk

def on_tile(xcoord , ycoord, vectorA, vectorB, box_list, multiplier):



        
    posL = np.linalg.solve(((vectorA[0],vectorB[0]),(vectorA[1],vectorB[1])),(ycoord,xcoord))

    xBox = math.floor(posL[1]) - multiplier[0] * math.floor(posL[0])
    yBox = math.floor(posL[0]) - multiplier[1] * math.floor(posL[1])

    if xBox >= 0 and xBox < len(box_list[0]) and yBox >=0 and yBox <len(box_list) :
        return box_list[len(box_list) - 1 - yBox][xBox], posL[0]%1 , posL[1]%1
    
    return 0 ,0 , 0

def find_image_bounds(vector1, vector2, boxShape):
    right = max(0, vector1[0],vector2[0], vector1[0] + vector2[0]) * boxShape[0]
    left = min(0, vector1[0],vector2[0], vector1[0] + vector2[0]) * boxShape[0] 

    top = max(0, vector1[1],vector2[1], vector1[1] + vector2[1]) * boxShape[1]
    bottom = min(0, vector1[1],vector2[1], vector1[1] + vector2[1]) * boxShape[1]

    xmultiplier = top - bottom 
    ymultiplier = right - left 

    multiplier = max(xmultiplier, ymultiplier)+1
    return multiplier, bottom - 0.5*( multiplier - xmultiplier), left -0.5* (multiplier - ymultiplier)


# Create the array that determines where cubes are
box_list = [[0]*5 for i in range(5)]






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



top_texture = texture((0,255,255))
left_texture = texture((255,255,255))
right_texture = texture((0,0,255))

top_texture.setTexture("brick.jpg")
left_texture.setTexture("portal.jpg")
right_texture.setTexture("test.jpg")



image_width = 500;
image_height = 500;

my_array = np.full((image_height,image_width,3),(0,0,0), dtype=np.ubyte)


Avc1 = (0,1) # vertical vector component
Avc2 = (0.87,-0.5) # horizontal vector component

Bvc1 = Avc1
Bvc2 = (Avc1[0] + Avc2[0], Avc1[1] + Avc2[1])

Cvc1 = Bvc2
Cvc2 = Avc2


print("beginning cubes")

xmultiplier , xoffset, yoffset = find_image_bounds(Avc1,Avc2,(len(Lbox_list[0]),len(Lbox_list)))
ymultiplier = xmultiplier

for xind in range(image_height):
    for yind in range(image_width):
        xcoord = (image_height - xind ) / image_height * xmultiplier + xoffset 
        ycoord = (yind ) / image_width * ymultiplier  + yoffset 


        check, xTilePos, yTilePos = on_tile(xcoord, ycoord, Avc1 , Avc2,Lbox_list, (0,0))


        if check >0 :
            my_array[xind][yind] = left_texture.getColour(xTilePos,yTilePos)
        if check !=2:
            check, xTilePos, yTilePos = on_tile(xcoord - Avc1[1], ycoord - Avc1[0] , Cvc1 , Cvc2,Tbox_list, (-1,0))
            if check >0 :
                my_array[xind][yind] = top_texture.getColour(xTilePos,yTilePos)
        
        if check !=2 :
            check, xTilePos, yTilePos = on_tile(xcoord - Avc2[1], ycoord - Avc2[0], Bvc1 , Bvc2,Rbox_list, (0,-1))
            if check >0 :
                my_array[xind][yind] = right_texture.getColour(xTilePos,yTilePos)        
        


window = tk.Tk()
window.geometry('1000x1000')
im = Image.fromarray(my_array)
tkimage = ImageTk.PhotoImage(im)

label = tk.Label(window , image = tkimage)

label.pack()

window.mainloop()




#im.show()
