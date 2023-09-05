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
        
        
        self.image_height = 400
        self.image_width = 600
        
        self.Avc1 = (0,1) # vertical vector component
        #self.Avc2 = (0.87,-0.5) # horizontal vector component
        self.Avc2 = (1,0)

        self.Bvc1 = self.Avc1
        self.Bvc2 = (self.Avc1[0] + self.Avc2[0], self.Avc1[1] + self.Avc2[1])

        self.Cvc1 = self.Bvc2
        self.Cvc2 = self.Avc2

        self.preview = np.full((self.image_height,self.image_width,3),(0,0,0), dtype=np.ubyte)

        self.boxHeight = 30
        self.boxLength = 45

        self.Lbox_list =[self.boxLength*[0] for j in range(self.boxHeight)]

        self.Rbox_list =[self.boxLength*[0] for j in range(self.boxHeight)]

        self.Tbox_list =[self.boxLength*[0] for j in range(self.boxHeight)]



    def __findImageBounds(self, givenHeight, givenLength):

        usedRight = max(self.Avc2[0] * givenLength , self.Avc2[0] * givenLength + self.Avc1[0]* givenHeight)
        usedLeft = min(0,self.Avc1[0]* givenHeight)
        usedTop = max(self.Avc1[1] * givenHeight, self.Avc1[1] *givenHeight + self.Avc2[1]*givenLength)
        usedBottom = min(0,self.Avc2[1]*givenLength)

        givenHeight = givenHeight + 1
        givenLength = givenLength + 1
        paddedRight = max(self.Avc2[0] * givenLength , self.Avc2[0] * givenLength + self.Avc1[0]* givenHeight)
        paddedLeft =  min(0,self.Avc1[0]* givenHeight)
        paddedTop = max(self.Avc1[1] * givenHeight, self.Avc1[1] *givenHeight + self.Avc2[1]*givenLength)
        paddedBottom = min(0,self.Avc2[1]*givenLength)


        deltaVert = paddedTop - paddedBottom
        deltaHorz = paddedLeft - paddedTop

        usedVert = usedTop - usedBottom
        usedHorz = usedRight - usedLeft

        multiplier = max(deltaVert / self.image_height, deltaHorz / self.image_width)

        return multiplier, usedBottom - 0.5 * (self.image_height* multiplier - usedVert), usedLeft - 0.5*(self.image_width * multiplier - usedHorz)
    
    
    def __on_tile(self, xcoord , ycoord, vectorA, vectorB, box_list, multiplier):
        xBox, yBox, posL = self.__getBoxCoordinates(xcoord, ycoord, vectorA, vectorB, box_list, multiplier)
        
        if yBox >= 0 and yBox < len(box_list[0]) and xBox >=0 and xBox <len(box_list) :
            return box_list[xBox][yBox], posL[0]%1 , posL[1]%1
        
        return -1 , posL[0]%1 , posL[1]%1

    def __getBoxCoordinates(self, xcoord , ycoord, vectorA, vectorB, box_list, multiplier):
        posL = np.linalg.solve(((vectorA[0],vectorB[0]),(vectorA[1],vectorB[1])),(ycoord,xcoord))
        
        yBox = math.floor(posL[1]) - multiplier[0] * math.floor(posL[0])
        xBox = len(box_list) - 1 -math.floor(posL[0]) - multiplier[1] * math.floor(posL[1])

        return xBox, yBox, posL

    def updateBoxlist(self, verticalPos, horizontalPos, leftValue, topValue, rightValue):

        xind , yind = self.__getScaledPos(verticalPos, horizontalPos)
        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1)
        xcoord = (self.image_height - xind )* sizeMultiplier + xoffset 
        ycoord = (yind )  * sizeMultiplier  + yoffset 
        xBox, yBox, posL = self.__getBoxCoordinates(xcoord, ycoord, self.Avc1, self.Avc2, self.Lbox_list, (0,0))
        if yBox >= 0 and yBox < len(self.Lbox_list[0]) and xBox >=0 and xBox <len(self.Lbox_list) :
            self.Lbox_list[xBox][yBox] = leftValue
            self.Rbox_list[xBox][yBox] = rightValue
            self.Tbox_list[xBox][yBox] = topValue

    def __getScaledPos(self, verticalPos, horizontalPos):
        scaledVertical = round(verticalPos * self.image_height)
        scaledHorizontal = round(horizontalPos * self.image_width)
        print("internal")
        print(scaledVertical)
        print(scaledHorizontal)

        return scaledVertical, scaledHorizontal

    def __cullBoxList(self):
        lowX = -1
        highX = self.boxHeight - 1
        lowY = -1
        highY = self.boxLength - 1

        for xind in range(self.boxHeight):
            for yind in range(self.boxLength):
                if (self.Lbox_list[xind][yind] > 0 or self.Rbox_list[xind][yind] >0 or self.Tbox_list[xind][yind]>0):
                    highX = xind
                    if (lowX == -1):
                        lowX = xind

        for yind in range(self.boxLength):
            for xind in range(self.boxHeight):
                if (self.Lbox_list[xind][yind] > 0 or self.Rbox_list[xind][yind] >0 or self.Tbox_list[xind][yind]>0):
                    highY = yind
                    if (lowY == -1):
                        lowY = yind


        LculledList = [(highY - lowY + 1) * [0] for i in range(highX - lowX + 1)]
        RculledList = [(highY - lowY + 1) * [0] for i in range(highX - lowX + 1)]
        TculledList = [(highY - lowY + 1) * [0] for i in range(highX - lowX + 1)]

        XculledInd = 0
        YculledInd = 0

        for xind in range(lowX, highX + 1):
            YculledInd = 0
            for yind in range(lowY, highY + 1):
                LculledList[XculledInd][YculledInd] = self.Lbox_list[xind][yind]
                RculledList[XculledInd][YculledInd] = self.Rbox_list[xind][yind]
                TculledList[XculledInd][YculledInd] = self.Tbox_list[xind][yind]

                YculledInd = YculledInd + 1

            XculledInd = XculledInd + 1       

         
        return LculledList, RculledList, TculledList
    
    def loadPreview(self):
        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1)
    

        for xind in range(self.image_height):
            for yind in range(self.image_width):
                xcoord = (self.image_height - xind ) * sizeMultiplier + xoffset 
                ycoord = (yind )* sizeMultiplier  + yoffset 

                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, self.Avc1 , self.Avc2, self.Lbox_list, (0,0))

                #this needs to be replaced with the background function
                self.preview[xind][yind] = (100,100,100) 

                if (xTilePos > 0.9 or yTilePos > 0.9):
                    self.preview[xind][yind] = (75,75,75)
                    continue

        return self.preview
    
    def getFigure(self):
        self.Avc1 = (0,1)
        self.Avc2 = (0.87, -0.5)

        self.Bvc1 = self.Avc1
        self.Bvc2 = (self.Avc1[0] + self.Avc2[0], self.Avc1[1] + self.Avc2[1])

        self.Cvc1 = self.Bvc2
        self.Cvc2 = self.Avc2
        
        self.image_height = 1000
        self.image_width = 1000
        renderImage = np.full((self.image_height,self.image_width,3),(0,0,0), dtype=np.ubyte)


        LculledList , RculledList, TculledList = self.__cullBoxList()
        #LculledList , RculledList, TculledList = self.Lbox_list, self.Rbox_list, self.Tbox_list

        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(len(LculledList),len(LculledList[0]))

        #sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1)
        


        for xind in range(self.image_height):
            for yind in range(self.image_width):
                xcoord = (self.image_height - xind ) * sizeMultiplier + xoffset 
                ycoord = (yind )* sizeMultiplier  + yoffset 


                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, self.Avc1 , self.Avc2, LculledList, (0,0))

                #this needs to be replaced with the background function
                renderImage[xind][yind] = (100,100,100) 


                if check >0 :
                    renderImage[xind][yind] = self.left_texture.getColour(xTilePos,yTilePos)
                if check !=2:
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc1[1], ycoord - self.Avc1[0] , self.Cvc1 , self.Cvc2,TculledList, (-1,0))
                    if check >0 :
                        renderImage[xind][yind] = self.top_texture.getColour(xTilePos,yTilePos)
                
                if check !=2 :
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc2[1], ycoord - self.Avc2[0], self.Bvc1 , self.Bvc2, RculledList, (0,1))
                    if check >0 :
                        renderImage[xind][yind] = self.right_texture.getColour(xTilePos,yTilePos)
        return renderImage
    
    def updatePreview(self, verticalPos, horizontalPos):
        scaledVertical , scaledHorizontal = self.__getScaledPos(verticalPos, horizontalPos)
        
        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1)
        previewAmount = round(4/sizeMultiplier)
        xmin = max(0,scaledVertical - previewAmount)
        xmax = min(self.image_height , scaledVertical + previewAmount)
        ymin = max(0,scaledHorizontal - previewAmount)
        ymax = min(self.image_width, scaledHorizontal + previewAmount)

        for xind in range(xmin, xmax):
            for yind in range(ymin, ymax):
                xcoord = (self.image_height - xind )  * sizeMultiplier + xoffset 
                ycoord = (yind )  * sizeMultiplier  + yoffset 


                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, self.Avc1 , self.Avc2, self.Lbox_list, (0,0))

                #this needs to be replaced with the background function
                self.preview[xind][yind] = (100,100,100) 

                if (xTilePos > 0.9 or yTilePos > 0.9):
                    self.preview[xind][yind] = (75,75,75)
                    continue

                if check >0 :
                    self.preview[xind][yind] = self.left_texture.getColour(xTilePos,yTilePos)
                if check !=2:
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc1[1], ycoord - self.Avc1[0] , self.Cvc1 , self.Cvc2, self.Tbox_list, (-1,0))
                    if check >0 :
                        self.preview[xind][yind] = self.top_texture.getColour(xTilePos,yTilePos)
                
                if check !=2 :
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - self.Avc2[1], ycoord - self.Avc2[0], self.Bvc1 , self.Bvc2, self.Rbox_list, (0,1))
                    if check >0 :
                        self.preview[xind][yind] = self.right_texture.getColour(xTilePos,yTilePos)
        return self.preview
