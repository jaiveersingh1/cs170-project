from student_utils import *
import itertools

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