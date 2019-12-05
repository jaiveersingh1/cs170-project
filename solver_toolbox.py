from student_utils import *
import itertools
from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY, INTEGER, OptimizationStatus
import matplotlib.pyplot as plt
import utils
import time
from colorama import init, Fore, Style
import sqlite3
import os
import random

class BaseSolver:
	""" Base class for solvers """

	def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
		"""
		Solve the problem using a specific technique.
		Input:
			list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
			list_of_homes: A list of homes
			starting_car_location: The name of the starting location for the car
			adjacency_matrix: The adjacency matrix from the input file
		Output:
			A cost of how expensive the current solution is
			A list of locations representing the car path
			A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
			NOTE: all outputs should be in terms of indices not the names of the locations themselves
		"""
		return 0, [], dict()

	def construct_starter(self, x, t, G, home_indices, car_path_indices):
		"""
		Treating the car's cycle as constant, find a valid solution to the corresponding ILP problem.
		Input:
			G: A NetworkX graph
			home_indices: The list of home indices in the graph
			car_path_indices: The indices of the vertices in G that are in the car path
		Output:
			MIP Model Starter, to be set as model.start
		"""

		E = list(G.to_directed().edges())

		x_starter = []
		x_set = set()
		prev = car_path_indices[0]
		for curr in car_path_indices[1:]:
			edge_index = E.index((prev, curr))
			x_set.add(x[edge_index])
			prev = curr

		for x_i in x:
			if x_i in x_set:
				x_starter.append((x_i, 1.0))
			else:
				x_starter.append((x_i, 0.0))

		shortest_paths = dict(nx.all_pairs_shortest_path(G))
		shortest_distances = dict(nx.floyd_warshall(G))
		
		t_starter = []
		for i, home_index in enumerate(home_indices):
			best_distance = float('inf')
			best_path = []
			for dropoff_vertex in car_path_indices:
				distance = shortest_distances[dropoff_vertex][home_index]
				path = shortest_paths[dropoff_vertex][home_index]

				if distance < best_distance:
					best_distance = distance
					best_path = path
			
			prev = best_path[0]
			t_set = set()
			for curr in best_path[1:]:
				edge_index = E.index((prev, curr))
				t_set.add(t[i][edge_index])
				prev = curr
			
			for x_i in t[i]:
				if x_i in t_set:
					t_starter.append((x_i, 1.0))
				else:
					t_starter.append((x_i, 0.0))

		return x_starter + t_starter

	def generate_random(self, G, start_index):
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
		curr = start_index
		while curr not in seen:
			seen.add(curr)
			path.append(curr)
			edges = [e for e in G.edges([curr])]
			curr = random.choice(edges)[1]
		if curr == start_index:
			return path + [start_index]
		index = path.index(curr)
		shame = path[:index + 1]
		return path + shame[::-1]
	
	def find_best_dropoffs(self, G, home_indices, car_path_indices):
		"""
		Treating the car's cycle as constant, find the best dropoff locations for the TAs to minimize walking cost.
		Input:
			G: A NetworkX graph
			home_indices: The indices of the vertices in G that are TA homes
			car_path_indices: The indices of the vertices in G that are in the car path
		Output:
			Total walking cost (TA ONLY)
			A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
			NOTE: all outputs should be in terms of indices not the names of the locations themselves
		"""

		# Initialize shortest_distances matrix, where shortest_distances[r][c] is the shortest distance from r to c
		shortest_distances = dict(nx.floyd_warshall(G))

		# Determine TA dropoff
		dropoffs = {}
		total_cost = 0

		for home in home_indices:

			# Find preferred dropoff location for this TA
			best_dropoff = None
			for dropoff in car_path_indices:
				if best_dropoff == None or shortest_distances[dropoff][home] < shortest_distances[best_dropoff][home]:
					best_dropoff = dropoff

			dropoffs[best_dropoff] = dropoffs.get(best_dropoff, []) + [home]
			total_cost += shortest_distances[best_dropoff][home]
		
		return total_cost, dropoffs

	def construct_path(self, start, edges, input_file):
		"""
		Constructs a path from an unordered list of edges given some starting vertex
		Input:
			start: starting vertex
			edges: list of edges represented by integer pairs
		Output:
			List of edges in a path
		"""
		conn = sqlite3.connect('models.sqlite')
		c = conn.cursor()

		G = nx.DiGraph()
		G.add_weighted_edges_from(edges)
		path = [start]
		if not edges:
			self.log_update_entry(Fore.YELLOW + "No edges." + Style.RESET_ALL)
		elif nx.is_eulerian(G):
			path_edges = list(nx.eulerian_circuit(G, start))
			path += [edge[1] for edge in path_edges]
		else:
			self.log_update_entry(Fore.YELLOW + "Graph was not Eulerian." + Style.RESET_ALL)
			c.execute('UPDATE models SET optimal = 0 WHERE input_file = ?', (input_file,))
			conn.commit()
		conn.close()
		return path

	logfile = "logfile_default.txt"
	
	def log_new_entry(self, input_file):
		msg = "\n{}\t{}  \t".format(time.ctime(), input_file)
		self.log_update_entry(msg)

	def log_update_entry(self, msg):
		f = open(self.logfile, "a+")
		f.write(msg + " ")
		f.close()
		
def randomSolveJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
	
	return 0, [], dict()

class BruteForceJSSolver(BaseSolver):
	def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
		"""
		Solve the problem using brute force.
		Input:
			list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
			list_of_homes: A list of homes
			starting_car_location: The name of the starting location for the car
			adjacency_matrix: The adjacency matrix from the input file
		Output:
			A cost of how expensive the current solution is
			A list of locations representing the car path
			A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
			NOTE: all outputs should be in terms of indices not the names of the locations themselves
		"""
		home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)

		G, message = adjacency_matrix_to_graph(adjacency_matrix)
		E = G.to_directed().edges(data='weight')

		starting_car_index = list_of_locations.index(starting_car_location)
		best_solution = (float('inf'), [], {})

		def powerset(L):
			for n in range(len(L) + 1):
				yield from itertools.combinations(L, n)

		counter = 0
		for edge_set in powerset(E):
			counter += 1
			if (counter % 10000 == 0):
				print(counter, end=" ")

			# Check if edge set is valid
			entry_counts = [0 for _ in list_of_locations]
			exit_counts = [0 for _ in list_of_locations]
			visited = set()
			driving_cost = 0
			contains_start = False
			
			for edge in edge_set:
				visited.add(edge[1])
				driving_cost += 2/3 * edge[2]
				if (edge[0] == starting_car_index or edge[1] == starting_car_index):
					contains_start = True

			G_chosen = nx.DiGraph()
			G_chosen.add_weighted_edges_from(edge_set)

			if edge_set and nx.is_eulerian(G_chosen) and contains_start:
				walking_cost, dropoffs = self.find_best_dropoffs(G, home_indices, list(visited))
				total_cost = walking_cost + driving_cost

				if total_cost < best_solution[0]:
					best_solution = (total_cost, self.construct_path(starting_car_index, edge_set), dropoffs)
		
		print("\n\nBest cost was", best_solution[0])
		return best_solution

class ILPSolver(BaseSolver):
	def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
		"""
		Solve the problem using an MST/DFS approach.
		Input:
			list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
			list_of_homes: A list of homes
			starting_car_location: The name of the starting location for the car
			adjacency_matrix: The adjacency matrix from the input file
		Output:
			A cost of how expensive the current solution is
			A list of locations representing the car path
			A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
			NOTE: all outputs should be in terms of indices not the names of the locations themselves
		"""
		conn = sqlite3.connect('models.sqlite')
		c = conn.cursor()
		seen = c.execute('SELECT best_objective_bound FROM models WHERE input_file = (?)', (input_file,)).fetchone()
		
		self.log_new_entry(input_file)

		home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
		location_indices = convert_locations_to_indices(list_of_locations, list_of_locations)

		G, message = adjacency_matrix_to_graph(adjacency_matrix)
		E = list(G.to_directed().edges(data='weight'))

		starting_car_index = list_of_locations.index(starting_car_location)

		start_paths = []
		num_random_paths = 5
		if "-r" in params:
			num_random_paths = int(params[params.index("-r") + 1])

		for i in range(num_random_paths):
			start_paths.append(self.generate_random(G, starting_car_index))

		if seen:
			output_file = 'submissions/submission_final/{}.out'.format(input_file.split('.')[0])
			print(output_file)
			if not "--no-prev" in params and os.path.isfile(output_file):
				start_paths.append(convert_locations_to_indices(utils.read_file(output_file)[0], list_of_locations))
		
		best_start_path_cost = float('inf')
		best_start_path_index = -1
		for i, path in enumerate(start_paths):
			walk_cost, dropoffs = self.find_best_dropoffs(G, home_indices, path)
			cost, msg = cost_of_solution(G, path, dropoffs)

			if cost < best_start_path_cost:
				best_start_path_cost = cost
				best_start_path_index = i

		start_path = start_paths[best_start_path_index]
		print("Starting path:")
		if best_start_path_index == num_random_paths:
			print("SAVED PATH:", start_path)
		elif best_start_path_index >= 0:
			print("RANDOM PATH:", start_path)
		else:
			print("No start path found")
		print("Starting cost:", best_start_path_cost)

		# number of nodes and list of vertices, not including source or sink
		n, V, H = len(list_of_locations), location_indices, home_indices 
		bigNum = (2 * n) 

		model = Model()

		# does the car drive from i to j?
		x = [model.add_var(var_type=BINARY) for e in E]

		# does the kth TA walk from i to j? over all num_homes TAs
		t = [[model.add_var(var_type=BINARY) for e in E] for k in H]

		# car flow from vertex u to vertex v
		f = [model.add_var(var_type=INTEGER) for e in E] \
		+ [model.add_var(var_type=INTEGER) for v in V] \
		+ [model.add_var(var_type=INTEGER)]

		# kth TA flow from vertex u to vertex v
		f_t = [[model.add_var(var_type=BINARY) for e in E] + [model.add_var(var_type=BINARY) for v in V] for k in H]

		for i in range(len(f)):
			model += f[i] >= 0

		# For each vertex v where v != source and v != sink, Sum{x_(u, v)} = Sum{x_(v, w)}
		for v in V:
			model += xsum([x[i] for i in range(len(E)) if E[i][1] == v]) == xsum([x[i] for i in range(len(E)) if E[i][0] == v])

		# For each vertex v where v != sink, Sum{f_(u, v)} = Sum{f_(v, w)}
		for j in range(len(V)):
			model += xsum([f[i] for i in range(len(E)) if E[i][1] == V[j]]) + (f[-1] if V[j] == starting_car_index else 0) \
				 == xsum([f[i] for i in range(len(E)) if E[i][0] == V[j]]) + f[len(E) + j]

		# For each edge (u, v) where u != source and v != sink, f_(u, v) <= (big number) * x_(u, v)
		for i in range(len(E)):
			model += f[i] <= bigNum * x[i]

		# For edge (source, start vertex), f_(source, start vertex) <= (big number)
		model += f[-1] <= bigNum

		# For each edge (u, sink), f_(u, sink) <= Sum{x_(w, u)}
		for j in range(len(V)):
			model += f[j + len(E)] \
				 <= xsum([x[i] for i in range(len(E)) if E[i][1] == V[j]])

		# For just the source vertex, f_(source,start vertex)} = Sum{x_(a, b)}
		model += f[-1] == xsum(x)

		# For every TA for every edge, can't flow unless edge is walked along
		for i in range(len(t)):
			for j in range(len(E)):
				model += f_t[i][j] <= t[i][j]

		# For every TA for every non-home vertex, flow in equals flow out
		for i in range(len(H)):
			for j in range(len(V)):
				if V[j] != H[i]:
					model += xsum(f_t[i][k] for k in range(len(E)) if E[k][1] == V[j]) + f_t[i][len(E) + j] \
						== xsum(f_t[i][k] for k in range(len(E)) if E[k][0] == V[j])

		# For every TA, flow out of the source vertex is exactly 1
		for k in f_t:
			model += xsum(k[len(E) + i] for i in range(len(V))) == 1

		# For every TA for every edge out of source, can't flow unless car visits vertex
		for k in f_t:
			for i in range(len(V)):
				model += k[len(E) + i] <= xsum(x[j] for j in range(len(E)) if E[j][1] == V[i])

		# For every TA, flow into the home vertex is exactly 1
		for i in range(len(H)):
			model += xsum(f_t[i][j] for j in range(len(E)) if E[j][1] == H[i]) + f_t[i][len(E) + H[i]] == 1

		# objective function: minimize the distance
		model.objective = minimize(2.0/3.0 * xsum([x[i] * E[i][2] for i in range(len(E))]) \
			+ xsum([xsum([t[i][j] * E[j][2] for j in range(len(E))]) for i in range(len(t))]))

		# WINNING ONLINE
		model.max_gap = 0.00001
		model.emphasis = 2
		model.symmetry = 2

		if "--no-model-start" not in params:
			model.start = self.construct_starter(x, t, G, home_indices, start_path)

		timeout = 300
		if "-t" in params:
			timeout = int(params[params.index("-t") + 1])

		if timeout != -1:
			status = model.optimize(max_seconds=timeout)
		else:
			status = model.optimize()

		if status == OptimizationStatus.OPTIMAL:
			print('optimal solution cost {} found'.format(model.objective_value))
			self.log_update_entry(Fore.GREEN + "Optimal cost={}.".format(model.objective_value) + Style.RESET_ALL)
		else:
			print("!!!! TIMEOUT !!!!")
			self.log_update_entry(Fore.RED + "Timeout!" + Style.RESET_ALL)

			if status == OptimizationStatus.FEASIBLE:
				print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
				self.log_update_entry("Feasible cost={}, bound={}.".format(model.objective_value, model.objective_bound))
			elif status == OptimizationStatus.NO_SOLUTION_FOUND:
				print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))
				self.log_update_entry("Failed, bound={}.".format(model.objective_bound))

		# if no solution found, return inf cost
		if model.num_solutions == 0:
			conn.close()
			return float('inf'), [], {}

		# printing the solution if found
		out.write('Route with total cost %g found. \n' % (model.objective_value))

		if "-v" in params:
			out.write('\nEdges (In, Out, Weight):\n')  
			for i in E:
				out.write(str(i) + '\t')  

			out.write('\n\nCar - Chosen Edges:\n')       
			for i in x:
				out.write(str(i.x) + '\t')

			out.write('\n\nCar - Flow Capacities:\n')  
			for i in f:
				out.write(str(i.x) + '\t')

			out.write('\n\nTAs - Home Indices:\n')  
			for i in H:
				out.write(str(i) + '\n')

			out.write('\nTAs - Chosen Edges:\n')  
			for i in t:
				for j in range(len(i)):
					out.write(str(i[j].x) + '\t')
				out.write('\n') 

			out.write('\nTAs - Flow Capacities:\n')  
			for i in f_t:
				for j in range(len(i)):
					out.write(str(i[j].x) + '\t')
				out.write('\n')

			out.write('\nActive Edges:\n')  

			for i in range(len(x)):
				if (x[i].x >= 1.0):
					out.write('Edge from %i to %i with weight %f \n' % (E[i][0], E[i][1], E[i][2]))
			out.write('\n')

		list_of_edges = [E[i] for i in range(len(x)) if x[i].x >= 1.0]
		car_path_indices = self.construct_path(starting_car_index, list_of_edges, input_file)
		
		walk_cost, dropoffs_dict = self.find_best_dropoffs(G, home_indices, car_path_indices)

		if not seen:
			print("SAVING", input_file)
			c.execute('INSERT INTO models (input_file, best_objective_bound, optimal) VALUES (?, ?, ?)', \
				(input_file, model.objective_value, status == OptimizationStatus.OPTIMAL))
			conn.commit()
		elif model.objective_value < seen[0]:
			print("UPDATING", input_file)
			c.execute('UPDATE models SET best_objective_bound = ?, optimal = ? WHERE input_file = ?', \
				(model.objective_value, status == OptimizationStatus.OPTIMAL, input_file))
			conn.commit()
		if not "-s" in params:
			print("Walk cost =", walk_cost, "\n")

		conn.close()
		return model.objective_value, car_path_indices, dropoffs_dict