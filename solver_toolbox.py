import networkx as nx

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

def bruteForceJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    pass