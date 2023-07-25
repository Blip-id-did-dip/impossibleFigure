from PIL import Image
import numpy as np

image_width = 500;
image_height = 500;

my_array = np.full((image_width,image_height,3),(0,0,0), dtype=np.ubyte)


vc1 = (0,-1)
vc2 = (-1,0.5)
vc3 = (1,0.8)

image_magnitude = 3/500

offset = (-image_height/2 , -image_width/2)


#A = np.zeros((2,2))
#b = np. zeros((2,1))
#b = [ycoord , xcoord]
            
#cola = vc1
#colb = vc2
#A[0] = [cola[0] , colb[0]]
#A[1] = [cola[1] , colb[1]]

for xind in range(image_width):
    for yind in range(image_height):
        xcoord = (-xind - offset[0]) * image_magnitude
        ycoord = (yind + offset[1])*image_magnitude

        posL = np.linalg.solve(((vc1[0],vc2[0]),(vc1[1],vc2[1])),(ycoord,xcoord))
        posR = np.linalg.solve(((vc1[0],vc3[0]),(vc1[1],vc3[1])),(ycoord,xcoord))
        posT = np.linalg.solve(((vc3[0],vc2[0]),(vc3[1],vc2[1])),(ycoord,xcoord))


        if np.max(posL) <1 and np.min(posL) >= 0 :
            my_array[xind][yind] = (255,255,255)
        elif np.max(posR) <1 and np.min(posR) >= 0 :
            my_array[xind][yind] = (0,0,255)
        elif np.max(posT) <1 and np.min(posT) >= 0 :
            my_array[xind][yind] = (0,255,255)
        



im = Image.fromarray(my_array)

im.show()
