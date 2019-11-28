from student_utils import *
import itertools
from itertools import product
from sys import stdout as out
from mip import Model, xsum, minimize, BINARY, INTEGER
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

    def construct_path(self, start, edges):
        """
        Constructs a path from an unordered list of edges given some starting vertex
        Input:
            start: starting vertex
            edges: list of edges represented by integer pairs
        Output:
            List of edges in a path
        """
        edge_dict = {}
        for edge in edges:
            edge_dict[edge[0]] = edge_dict.get(edge[0], []) + [edge[1]]

        path = [start]
        current = start
        for _ in range(len(edges)):
            next_edges = edge_dict.get(current)
            if len(next_edges) == 1:
                next_vertex = next_edges[0]
                edge_dict.pop(current)

                path.append(next_vertex)
                current = next_vertex                
            else:
                for edge in next_edges:
                    if current in edge_dict.get(edge):
                        next_vertex = edge
                        edge_dict[current].remove(next_vertex)

                        path.append(next_vertex)
                        current = next_vertex
                        break
        return path

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
        
        home_indices = convert_locations_to_indices(list_of_homes, list_of_locations)
        location_indices = convert_locations_to_indices(list_of_locations, list_of_locations)

        G, message = adjacency_matrix_to_graph(adjacency_matrix)
        E = list(G.to_directed().edges(data='weight'))

        starting_car_index = list_of_locations.index(starting_car_location)

        # number of nodes and list of vertices, not including source or sink
        n, V, H = len(list_of_locations), location_indices, home_indices 
        bigNum = (n ** 2) 

        model = Model()

        # does the car drive from i to j?
        x = [model.add_var(var_type=BINARY) for e in E]

        # does the kth TA walk from i to j? over all num_homes TAs
        t = [[model.add_var(var_type=BINARY) for e in E] for k in H]

        # f_(u, v) = N; flow from vertex u to vertex v
        f = [model.add_var(var_type=INTEGER) for e in E] \
        + [model.add_var(var_type=INTEGER) for v in V] \
        + [model.add_var(var_type=INTEGER)]

        for i in range(len(f)):
            model += f[i] >= 0

        # For each vertex v where v != source and v != sink, Sum{x_(u, v)} = Sum{x_(v, w)}
        print(E)
        for v in V:
            model += xsum([x[i] for i in range(len(E)) if E[i][1] == v]) == xsum([x[i] for i in range(len(E)) if E[i][0] == v])

        # For each vertex v where v != source and v != sink, Sum{f_(u, v)} = Sum{f_(v, w)}
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
                 <= xsum([x[i] for i in range(len(E)) if E[i][1] \
                 == V[j]])

        # For just the source vertex, f_(source,start vertex)} = Sum{x_(a, b)}
        model += f[-1] == xsum(x)

        # For each TA k, for each vertex v, Sum{t^(i)_(u, v)} + Sum{x_(u, v)} >= Sum{t^(i)_(v, w)}
        for k in t:
            for v in V:
                model += xsum([k[i] for i in range(len(E)) if E[i][1] == v]) + xsum([x[i] for i in range(len(E)) if E[i][1] == v]) \
                 >= xsum([k[i] for i in range(len(E)) if E[i][0] == v])

        # For each TA k, for each home h, Sum{t^(i)_(u, h)} + Sum(x_(u, h)} > 0
        for j in range(len(t)):
            model += xsum([t[j][i] for i in range(len(E)) if E[i][1] == H[j]]) + xsum([x[i] for i in range(len(E)) if E[i][1] == H[j]]) >= 1

        # For each TA i, for each vertex v, Sum{t^(i)_(u, v)} <= 1
        for k in t:
            for v in V:
                model += xsum([k[i] for i in range(len(E)) if E[i][1] == v]) <= 1

        # objective function: minimize the distance
        cost_function = 2.0/3.0 * xsum([x[i] * E[i][2] for i in range(len(E))]) \
            + xsum([xsum([t[i][j] * E[j][2] for j in range(len(E))]) for i in range(len(t))])

        model.objective = minimize(cost_function)

        # WINNING ONLINE
        model.optimize()

        # printing the solution if found
        if model.num_solutions:
            out.write('Route with total cost %g found. \n' % (model.objective_value))

            out.write('\nEdges (In, Out, Weight):\n')  
            for i in E:
                out.write(str(i) + ' ')  

            out.write('\n\nCar - Chosen Edges:\n')       
            for i in x:
                out.write(str(i.x) + ' ')

            out.write('\n\nTAs - Chosen Edges:\n')  
            for i in t:
                for j in range(len(i)):
                    out.write(str(i[j].x) + ' ')
                out.write('\n') 

            out.write('\nFlow Capacities:\n')  
            for i in f:
                out.write(str(i.x) + ' ')
            out.write('\n') 

            out.write('\nActive Edges:\n')  

            for i in range(len(x)):
                if (x[i].x >= 1.0):
                    out.write('Edge from %i to %i with weight %f \n' % (E[i][0], E[i][1], E[i][2]))
            out.write('\n')

        list_of_edges = [E[i] for i in range(len(x)) if x[i].x >= 1.0]
        car_path_indices = self.construct_path(starting_car_index, list_of_edges)
        walk_cost, dropoffs_dict = self.find_best_dropoffs(G, home_indices, car_path_indices)

        return model.objective_value, car_path_indices, dropoffs_dict