class BaseSolver:
    """ Base class for solvers """

    def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
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
    
    def findBestDropoffs(list_of_locations, list_of_homes, list_of_car_visits, adjacency_matrix):
        """
        Treating the car's cycle as constant, find the best dropoff locations for the TAs to minimize walking cost.
        Input:
            list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
            list_of_homes: A list of homes
            list_of_car_visits: A list of locations representing the car path
            adjacency_matrix: The adjacency matrix from the input file
        Output:
            A cost of how expensive the current solution is
            A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
            NOTE: all outputs should be in terms of indices not the names of the locations themselves
        """

        shortestDistances = [[None for c in adjacency_matrix] for r in adjacency_matrix]
        print(shortestDistances)
        # Use Floyd-Warshall Algorithm to find shortest paths between every pair of points




def randomSolveJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    
    return 0, [], dict()

def bruteForceJS(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, params=[]):
    