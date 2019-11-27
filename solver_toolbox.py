from student_utils import *
import itertools
from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY
import matplotlib.pyplot as plt
import networkx
import utils

class BaseSolver:
    """ Base class for solvers """

    def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
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



def randomSolveJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    
    return 0, [], dict()


class BruteForceJSSolver(BaseSolver):
    def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
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
            
            for edge in edge_set:
                exit_counts[edge[0]] += 1
                entry_counts[edge[1]] += 1
                visited.add(edge[1])
                driving_cost += 2/3 * edge[2]
            
            valid_cycle = (starting_car_index in visited) and all([entry_counts[i] == exit_counts[i] for i in range(len(list_of_locations))])
            if valid_cycle:
                walking_cost, dropoffs = self.find_best_dropoffs(G, home_indices, list(visited))
                total_cost = walking_cost + driving_cost
                if total_cost < best_solution[0]:
                    best_solution = (total_cost, [], dropoffs)

        
        print("\n\nBest cost was", best_solution[0])
        return best_solution

class ILPSolver(BaseSolver):
    def solve(self, list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
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
        '''
        home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)

        G, message = adjacency_matrix_to_graph(adjacency_matrix)
        E = G.to_directed().edges(data='weight')

        starting_car_index = list_of_locations.index(starting_car_location)
        best_solution = (float('inf'), [], {})

        print("\n\nBest cost was", best_solution[0])
        return best_solution
        '''

        # number of nodes and list of vertices
        n, V, H = len(list_of_locations), range(len(list_of_locations)), range(len(list_of_homes))    

        model = Model()

        # binary variables indicating if arc (i,j) is used on the route or not
        x = [[model.add_var(var_type=BINARY) for j in V] for i in V]

        # continuous variable to prevent subtours: each city will have a
        # different sequential id in the planned route except the first one
        y = [model.add_var() for i in V]

        # objective function: minimize the distance
        model.objective = minimize(xsum(adjacency_matrix[i][j]*x[i][j] for i in V for j in V))

        # constraint : leave each city only once
        for i in V:
            model += xsum(x[i][j] for j in set(V) - {i}) == 1

        # constraint : enter each city only once
        for i in V:
            model += xsum(x[j][i] for j in set(V) - {i}) == 1

        # subtour elimination
        for (i, j) in set(product(set(V) - {0}, set(V) - {0})):
                model += y[i] - (n+1)*x[i][j] >= y[j]-n

        # optimizing
        model.optimize()

        # checking if a solution was found
        if model.num_solutions:
            out.write('Route with total distance %g found: %s' % (model.objective_value, starting_car_location))
            nc = 0
            while True:
                nc = [i for i in V if x[nc][i].x >= 0.99][0]
                out.write(' -> %s' % list_of_locations[nc])
                if nc == 0:
                    break
            out.write('\n')


tsp = ILPSolver()
input_data = utils.read_file("inputs/300_50.in")
num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)

for i in range(len(adjacency_matrix)):
    for j in range(len(adjacency_matrix)):
        if (adjacency_matrix[i][j] == 'x' and i == j):
            adjacency_matrix[i][j] = 0
        elif (adjacency_matrix[i][j] == 'x'):
            adjacency_matrix[i][j] = 43298432 # big number

tsp.solve(list_locations, list_houses, starting_car_location, adjacency_matrix)
