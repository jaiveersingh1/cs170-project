import sqlite3
from output_validator import *
from utils import *
from progressbar import ProgressBar

conn = sqlite3.connect('models.sqlite')
c = conn.cursor()

results = c.execute("SELECT * FROM models ORDER BY input_file").fetchall()

conn.commit()
conn.close()

pbar = ProgressBar()

files = []
for file, score, optimal in pbar(results):
	if optimal == '1':
		pass
	file = file.split('.')[0]
	our_cost = validate_output_nm('batches/inputs/{}.in'.format(file), 'submissions/submission_final/{}.out'.format(file))

	input_data = read_file('batches/inputs/{}.in'.format(file))
	number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(input_data)

	path = convert_locations_to_indices([starting_location], list_of_locations)
	homes = convert_locations_to_indices(list_of_houses, list_of_locations)
	dropoffs = {path[0]: homes}
	G, message = adjacency_matrix_to_graph(adjacency_matrix)
	bad_cost, message = cost_of_solution(G, path, dropoffs)

	files.append((our_cost / bad_cost, file))

files.sort(key = lambda x: x[0])

print("\n\nDamaging Files")
for f in files:
	print(f)
