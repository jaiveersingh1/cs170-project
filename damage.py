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

conn = sqlite3.connect('damages.sqlite')
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS damages")
c.execute("CREATE TABLE damages (input_file TEXT PRIMARY KEY, damage NUMERIC)")

files = []
for file, score, optimal in pbar(results):
	file = file.split('.')[0]
	our_cost = validate_output_nm('batches/inputs/{}.in'.format(file), 'submissions/submission_final/{}.out'.format(file))

	input_data = read_file('batches/inputs/{}.in'.format(file))
	number_of_locations, number_of_houses, list_of_locations, list_of_houses, starting_location, adjacency_matrix = data_parser(input_data)

	path = convert_locations_to_indices([starting_location], list_of_locations)
	homes = convert_locations_to_indices(list_of_houses, list_of_locations)
	dropoffs = {path[0]: homes}
	G, message = adjacency_matrix_to_graph(adjacency_matrix)
	bad_cost, message = cost_of_solution(G, path, dropoffs)

	damage = our_cost / bad_cost * 100.0

	c.execute('INSERT INTO damages (input_file, damage) VALUES (?, ?)', (file, damage))


	files.append((damage, file, optimal))

files.sort(key = lambda x: x[0])
conn.commit()
conn.close()

print("\n\nDamaging Files")
total = 0
for f in files:
	total += f[0]
	if f[2] == 0:
		print(f)

print(total / len(files))
