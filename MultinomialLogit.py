from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt

class MultinomialLogitCalculator:

    def __init__(self, multiPathHandler, theta = 1):
        self.pathHandler = multiPathHandler
        self.theta = theta

    def getProbabilities(self):
        paths = self.pathHandler.paths
        nPaths = len(paths)
        probs = []
        sumExponentials = 0
        for i in range(0,nPaths):
            cost = paths[i].getPathCost()
            sumExponentials = sumExponentials + np.exp(-self.theta*cost)

        for i in range(0,nPaths):
            cost = paths[i].getPathCost()
            prob = np.exp(-self.theta*cost)/sumExponentials
            probs.append(prob)

        return np.array(probs)

    def showProbabilityDistribution(self):
        probs = self.getProbabilities()
        xArray = list(range(1,len(self.pathHandler.paths)+1))
        width = xArray[1] - xArray[0]
        plt.bar(xArray, probs, width =width, align = 'center', edgecolor = 'none', facecolor = '#ffbb00')
        plt.xlabel("Path")
        plt.ylabel("Probability")
        plt.title("Multinomial logit")

    def choosePath(self):
        cumulative = 0
        probs = self.getProbabilities()
        randomNumber = random.random()
        paths = self.pathHandler.paths
        for i in range(0,len(probs)):
            if(randomNumber >= cumulative and randomNumber <= cumulative + probs[i]):
                return paths[i]
            else:
                cumulative = cumulative + probs[i]

        return -1