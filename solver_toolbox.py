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
    
    def find_best_dropoffs(self, list_of_locations, list_of_homes, list_of_car_stops, adjacency_matrix):
        """
        Treating the car's cycle as constant, find the best dropoff locations for the TAs to minimize walking cost.
        Input:
            list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
            list_of_homes: A list of homes
            list_of_car_stops: A list of locations representing the car path
            adjacency_matrix: The adjacency matrix from the input file
        Output:
            Total walking cost (TA ONLY)
            A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
            NOTE: all outputs should be in terms of indices not the names of the locations themselves
        """

        # Initialize shortest_distances matrix, where shortest_distances[r][c] is the shortest distance from r to c

        V = len(adjacency_matrix)
        shortest_distances = [[None for c in range(V)] for r in range(V)]
        for r in range(V):
            for c in range(V):
                if c == r:
                    shortest_distances[r][c] = 0
                elif adjacency_matrix[r][c] == 'x':
                    shortest_distances[r][c] = float('inf')
                else:
                    shortest_distances[r][c] = adjacency_matrix[r][c]
        
        # Use Floyd-Warshall Algorithm to find shortest paths between every pair of points
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    shortest_distances[i][j] = min(shortest_distances[i][j], shortest_distances[i][k] + shortest_distances[k][j])
        
        # Translate home names into indices
        home_indices = []
        for home_name in list_of_homes:
            home_indices.append(list_of_locations.index(home_name))

        # Determine TA dropoff
        dropoffs = {}
        total_cost = 0

        for home in home_indices:

            # Find preferred dropoff location for this TA
            best_dropoff = None
            for dropoff in list_of_car_stops:
                if best_dropoff == None or shortest_distances[dropoff][home] < shortest_distances[best_dropoff][home]:
                    best_dropoff = dropoff

            dropoffs[best_dropoff] = dropoffs.get(best_dropoff, []) + [home]
            total_cost += shortest_distances[best_dropoff][home]
        
        return total_cost, dropoffs



def randomSolveJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    
    return 0, [], dict()

def bruteForceJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    pass