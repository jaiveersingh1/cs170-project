import os
import argparse
import shutil

def copy(directory, new_dir, input_file):
	shutil.copy(directory + input_file, new_dir + input_file)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Parsing arguments')
	parser.add_argument('--all', action='store_true', help='If specified, the output validator is run on all files in the output directory. Else, it is run on just the given output file')
	old_dir = input("Where are your current files located? ")
	new_dir = input("Where do you want to put these files? ")
	os.makedirs(new_dir, exist_ok = True)
	while True:
		file = input("Input file name or type 'exit' to quit: ")
		if file == 'exit':
			break
		copy(old_dir, new_dir, file)
