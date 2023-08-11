from PIL import Image
import random
import numpy as np
import math

def on_tile(xcoord , ycoord, vectorA, vectorB, box_list, multiplier):



        
    posL = np.linalg.solve(((vectorA[0],vectorB[0]),(vectorA[1],vectorB[1])),(ycoord,xcoord))

    xBox = math.floor(posL[1]) - multiplier[0] * math.floor(posL[0])
    yBox = math.floor(posL[0]) - multiplier[1] * math.floor(posL[1])

    if xBox >= 0 and xBox <= 4 and yBox >=0 and yBox <=4 :
        return box_list[4 - yBox][xBox]
    
    return 0


# Create the array that determines where cubes are
box_list = [[0]*5 for i in range(5)]
##box_count = 0
##for x in range(5):
##    for y in range(5):
##        if random.randint(0,1) == 1:
##            box_list[x][y] = 1
##            box_count += 1;



##box_count = 18
##cube_list = [[0]*2 for i in range(box_count)]
##box_index = 0
##for x in range(5):
##    for y in range(5):
##        if box_list[x][y] == 1:
##            cube_list[box_count - box_index - 1][0] = x
##            cube_list[box_count - box_index - 1][1]= y
##            box_index +=1

Lbox_list = [[1,2,1,1,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0],
            [1,0,0,0,0]]

Rbox_list = [[0,0,0,0,1],
            [1,0,0,1,0],
            [1,0,1,0,0],
            [1,1,0,0,0],
            [1,0,0,0,0]]

Tbox_list = [[1,1,1,1,1],
            [0,0,0,1,0],
            [0,0,1,0,0],
            [0,1,0,0,0],
            [0,0,0,0,0]]





image_width = 100;
image_height = 100;

my_array = np.full((image_height,image_width,3),(0,0,0), dtype=np.ubyte)


Avc1 = (0,1)
Avc2 = (1,0.2)

Bvc1 = (0,1)
Bvc2 = (1,1.2)

Cvc1 = (1, 1.2)
Cvc2 = (1, 0.2)


print("beginning cubes")

for xind in range(image_height):
    for yind in range(image_width):
        xcoord = (image_height - xind ) / image_height * 9 -1
        ycoord = (yind ) / image_width * 9 -1


        check = on_tile(xcoord, ycoord, Avc1 , Avc2,Lbox_list, (0,0))


        if check >0 :
            my_array[xind][yind] = (255,255,255)
        if check !=2 and   on_tile(xcoord - 1, ycoord , Cvc1 , Cvc2,Tbox_list, (-1,0)):
            my_array[xind][yind] = (0,255,255)
        
        if check !=2 and   on_tile(xcoord - 0.2, ycoord - 1, Bvc1 , Bvc2,Rbox_list, (0,-1)):
            my_array[xind][yind] = (0,0,255)
        
        



im = Image.fromarray(my_array)

im.show()
