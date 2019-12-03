from student_utils import *
import random
import generator
import utils
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def generate(G, start):
	"""
	Generate a random cycle starting at start
	Inputs:
		G: networkx graph
		start: starting vertex
	Outputs:
		list of vertices representing the car path
	"""
	path = []
	seen = set([])
	curr = start
	while curr not in seen:
		# print(curr)
		seen.add(curr)
		path.append(curr)
		edges = [e for e in G.edges([curr])]
		# print(edges)
		curr = random.choice(edges)[1]
	if curr == start:
		return path + [start]
	return path + nx.shortest_path(G, source = curr, target = start)

# Test code
# input_data = utils.read_file('batches/inputs/275_50.in')
# num_of_locations, num_houses, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix = data_parser(input_data)
# home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
# location_indices = convert_locations_to_indices(list_of_locations, list_of_locations)
# for i in range(len(adjacency_matrix)):
#     for j in range(len(adjacency_matrix)):
#             if (adjacency_matrix[i][j] == 'x'):
#                     adjacency_matrix[i][j] = 0

# G = nx.from_numpy_matrix(np.matrix(adjacency_matrix), create_using=nx.DiGraph)
# print(generate(G, int(0)))


# labels = { i : i for i in location_indices }
# pos = nx.spring_layout(G)
# nx.draw_networkx_nodes(G, pos,
#          nodelist=location_indices,
#          node_color='b',
#          node_size=100)
# nx.draw_networkx_nodes(G, pos,
#          nodelist=home_indices,
#          node_color='g',
#          node_size=100)
# nx.draw_networkx_nodes(G, pos,
#          nodelist=[list_of_locations.index(starting_car_location)],
#          node_color='r',
#          node_size=100)
# nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
# nx.draw_networkx_labels(G, pos, labels, font_size=8)
# plt.show()