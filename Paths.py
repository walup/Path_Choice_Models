from Utilities import DistanceCalculator
import numpy as np
import matplotlib.pyplot as plt
from Utilities import RandomColorGenerator


class Point:

    def __init__(self, coord1, coord2):
        self.coord1 = coord1
        self.coord2 = coord2
        self.id = "(" + str(coord1) + ","+str(coord2) + ")"

    def __eq__(self, other):
        return self.id == other.id

    def getId(self):
        return self.id

class Connection:

    def __init__(self, point1, point2, weight):
        self.fromNode = point1
        self.toNode = point2
        self.weight = weight

    def __eq__(self, other):
        return self.fromNode == other.fromNode and self.toNode == other.toNode

class PathUtilities:

    def getPathFromPointsAndDistance(self, points, distanceType):
        nPoints = len(points)
        distanceCalculator = DistanceCalculator()
        connections = []

        for i in range(0,nPoints-1):
            point1 = points[i]
            point2 = points[i+1]
            weight = distanceCalculator.obtainDistance(distanceType, point1, point2)

            connection = Connection(point1, point2, weight)
            connections.append(connection)

        return Path(connections)

class MultiPathHandler:

    def __init__(self, paths):
        self.paths = paths
        self.computeSharedConnections()

    def computeSharedConnections(self):
        self.allConnections = []
        for i in range(0,len(self.paths)):
            connections = self.paths[i].connections
            for j in range(0,len(connections)):
                connection = connections[j]
                if(not connection in self.allConnections):
                    self.allConnections.append(connection)

        self.sharedConnectionCounts = {}
        for i in range(0,len(self.allConnections)):
            connection = self.allConnections[i]
            counts = 0
            for j in range(0,len(self.paths)):
                if(connection in self.paths[j].connections):
                    counts = counts + 1
            self.sharedConnectionCounts[self.getConnectionId(connection)] = counts

    def getConnectionId(self, connection):
        id = connection.fromNode.id + "->"+connection.toNode.id
        return id

    def getConnectionCounts(self, connection):
        id = self.getConnectionId(connection)
        return self.sharedConnectionCounts[id]
    

    def drawPaths(self):
        nPaths = len(self.paths)
        colorGenerator = RandomColorGenerator()
        randomColors = colorGenerator.getRandomColors(nPaths)
        plt.figure(figsize = (7,7))
        
        for i in range(0,nPaths):
            self.paths[i].connectionColor = randomColors[i]
            self.paths[i].drawPath(i+1)

        plt.legend(loc = 'center right', bbox_to_anchor=(1.3, 0.5))

class Path:
    def __init__(self, connections):
        '''
        It is assumed that the connections are given in ordered fashion
        '''
        self.connections = connections
        self.nodeColor = "#c44352"
        self.connectionColor = "#2fa7d6"
        self.initialPointColor = "#e410e8"
        self.finalPointColor = "#e410e8"
        

    def drawPath(self, id):
        nConnections = len(self.connections)

        for i in range(0,nConnections):
            connection = self.connections[i]
            initialPoint = connection.fromNode
            finalPoint = connection.toNode
            #Draw the connection
            if(i == 0):
                plt.plot([initialPoint.coord1, finalPoint.coord1], [initialPoint.coord2, finalPoint.coord2], color = self.connectionColor, linewidth = 2, label = "Path "+str(id))
            else:
                plt.plot([initialPoint.coord1, finalPoint.coord1], [initialPoint.coord2, finalPoint.coord2], color = self.connectionColor, linewidth = 2)
                
            #Draw the initial point
            plt.plot(initialPoint.coord1, initialPoint.coord2, marker = "o", markersize = 5, color = self.nodeColor)
            #Draw the final point
            plt.plot(finalPoint.coord1, finalPoint.coord2, marker = "o", markersize = 5, color = self.nodeColor)

        initialPoint = self.connections[0].fromNode
        finalPoint = self.connections[-1].toNode
        
        plt.plot(initialPoint.coord1, initialPoint.coord2, marker = "o", markersize = 5, color = self.initialPointColor)
        plt.text(initialPoint.coord1, initialPoint.coord2 + 0.15, "Initial",horizontalalignment = 'center')
        plt.plot(finalPoint.coord1, finalPoint.coord2, marker = "o", markersize = 5, color = self.finalPointColor)
        plt.text(finalPoint.coord1, finalPoint.coord2 + 0.15, "Final",horizontalalignment = 'center')

    def getPathCost(self):
        cost = 0
        nConnections = len(self.connections)
        for i in range(0,nConnections):
            cost = cost + self.connections[i].weight

        return cost



        