import sqlite3
import argparse
import utils
import shutil
import os

from output_validator import *

def print_local_table(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    results = c.execute("SELECT * FROM models ORDER BY input_file").fetchall()
    optimal = c.execute("SELECT * FROM models WHERE optimal = 1").fetchall()
    [print(i) for i in results]

    print()
    print("There are {} out of {} optimal results".format(len(optimal), len(results)))
    conn.commit()
    conn.close()

def run_queries(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    while True:
        command = input("Enter SQL command, or 'exit' to quit: ")
        
        if command == "exit":
            conn.commit()
            conn.close()
            return
        
        try:
            results = c.execute(command).fetchall()
            print("Results:")
            [print(i) for i in results]
            print()
        except:
            print("Invalid query.")
        

def merge_tables(filename):
    saved_tables = utils.get_files_with_extension("models/", 'sqlite')
    
    local_conn = sqlite3.connect(filename)
    local_cursor = local_conn.cursor()
    local_res = local_cursor.execute("SELECT * FROM models ORDER BY input_file").fetchall()
    local_conn.close()

    new_table = input("Where to save new output? ")
    new_conn = sqlite3.connect(new_table)
    new_cursor = new_conn.cursor()
    new_cursor.execute("DROP TABLE IF EXISTS models")
    new_cursor.execute("CREATE TABLE IF NOT EXISTS models (input_file TEXT PRIMARY KEY, best_objective_bound NUMERIC, optimal INTEGER)")

    for result in local_res:
        new_cursor.execute('INSERT INTO models (input_file, best_objective_bound, optimal) VALUES (?, ?, ?)', result)

    for table in saved_tables:
        remote_conn = sqlite3.connect(table)
        remote_cursor = remote_conn.cursor()
        remote_results = remote_cursor.execute("SELECT * FROM models ORDER BY input_file").fetchall()

        def compare(a, b):
            if a[2] and b[2]:
                if a[1] != b[1]:
                    print("DANGER: entries claim to both be optimal with different costs")
                    print(a)
                    print(b)
                else:
                    return min([a, b], key = lambda x: x[1])

            if a[2] and not b[2] and a[1] >= b[1]:
                print("DANGER: optimal entry has greater cost than non-optimal")
                print(a)
                print(b)
                return a
            elif not a[2] and b[2] and a[1] <= b[1]:
                print("DANGER: optimal entry has greater cost than non-optimal")
                print(a)
                print(b)
                return b

            return a if a[1] < b[1] else b

        for result in remote_results:
            seen = new_cursor.execute('SELECT * FROM models WHERE input_file = (?)', [result[0]]).fetchone()
            if not seen:
                new_cursor.execute('INSERT INTO models (input_file, best_objective_bound, optimal) VALUES (?, ?, ?)', result)
            else:
                comp = compare(seen, result)
                new_cursor.execute('UPDATE models SET best_objective_bound = ?, optimal = ? WHERE input_file = ?', (comp[1], comp[2], comp[0]))
        
        remote_conn.close()            
                
    new_conn.commit()
    new_conn.close()    

def remaining(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    input_folder = input("Which folder to check against? ")
    inputs = [file.split("/")[-1] for file in utils.get_files_with_extension(input_folder, 'in')]
    results = [file[0] for file in c.execute("SELECT input_file FROM models").fetchall()]
    remaining = []
    for i in inputs:
        if i not in results:
            remaining.append(i)
            print(i)

    conn.commit()
    conn.close()

    print(f"There are {len(remaining)} files remaining.")

    splitter('remaining', remaining)
    
def splitter(new_directory, files):
    num_batches = int(input("How many batches to split into? (-1 to skip) "))
    if num_batches == -1:
        return

    factor = int(len(files) / num_batches)

    for i in range(num_batches):
        directory = "batches/split_{}/batch{}/".format(new_directory, i)
        print("CREATED", directory)
        os.makedirs(directory)

        for file in files[i * factor: (i + 1) * factor]:
            shutil.copy("batches/inputs/{}".format(file), directory + file)

def split(input_folder):
    inputs = [file.split("/")[-1] for file in utils.get_files_with_extension(input_folder, 'in')]
    splitter(input_folder.split('/')[-1], inputs)


def discrepancy_check(filename, allowance):
    conn = sqlite3.connect('models.sqlite')
    c = conn.cursor()
    output_directory = "submissions/submission_final/"

    logfile = open("batches/batch_discrepancy/logfile.txt", "a")

    print("Checking for discrepancies between MODELS table and submissions_final directory...")

    for entry in os.scandir(output_directory): 
        output_file = entry.path
        output_file_name = output_file.split('/')[-1]
        input_file_name = output_file_name.split('.')[0] + ".in"
        input_file = "batches/inputs/" + input_file_name

        query_result = c.execute('SELECT optimal, best_objective_bound FROM models WHERE input_file = (?)', (input_file_name,)).fetchone()
        cost_from_file = validate_output_nm(input_file, output_file)

        if (not query_result):
            logfile.write(input_file_name.split('.')[0] + ": " + "File is not in the MODELS table, but has an output in the submission_final directory.\n")
            if (not os.path.exists("batches/batch_discrepancy/" + input_file_name + ".in")):
                shutil.copy(input_file, "batches/batch_discrepancy")
        elif ((abs(query_result[1] - cost_from_file) / query_result[1]) * 100 >= allowance):
            logfile.write(output_file_name.split('.')[0] + ": " + "MODELS cost is " + str(query_result[1]) \
                + " but OV cost " + str(cost_from_file) + ". Percent Differential: " + \
                    str(((query_result[1] - cost_from_file) / query_result[1]) * 100) + ".\n")
            if (not os.path.exists("batches/batch_discrepancy/" + input_file_name + ".in")):
                shutil.copy(input_file, "batches/batch_discrepancy")

    results = [file[0] for file in c.execute("SELECT input_file FROM models").fetchall()]
    for file in results:
        if (not os.path.exists(output_directory + file.split('.')[0] + ".out")):
            logfile.write(file.split('.')[0] + ": " + "File is in the MODELS table, but does not have an output in the submission_final directory.\n")
            if (not os.path.exists("batches/batch_discrepancy/" + file)):
                shutil.copy("batches/inputs/" + file, "batches/batch_discrepancy")

    logfile.close()
    conn.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('command', type=str, choices=['print', 'merge', 'query', 'remaining', 'discrepancy', 'split'], help='The command to run')
    parser.add_argument('input', type=str, help='The path to the input table')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()

    if args.command == 'print':
        print_local_table(args.input)
    elif args.command == 'merge':
        merge_tables(args.input)
    elif args.command == 'query':
        run_queries(args.input)
    elif args.command == 'remaining':
        remaining(args.input)
    elif args.command == 'discrepancy':
        allowance = 0.1
        if '-p' in args.params:
            allowance = float(args.params[args.params.index("-p") + 1])
        discrepancy_check(args.input, allowance)
    elif args.command == 'split':
        split(args.input)
    else:
        print("Unsupported command")