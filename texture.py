from PIL import Image
import numpy as np
from math import floor

class texture:
    def __init__(self, colour):
        self.colour = colour
        self.solidBlock = 1

    def setTexture(self, texturePath):
        im = Image.open(texturePath)
        self.texture = np.asarray(im)
        self.textureSize = (self.texture.shape[0]-1 ,self.texture.shape[1]-1)
        self.solidBlock = 0

        
    def getColour(self, xPos, yPos):
        if self.solidBlock == 1:
            return (self.colour[0], self.colour[1]*xPos, self.colour[2]*yPos)

        
        xind = floor((1-xPos) * self.textureSize[0])
        yind = floor((yPos) * self.textureSize[1])

        return self.texture[xind][yind]
        #return (self.colour[0], self.colour[1]*xPos, self.colour[2]*yPos)
