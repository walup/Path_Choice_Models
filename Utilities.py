from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
import random

class DistanceType(Enum):
    EUCLIDEAN = 0
    MANHATTAN = 1

class RandomColorGenerator:

    def getRandomColor(self):
        redValue = random.random()
        greenValue = random.random()
        blueValue = random.random()

        return np.array([redValue, greenValue, blueValue])

    def rgb2Hex(self, color):
        red = int(color[0]*255)
        blue = int(color[1]*255)
        green = int(color[2]*255)
        
        redString = "0x{:02x}".format(red)[2:]
        blueString = "0x{:02x}".format(blue)[2:]
        greenString = "0x{:02x}".format(green)[2:]

        hexString = "#"+redString+blueString+greenString

        return hexString

    def getRandomColors(self, nColors, separation = 0.1):

        colors = []
        maxIter = 10*nColors
        iters = 0
        while(len(colors) < nColors and iters < maxIter):
            newColor = self.getRandomColor()
            addColor = True
            for i in range(0,len(colors)):
                color = colors[i]
                dst = np.sqrt((newColor[0] - color[0])**2 + (newColor[1] - color[1])**2 + (newColor[2] - color[2])**2)
                if(dst < separation):
                    addColor = False

            if(addColor):
                colors.append(newColor)

            iters = iters + 1

        if(iters >= maxIter):
            print("Iterations exceeded error")
            return -1
        else:

            hexColors = []
            for i in range(0,len(colors)):
                hexValue = self.rgb2Hex(colors[i])
                hexColors.append(hexValue)
            return hexColors

class DistanceCalculator:

    def euclideanDistance(self, point1, point2):
        return np.sqrt((point1.coord1 - point2.coord1)**2 + (point1.coord2 - point2.coord2)**2)

    def manhattanDistance(self, point1, point2):
        return np.abs(point1.coord1 - point2.coord1) + np.abs(point1.coord2 - point2.coord2)

    def obtainDistance(self, distanceType, point1, point2):
        if(distanceType == DistanceType.EUCLIDEAN):
            return self.euclideanDistance(point1, point2)
        elif(distanceType == DistanceType.MANHATTAN):
            return self.manhattanDistance(point1, point2)