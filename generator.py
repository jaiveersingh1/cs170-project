import numpy as np
import math

class Vertex:
  def __init__(self, x, y, nodeType, numLocations):
    self.x = x
    self.y = y
    self.nodeType = nodeType
    self.adjList = []
    self.degree = 0

    for i in range(numLocations):
      self.adjList.append('x')

  def __str__(self):
    return str(self.x) + " " + str(self.y) + " " + str(self.nodeType) + " " + str(self.adjList)

  def addAdjacent(self, adjVertex):
    self.adjList.append(adjVertex)


class GraphGenerator:
  def __init__(self, vertices, numLocations, numHomes):
    self.vertices = vertices
    self.numLocations = numLocations
    self.numHomes = numHomes
    self.startVertex = 0
    self.homeList = []

  def __str__(self):
    return str(self.vertices)

  # START = 1 | TA = 2
  def genGraph(self):

    for i in range(self.numLocations):
      x, y = np.random.uniform(0, self.numLocations), np.random.uniform(0, self.numLocations)
      self.vertices.append(Vertex(x, y, 0, self.numLocations))
    
    self.startVertex = np.random.randint(0, self.numLocations - 1)

    currHomes = 0
    while (currHomes < self.numHomes):
      v = self.vertices[np.random.randint(0, self.numLocations - 1)] 
      if (v.nodeType != 2):
        v.nodeType = 2
        self.homeList.append(np.random.randint(0, self.numLocations - 1))
        currHomes += 1

    for i in range(self.numLocations):
      self.vertices[i].degree = int((np.random.laplace(0.4, 0.1))*(self.numLocations - i))
      vs = {i}

      numNeighbors = 0
      while (numNeighbors < self.vertices[i].degree):
        v = np.random.randint(0, self.numLocations)
        while v in vs:
          v = np.random.randint(0, self.numLocations)
        if (self.vertices[i].adjList[v] == 'x'):
          vs.add(v)
          self.vertices[i].adjList[v] = self.dist(v, i)
          self.vertices[v].adjList[i] = self.dist(v, i)
          numNeighbors += 1

    for i in range(self.numLocations):
      print(self.vertices[i].adjList)

  def dist(self, v, i):
    x_1, x_2 = self.vertices[v].x, self.vertices[i].x
    y_1, y_2 = self.vertices[v].y, self.vertices[i].y
    return round(math.sqrt((y_2 - y_1)**2 + (x_2 - x_1)**2), 5)

  def avgDegree(self):
    totalDegree = 0
    for i in range(self.numLocations):
      totalDegree += self.vertices[i].degree
    return totalDegree / self.numLocations


  def writeInput(self, inputNum):
    f = open("input" + str(inputNum) + ".txt", "w")
    f.write(str(self.numLocations) + "\n" + str(self.numHomes) + "\n")

    for i in range(self.numLocations):
      f.write(str(i) + " ")
    f.write("\n")

    for i in range(self.numHomes):
      f.write(str(self.homeList[i]) + " ")
    f.write("\n" + str(self.startVertex) + "\n")

    for i in range(self.numLocations):
      for j in range(self.numLocations):
        f.write(str(self.vertices[i].adjList[j]) + " ")
      f.write("\n")

    f.close()

gen = GraphGenerator([], 200, 5)
gen.genGraph()
gen.writeInput(0)

print(gen.avgDegree())
