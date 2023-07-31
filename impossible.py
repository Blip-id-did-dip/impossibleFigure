from PIL import Image
import random
import numpy as np


def on_tile(xcoord , ycoord, vectorA, vectorB, vectorC, cube_list):
    #side = -1
    #rel_pos = [-1,-1]
    for cube_index in range(len(cube_list)):
        trueY = ycoord + vectorA[0] * cube_list[cube_index][0] + vectorB[0] * cube_list[cube_index][1]
        trueX = xcoord + vectorA[1] * cube_list[cube_index][0] + vectorB[1] * cube_list[cube_index][1]
        
        posL = np.linalg.solve(((vectorA[0],vectorB[0]),(vectorA[1],vectorB[1])),(trueY,trueX))
        posR = np.linalg.solve(((vectorA[0],vectorC[0]),(vectorA[1],vectorC[1])),(trueY,trueX))
        posT = np.linalg.solve(((vectorC[0],vectorB[0]),(vectorC[1],vectorB[1])),(trueY,trueX))


        if np.max(posL) <1 and np.min(posL) >= 0 :
            return 0
        elif np.max(posR) <1 and np.min(posR) >= 0 :
            return 1
        elif np.max(posT) <1 and np.min(posT) >= 0 :
            return 2
    
    return -1


# Create the array that determines where cubes are
box_list = [[0]*5 for i in range(5)]
box_count = 0
for x in range(5):
    for y in range(5):
        if random.randint(0,1) == 1:
            box_list[x][y] = 1
            box_count += 1;


##box_list = [[1,1,1,1,1],
##            [1,1,0,0,1],
##            [1,0,0,0,1],
##            [1,1,0,0,1],
##            [1,1,1,1,1]]
box_count = 18
cube_list = [[0]*2 for i in range(box_count)]
box_index = 0
for x in range(5):
    for y in range(5):
        if box_list[x][y] == 1:
            cube_list[box_count - box_index - 1][0] = x
            cube_list[box_count - box_index - 1][1]= y
            box_index +=1

##cube_list = [[0] *2 for i in range(15)]
##cube_list[1] = [0,4]
##cube_list[2] = [0,3]
##cube_list[3] = [0,2]
##cube_list[4] = [0,1]
##cube_list[5] = [0,0]




image_width = 100;
image_height = 100;

my_array = np.full((image_width,image_height,3),(0,0,0), dtype=np.ubyte)


vc1 = (0,-1)
vc2 = (-1,0.5)
vc3 = (1,0.5)

image_magnitude = 3/(image_height+image_width/2)

offset = (-image_width *3/5 , -image_height/5)



print("beginning cubes")

for xind in range(image_width):
    for yind in range(image_height):
        xcoord = (-xind - offset[0]) * image_magnitude * 3.5
        ycoord = (yind + offset[1]) * image_magnitude  * 3.5


        side = on_tile(xcoord, ycoord, vc1 , vc2, vc3,cube_list)

        if side == 0:
            my_array[xind][yind] = (255,255,255)
        elif side == 1 :
            my_array[xind][yind] = (0,0,255)
        elif side == 2 :
            my_array[xind][yind] = (0,255,255)
        



im = Image.fromarray(my_array)

im.show()
