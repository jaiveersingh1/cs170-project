import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from solver_toolbox import *

from student_utils import *
"""
======================================================================
  Complete the following function.
======================================================================
"""

# Initialize solvers and modes
ilp_solver = ILPSolver()
brute_force_solver = BruteForceJSSolver()
naive_solver = NaiveSolver()

solvers_mode = {
    "all": [ilp_solver, brute_force_solver],
    "bf": [brute_force_solver],
    "ilp": [ilp_solver],
    "naive": [naive_solver]
}

# One-time initialization of logfiles for this run
for solver in solvers_mode["all"]:
    timestamp = time.strftime("%d-%m-%y_%H-%M-%S")
    solver.logfile = "logfiles/logfile_{}.txt".format(timestamp)

# Init colorama
init()

def solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_locations: A list of locations such that node i of the graph corresponds to name at index i of the list
        list_of_homes: A list of homes
        starting_car_location: The name of the starting location for the car
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        A list of locations representing the car path
        A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
        NOTE: both outputs should be in terms of indices not the names of the locations themselves
    """
    best_solution = (float('inf'), [], {})

    conn = sqlite3.connect('models.sqlite')
    c = conn.cursor()

    prev = c.execute('SELECT best_objective_bound FROM models WHERE input_file = (?)', (input_file,)).fetchone()
    conn.close()

    
    mode = "ilp"
    if "-m" in params:
        mode = params[params.index("-m") + 1]

    for solver in solvers_mode[mode]:

        solution = solver.solve(list_of_locations, list_of_homes, starting_car_location, adjacency_matrix, input_file, params)
        if best_solution == None or solution[0] < best_solution[0]:
            best_solution = solution

    return ("--force-write" in params or not prev or prev[0] > best_solution[0]), best_solution[1], best_solution[2]

"""
======================================================================
   No need to change any code below this line
======================================================================
"""

"""
Convert solution with path and dropoff_mapping in terms of indices
and write solution output in terms of names to path_to_file + file_number + '.out'
"""
def convertToFile(path, dropoff_mapping, path_to_file, list_locs):
    string = ''
    for node in path:
        string += list_locs[node] + ' '
    string = string.strip()
    string += '\n'

    dropoffNumber = len(dropoff_mapping.keys())
    string += str(dropoffNumber) + '\n'
    for dropoff in dropoff_mapping.keys():
        strDrop = list_locs[dropoff] + ' '
        for node in dropoff_mapping[dropoff]:
            strDrop += list_locs[node] + ' '
        strDrop = strDrop.strip()
        strDrop += '\n'
        string += strDrop
    utils.write_to_file(path_to_file, string)

def solve_from_file(input_file, output_directory, params=[]):
    print('\nProcessing', input_file)

    conn = sqlite3.connect('models.sqlite')
    c = conn.cursor()

    input_file_name = input_file.split('/')[-1]

    optimal = c.execute('SELECT optimal FROM models WHERE input_file = (?)', (input_file_name,)).fetchone()
    conn.close()

    # skip over optimal inputs
    if optimal and optimal[0] and "--no-skip" not in params:
        print('SKIPPPING', input_file_name)
        return

    input_data = utils.read_file(input_file)
    num_of_locations, num_houses, list_locations, list_houses, starting_car_location, adjacency_matrix = data_parser(input_data)
    improved, car_path, drop_offs = solve(list_locations, list_houses, starting_car_location, adjacency_matrix, input_file_name, params=params)

    # only write out file if we got a better cost
    if not improved:
        print(input_file_name, 'DIDN\'T IMPROVE')
        return

    basename, filename = os.path.split(input_file)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    output_file = utils.input_to_output(input_file, output_directory)
    convertToFile(car_path, drop_offs, output_file, list_locations)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for i, input_file in enumerate(input_files):
        print (f"~~ Solving file {i + 1} of {len(input_files)} ~~")
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = 'submissions/submission_final/'
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
