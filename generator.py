import math
import utils
import pickle
import argparse
import networkx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from student_utils import *
from scipy.sparse.csgraph import connected_components

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

	def genGraph(self, ddMean=0.2, ddDecay=0.1):

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
			self.vertices[i].degree = int((np.random.laplace(ddMean, ddDecay))*(self.numLocations - i))
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

		if (self.checkConnectivity() != 1):
			new_gen = GraphGenerator(self.numLocations, self.numHomes)
			self.vertices = new_gen.genGraph(ddMean, ddDecay)
		else:
			print("Average Degree:", self.avgDegree())

		return self.vertices

	def dist(self, v, i):
		x_1, x_2 = self.vertices[v].x, self.vertices[i].x
		y_1, y_2 = self.vertices[v].y, self.vertices[i].y
		return round(math.sqrt((y_2 - y_1)**2 + (x_2 - x_1)**2), 5)

	def avgDegree(self):
		totalDegree = 0
		for i in range(self.numLocations):
			for j in range(self.numLocations):
				if (self.vertices[i].adjList[j] != 'x'):
					totalDegree += 1
		return totalDegree / self.numLocations

	def checkConnectivity(self):
		adj_matrix = [self.vertices[i].adjList.copy() for i in range(self.numLocations)]

		for i in range(len(adj_matrix)):
			for j in range(len(adj_matrix)):
				if (adj_matrix[i][j] == 'x'):
					adj_matrix[i][j] = 0

		adj_matrix = np.array(adj_matrix, dtype=np.float32)

		return connected_components(csgraph=adj_matrix, return_labels=False)

	def cycleFinder(self, graph=None):
		if (not graph):
			graph = {}
			for i in range(self.numLocations):
				if (i not in graph):
					graph[i] = []
				for j in range(self.numLocations):
					if (self.vertices[i].adjList[j] != 'x'):
						graph[i].append(j)

		cycles = [[node]+path  for node in graph for path in self.dfs(graph, node, node)]
		cycles = [cy for cy in cycles if cy[0] != cy[2]]

		print("------------------------------\nCycles: ")
		
		for cy in cycles:
			path = [str(node) for node in cy]
			s = " -> ".join(path)
			print(s)

		if (len(cycles) == 0):
			print("None found!")

	def dfs(self, graph, start, end):
		fringe = [(start, [])]
		while fringe:
			state, path = fringe.pop()
			if path and state == end:
				yield path
				continue
			for next_state in graph[state]:
				if next_state in path:
					continue
				fringe.append((next_state, path+[next_state]))

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

	def serializer(self, output_file):
		with open(output_file, "wb") as fp:
			pickle.dump(self, fp)


class GraphVisualizer:
	def __init__(self, gen=None):
		self.gen = gen

	def connectPoints(self, x, y, p1, p2):
		x1, x2 = x[p1], x[p2]
		y1, y2 = y[p1], y[p2]
		plt.plot([x1, x2], [y1, y2], 'k-')

	def visGen(self):
		X, Y = [], []
		color_map = {1: 'red', 2: 'green', 3: 'blue'}

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

			plt.scatter(X[i], Y[i], color=color_map.get(color, 'black'))
			plt.annotate(i, (X[i], Y[i]))

		connected = set()
		for i in range(self.gen.numLocations):
			for j in range(self.gen.numLocations):
				if (self.gen.vertices[i].adjList[j] != 'x'):
					if tuple([i, j]) not in connected and tuple([j, i]) not in connected:
						self.connectPoints(X, Y, i, j)
						connected.add(tuple([i, j]))

		plt.show()

	def visSerial(self, output_file):
		with open(output_file, "rb") as fp:
			self.gen = pickle.load(fp)
		self.visGen()

	def visFromAdj(self, input_matrix, solution_file):
		input_data = utils.read_file(input_matrix)
		num_of_locations, num_houses, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix = data_parser(input_data)
		home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
		location_indices = convert_locations_to_indices(list_of_locations, list_of_locations)

		for i in range(len(adjacency_matrix)):
			for j in range(len(adjacency_matrix)):
				if (adjacency_matrix[i][j] == 'x'):
					adjacency_matrix[i][j] = 0

		G = nx.from_numpy_matrix(np.matrix(adjacency_matrix), create_using=nx.DiGraph)
		pos = nx.spring_layout(G)

		labels = { i : i for i in location_indices }
				
		nx.draw_networkx_nodes(G, pos,
					   nodelist=location_indices,
					   node_color='b',
					   node_size=100)
		nx.draw_networkx_nodes(G, pos,
					   nodelist=home_indices,
					   node_color='g',
					   node_size=100)
		nx.draw_networkx_nodes(G, pos,
					   nodelist=[list_of_locations.index(starting_car_location)],
					   node_color='r',
					   node_size=100)
		nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)

		if (type(solution_file) == str):
			with open(solution_file) as f:
				path = list(f.readline().split())

			path_edges = [[list_of_locations.index(path[i]), list_of_locations.index(path[i+1])] for i in range(len(path) - 1)]
			nx.draw_networkx_edges(G, pos,
						edgelist=path_edges,
						width=3, alpha=0.5, edge_color='r')
			nx.draw_networkx_labels(G, pos, labels, font_size=8)

		plt.show()


# -------------------------------------------------------------- COMMAND LINE INTERFACE -------------------------------------------------------------- #
if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Parsing arguments')
	parser.add_argument('action', type=str, help='The type of action to execute.')
	parser.add_argument('input1', type=str, help='The path to the input file or directory')
	parser.add_argument('input2', type=str, nargs=None, default=None, help='The path to the input file or directory')

	args = parser.parse_args()
	action = args.action
	input_1 = args.input1
	input_2 = args.input2

	if (action == "visualize" or action == "vis" or action == "visual"):
		vis = GraphVisualizer()
		vis.visFromAdj(input_1, input_2)

	if (action == "generate" or action == "gen"):
		gen = GraphGenerator(int(input_1), int(input_2))
		gen.genGraph()
		gen.cycleFinder()

		gen.writeInput(0)
		gen.serializer("serialized_graphs/test0.pickle")

		vis = GraphVisualizer(gen)
		vis.visGen()