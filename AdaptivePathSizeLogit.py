from enum import Enum
import random
import numpy as np
import matplotlib.pyplot as plt

class AdaptivePathSizeLogitCalculator:

    def __init__(self, pathHandler, theta = 1, beta = 1):
        self.pathHandler = pathHandler
        self.theta = theta
        self.beta = beta
        #Tau value used for getting the solution iteratively 
        self.tau = 10**-16
        self.E = 3
        self.N = len(self.pathHandler.paths)
        self.maxIterations = 100

    #Initialize the probabilities as homogeneous
    def initializeProbabilities(self):
        self.probs = np.zeros(self.N)
        for i in range(0,self.N):
            self.probs[i] = 1/self.N
        self.errorArray = np.zeros(self.N)

    def getPathGamma(self, path, index):
        connections = path.connections
        nConnections = len(connections)
        pathCost = path.getPathCost()
        gamma = 0
        paths = self.pathHandler.paths
        for i in range(0,len(connections)):
            connection = connections[i]
            weightedSum = 0
            connectionCost = connection.weight
            for j in range(0,len(paths)):
                if(connection in paths[j].connections):
                    weightedSum = weightedSum + self.probs[j]/self.probs[index]
            gamma = gamma + (connectionCost/pathCost)*(1/weightedSum)

        return gamma

    def iterateProbabilities(self):
        paths = self.pathHandler.paths
        gammas = []
        for i in range(0,self.N):
            gamma = self.getPathGamma(paths[i], i)
            pathCost = paths[i].getPathCost()
            gammas.append((gamma**self.beta)*np.exp(-self.theta*pathCost))

        sumGammas = sum(gammas)
        for i in range(0,self.N):
            gamma = gammas[i]
            g = gamma/sumGammas
            prob = self.tau + (1 - self.N*self.tau)*g
            error = np.abs(prob - self.probs[i])
            self.probs[i] = prob
            self.errorArray[i] = error

    def getProbabilities(self):
        self.initializeProbabilities()
        error = float('inf')
        iters = 0
        while(error > np.log(10**-self.E) and iters < self.maxIterations):
            self.iterateProbabilities()
            error = np.sum(self.errorArray)
            iters = iters + 1

        return self.probs


    def showProbabilityDistribution(self):
        probs = self.getProbabilities()
        xArray = list(range(1,len(self.pathHandler.paths)+1))
        width = xArray[1] - xArray[0]
        plt.bar(xArray, probs, width =width, align = 'center', edgecolor = 'none', facecolor = '#ffbb00')
        plt.xlabel("Path")
        plt.ylabel("Probability")
        plt.title("APSL")

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