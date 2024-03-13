from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt


class PathSizeLogitCalculator:

    def __init__(self, pathHandler, theta = 1, beta = 1):
        self.pathHandler = pathHandler
        self.theta = theta
        self.beta = beta

    def getPathGamma(self, path):
        connections = path.connections
        cost = path.getPathCost()
        gamma = 0
        for i in range(0,len(connections)):
            connection = connections[i]
            counts = self.pathHandler.getConnectionCounts(connection)
            connectionCost = connection.weight
            gamma = gamma + (connectionCost/cost)*(1/counts)

        return gamma

    def getProbabilities(self):
        paths = self.pathHandler.paths
        nPaths = len(paths)
        probs = []
        sumExponentials = 0
        gammas = []
        for i in range(0,nPaths):
            cost = paths[i].getPathCost()
            pathGamma = self.getPathGamma(paths[i])
            gammas.append(pathGamma)
            sumExponentials = sumExponentials + ((pathGamma)**(self.beta))*np.exp(-self.theta*cost)

        for i in range(0,nPaths):
            cost = paths[i].getPathCost()
            prob = (((gammas[i])**(self.beta))*np.exp(-self.theta*cost))/sumExponentials
            probs.append(prob)

        return np.array(probs)

    def showProbabilityDistribution(self):
        probs = self.getProbabilities()
        xArray = list(range(1,len(self.pathHandler.paths)+1))
        width = xArray[1] - xArray[0]
        plt.bar(xArray, probs, width =width, align = 'center', edgecolor = 'none', facecolor = '#ffbb00')
        plt.xlabel("Path")
        plt.ylabel("Probability")
        plt.title("PSL")

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