from PIL import Image
import random
import numpy as np
import math
from texture import texture

class impossibleFigure:
    def __init__(self):
        self.top_texture = texture((0,255,255))
        self.left_texture = texture((255,255,255))
        self.right_texture = texture((0,0,255))
        
        self.image_width = 200;
        self.image_height = 200;
        
        self.Avc1 = (0,1) # vertical vector component
        self.Avc2 = (0.87,-0.5) # horizontal vector component

        self.Bvc1 = self.Avc1
        self.Bvc2 = (self.Avc1[0] + self.Avc2[0], self.Avc1[1] + self.Avc2[1])

        self.Cvc1 = self.Bvc2
        self.Cvc2 = self.Avc2




    def __find_image_bounds(self, vector1, vector2, boxShape):
        right = max(0, vector1[0],vector2[0], vector1[0] + vector2[0]) * boxShape[0]
        left = min(0, vector1[0],vector2[0], vector1[0] + vector2[0]) * boxShape[0] 

        top = max(0, vector1[1],vector2[1], vector1[1] + vector2[1]) * boxShape[1]
        bottom = min(0, vector1[1],vector2[1], vector1[1] + vector2[1]) * boxShape[1]

        xmultiplier = top - bottom 
        ymultiplier = right - left 

        multiplier = max(xmultiplier, ymultiplier)+1
        return multiplier, bottom - 0.5*( multiplier - xmultiplier), left -0.5* (multiplier - ymultiplier)
    
    
    def __on_tile(self, xcoord , ycoord, vectorA, vectorB, box_list, multiplier):
        posL = np.linalg.solve(((vectorA[0],vectorB[0]),(vectorA[1],vectorB[1])),(ycoord,xcoord))
        
        xBox = math.floor(posL[1]) - multiplier[0] * math.floor(posL[0])
        yBox = math.floor(posL[0]) - multiplier[1] * math.floor(posL[1])
        
        if xBox >= 0 and xBox < len(box_list[0]) and yBox >=0 and yBox <len(box_list) :
            return box_list[len(box_list) - 1 - yBox][xBox], posL[0]%1 , posL[1]%1
        
        return 0 ,0 , 0


    def getFigure(self, Lbox_list, Rbox_list, Tbox_list):
        figureArray = np.full((self.image_height,self.image_width,3),(0,0,0), dtype=np.ubyte)
        xmultiplier , xoffset, yoffset = self.__find_image_bounds(self.Avc1,self.Avc2,(len(Lbox_list[0]),len(Lbox_list)))
        ymultiplier = xmultiplier

        for xind in range(self.image_height):
            for yind in range(self.image_width):
                xcoord = (self.image_height - xind ) / self.image_height * xmultiplier + xoffset 
                ycoord = (yind ) / self.image_width * ymultiplier  + yoffset 


                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, self.Avc1 , self.Avc2, Lbox_list, (0,0))


                if check >0 :
                    figureArray[xind][yind] = self.left_texture.getColour(xTilePos,yTilePos)
                if check !=2:
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc1[1], ycoord - self.Avc1[0] , self.Cvc1 , self.Cvc2,Tbox_list, (-1,0))
                    if check >0 :
                        figureArray[xind][yind] = self.top_texture.getColour(xTilePos,yTilePos)
                
                if check !=2 :
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc2[1], ycoord - self.Avc2[0], self.Bvc1 , self.Bvc2,Rbox_list, (0,-1))
                    if check >0 :
                        figureArray[xind][yind] = self.right_texture.getColour(xTilePos,yTilePos)
        return figureArray
