from PIL import Image
import random
import numpy as np
import math
from texture import texture


class impossibleFigure:
    def __init__(self):
        self.top_texture = texture((0,128,255))
        self.left_texture = texture((255,255,255))
        self.right_texture = texture((128,255,128))
        
        
        self.image_height = 300
        self.image_width = 450
        
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



    def __findImageBounds(self, givenHeight, givenLength,imageHeight,imageLength,vectorA1,vectorA2):

        vectorB1 = vectorA1
        vectorB2 = (vectorA1[0] + vectorA2[0], vectorA1[1] + vectorA2[1])

        vectorC1 = vectorB2
        vectorC2 = vectorA2

        usedRight = max(vectorA2[0] * givenLength , vectorA2[0] * givenLength + vectorA1[0]* givenHeight)
        usedLeft = min(0,vectorA1[0]* givenHeight)
        usedTop = max(vectorA1[1] * givenHeight, vectorA1[1] *givenHeight + vectorA2[1]*givenLength)
        usedBottom = min(0,vectorA2[1]*givenLength)

        givenHeight = givenHeight + 1
        givenLength = givenLength + 1
        paddedRight = max(vectorA2[0] * givenLength , vectorA2[0] * givenLength + vectorA1[0]* givenHeight)
        paddedLeft =  min(0,vectorA1[0]* givenHeight)
        paddedTop = max(vectorA1[1] * givenHeight, vectorA1[1] *givenHeight + vectorA2[1]*givenLength)
        paddedBottom = min(0,vectorA2[1]*givenLength)


        deltaVert = paddedTop - paddedBottom
        deltaHorz = paddedLeft - paddedTop

        usedVert = usedTop - usedBottom
        usedHorz = usedRight - usedLeft

        multiplier = max(deltaVert / imageHeight, deltaHorz / imageLength)

        return multiplier, usedBottom - 0.5 * (imageHeight* multiplier - usedVert), usedLeft - 0.5*(imageLength * multiplier - usedHorz)
    
    
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

    #def updateAutoMode(self,xBox,yBox):
        
    
    #def __inBox(self,xBox,yBox): 
    #    return (yBox >= 0 and yBox < len(self.Lbox_list[0]) and xBox >=0 and xBox <len(self.Lbox_list))

    def __getScaledPos(self, verticalPos, horizontalPos):
        scaledVertical = round(verticalPos * self.image_height)
        scaledHorizontal = round(horizontalPos * self.image_width)


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
        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1,self.image_height,self.image_width,self.Avc1,self.Avc2)
    

        for xind in range(self.image_height):
            for yind in range(self.image_width):
                xcoord = (self.image_height - xind ) * sizeMultiplier + xoffset 
                ycoord = (yind )* sizeMultiplier  + yoffset 

                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, self.Avc1 , self.Avc2, self.Lbox_list, (0,0))

                #this needs to be replaced with the background function
                self.preview[xind][yind] = (100,100,100) 

                if (xTilePos > 0.8 or yTilePos > 0.8):
                    self.preview[xind][yind] = (90,90,90)
                    continue

        return self.preview
    
    def getFigure(self):
        vectorA1 = (0,1)
        vectorA2 = (0.87, -0.5)

        vectorB1 = vectorA1
        vectorB2 = (vectorA1[0] + vectorA2[0], vectorA1[1] + vectorA2[1])

        vectorC1 = vectorB2
        vectorC2 = vectorA2
        
        renderHeight = 1000
        renderWidth = 1000
        renderImage = np.full((renderHeight,renderWidth,3),(0,0,0), dtype=np.ubyte)


        LculledList , RculledList, TculledList = self.__cullBoxList()
        #LculledList , RculledList, TculledList = self.Lbox_list, self.Rbox_list, self.Tbox_list

        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(len(LculledList),len(LculledList[0]),renderHeight,renderWidth,vectorA1,vectorA2)

        #sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1)
        
        renderImage = self.__assignColour(renderImage,renderHeight,renderWidth,0,renderHeight,0,renderWidth,sizeMultiplier,xoffset,yoffset,vectorA1,vectorA2,LculledList,TculledList,RculledList)

        return renderImage
    
    def updatePreview(self, verticalPos, horizontalPos, fullFlag = False):
        sizeMultiplier , xoffset, yoffset = self.__findImageBounds(self.boxHeight + 1, self.boxLength +1,self.image_height,self.image_width,self.Avc1,self.Avc2)
        if fullFlag :
            xmin = 0
            xmax = self.image_height
            ymin = 0
            ymax = self.image_width
        else:
            xind , yind = self.__getScaledPos(verticalPos, horizontalPos)
            xcoord = (self.image_height - xind )* sizeMultiplier + xoffset 
            ycoord = (yind )  * sizeMultiplier  + yoffset 
            xBox, yBox, posL = self.__getBoxCoordinates(xcoord, ycoord, self.Avc1, self.Avc2, self.Lbox_list, (0,0))
            #scaledVertical , scaledHorizontal = self.__getScaledPos((xBox)/(self.boxHeight),(yBox) / (self.boxLength) )
            
            scaledVertical = math.floor((xBox)*self.image_height/(self.boxHeight+2) )
            scaledHorizontal = math.floor((yBox)*self.image_width/(self.boxLength+3)+10)
            print("internal")
            print(scaledVertical)
            print(scaledHorizontal)

            
            xmin = max(0,scaledVertical)
            xmax = min(self.image_height , scaledVertical + 25)
            ymin = max(0,scaledHorizontal)
            ymax = min(self.image_width, scaledHorizontal +20)

        self.preview = self.__assignColour(self.preview,self.image_height,self.image_width,xmin,xmax,ymin,ymax,sizeMultiplier,xoffset,yoffset,self.Avc1,self.Avc2,self.Lbox_list,self.Tbox_list,self.Rbox_list,previewFlag=True)
        return self.preview

    def __assignColour(self,renderImage,imageHeight,imageWidth,xmin,xmax,ymin,ymax,sizeMultiplier,xoffset,yoffset,vectorA1,vectorA2,LboxList,TboxList,Rboxlist,previewFlag=False):
        vectorB1 = vectorA1
        vectorB2 = (vectorA1[0] + vectorA2[0], vectorA1[1] + vectorA2[1])

        vectorC1 = vectorB2
        vectorC2 = vectorA2

        for xind in range(xmin,xmax):
            for yind in range(ymin,ymax):
                xcoord = (imageHeight - xind ) * sizeMultiplier + xoffset 
                ycoord = (yind )* sizeMultiplier  + yoffset 


                check, xTilePos, yTilePos = self.__on_tile(xcoord, ycoord, vectorA1 , vectorA2, LboxList, (0,0))

                #this needs to be replaced with the background function
                if previewFlag:
                    self.preview[xind][yind] = (100,100,100) 

                    if (xTilePos > 0.8 or yTilePos > 0.8):
                        self.preview[xind][yind] = (90,90,90)
                        continue
                else:
                    renderImage[xind][yind] = (math.floor(100*xind*yind/imageHeight/imageWidth),math.floor(100*yind/imageWidth),math.floor(100*xind/imageWidth))


                if check >0 :
                    renderImage[xind][yind] = self.left_texture.getColour(xTilePos,yTilePos)
                if check !=2:
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - vectorA1[1], ycoord - vectorA1[0] , vectorC1 , vectorC2,TboxList, (-1,0))
                    if check >0 :
                        renderImage[xind][yind] = self.top_texture.getColour(xTilePos,yTilePos)
                
                if check !=2 :
                    check, xTilePos, yTilePos = self.__on_tile(xcoord - vectorA2[1], ycoord - vectorA2[0], vectorB1 , vectorB2, Rboxlist, (0,1))
                    if check >0 :
                        renderImage[xind][yind] = self.right_texture.getColour(xTilePos,yTilePos)
        return renderImage

    def saveFigure(self):
        with open("local/testfile.bin", "wb") as saveFile:
            #saveFile.write("hello file num 2")
            for xind in range(self.boxHeight):
                for yind in range(self.boxLength):
                    saveFile.write(self.Lbox_list[xind][yind].to_bytes(4))
                    saveFile.write(self.Tbox_list[xind][yind].to_bytes(4))
                    saveFile.write(self.Rbox_list[xind][yind].to_bytes(4))
        
        print("figure saved!")

    def loadFigure(self):
        with open("local/testfile.bin", "rb") as saveFile:
            #myvar = saveFile.readline()
            #print(myvar)
            for xind in range(self.boxHeight):
                for yind in range(self.boxLength):
                    self.Lbox_list[xind][yind]=int.from_bytes(saveFile.read(4))
                    self.Tbox_list[xind][yind]=int.from_bytes(saveFile.read(4))
                    self.Rbox_list[xind][yind]=int.from_bytes(saveFile.read(4))
                    
        
        print("figure loaded!")
