import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt

class Vertex:
  def __init__(self, x, y, nodeType, numLocations):
    self.x = x
    self.y = y
    self.nodeType = nodeType
    self.adjList = ['x' for i in range(numLocations)]
    self.degree = 0

  def __str__(self):
    return str(self.x) + " " + str(self.y) + " " + str(self.nodeType) + " " + str(self.adjList)


class GraphGenerator:
  def __init__(self, numLocations, numHomes):
    self.vertices = []
    self.numLocations = numLocations
    self.numHomes = numHomes
    self.startVertex = 0
    self.homeList = set()

  def __str__(self):
    return str(self.vertices)

  def genGraph(self):

    for i in range(self.numLocations):
      x, y = np.random.uniform(0, self.numLocations), np.random.uniform(0, self.numLocations)
      self.vertices.append(Vertex(x, y, 0, self.numLocations))
    
    self.startVertex = np.random.randint(0, self.numLocations - 1)

    currHomes = 0
    while (currHomes < self.numHomes):
      v = np.random.randint(0, self.numLocations - 1)
      if (v not in self.homeList):
        self.homeList.add(v)
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

    print("Average Degree:", gen.avgDegree())

  def dist(self, v, i):
    x_1, x_2 = self.vertices[v].x, self.vertices[i].x
    y_1, y_2 = self.vertices[v].y, self.vertices[i].y
    return round(math.sqrt((y_2 - y_1)**2 + (x_2 - x_1)**2), 5)

  def avgDegree(self):
    totalDegree = 0
    for i in range(self.numLocations):
      totalDegree += self.vertices[i].degree
    return totalDegree / self.numLocations


  def writeInput(self, inputNum=-1):
    if (inputNum == -1):
      return 
    
    f = open("input" + str(inputNum) + ".txt", "w")
    f.write(str(self.numLocations) + "\n" + str(self.numHomes) + "\n")

    for i in range(self.numLocations):
      f.write(str(i) + " ")
    f.write("\n")

    for home in self.homeList:
      f.write(str(home) + " ")
    f.write("\n" + str(self.startVertex) + "\n")

    for i in range(self.numLocations):
      for j in range(self.numLocations):
        f.write(str(self.vertices[i].adjList[j]) + " ")
      f.write("\n")

    f.close()

class VisualGrapher:
  def __init__(self, gen):
    self.gen = gen

  def connectPoints(self, x, y, p1, p2):
    x1, x2 = x[p1], x[p2]
    y1, y2 = y[p1], y[p2]
    plt.plot([x1,x2],[y1,y2],'k-')

  def visualizer(self):
    X, Y = [], []
    color_map = {1:'red',2:'green',3:'blue'}

    for i in range(self.gen.numLocations):
      X.append(self.gen.vertices[i].x)
      Y.append(self.gen.vertices[i].y)

      color = 0
      if (i == self.gen.startVertex):
        color = 1
      elif (i in self.gen.homeList):
        color = 2
      else:
        color = 3

      plt.scatter(X[i] , Y[i], color = color_map.get(color, 'black'))

    connected = set()
    for i in range(self.gen.numLocations):
      for j in range(self.gen.numLocations):
        if (self.gen.vertices[i].adjList[j] != 'x'):
          if tuple([i, j]) not in connected and tuple([j, i]) not in connected:
              self.connectPoints(X, Y, i, j)
              connected.add(tuple([i, j]))

    plt.show()

gen = GraphGenerator(10, 5) # PARAMS: NUM_LOCATIONS, NUM_HOMES
vis = VisualGrapher(gen) # PARAMS: GENERATOR INSTANCE

gen.genGraph()
gen.writeInput() # PARAMS: INPUT_NUM (e.g. INPUT_NUM = 1 writes to input1.txt | INPUT_NUM = -1 does not write to file)
vis.visualizer()
