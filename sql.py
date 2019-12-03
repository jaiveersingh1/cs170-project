import sqlite3
import argparse
import utils

def print_local_table():
    conn = sqlite3.connect('models.sqlite')
    c = conn.cursor()
    results = c.execute("SELECT * FROM models ORDER BY input_file").fetchall()
    optimal = c.execute("SELECT * FROM models WHERE optimal = 1").fetchall()
    [print(i) for i in results]

    print()
    print("There are {} out of {} optimal results".format(len(optimal), len(results)))
    conn.commit()
    conn.close()

def run_queries():
    conn = sqlite3.connect('models.sqlite')
    c = conn.cursor()

    while True:
        command = input("Enter SQL command, or exit to quit: ")
        
        if command == "exit":
            conn.commit()
            conn.close()
            return
        
        results = c.execute(command).fetchall()

        print("Results:")
        [print(i) for i in results]
        print()

def merge_tables():

    NUM_ENTRIES = 500

    saved_tables = utils.get_files_with_extension("models/", 'sqlite')

    local_conn = sqlite3.connect('models.sqlite')
    local_cursor = local_conn.cursor()
    orig_local_res = local_cursor.execute("SELECT * FROM models ORDER BY input_file LIMIT {}".format(NUM_ENTRIES)).fetchall()
    
    for table in saved_tables:
        print(table)
        remote_conn = sqlite3.connect(table)
        remote_cursor = remote_conn.cursor()

        local_results = local_cursor.execute("SELECT * FROM models ORDER BY input_file LIMIT {}".format(NUM_ENTRIES)).fetchall()
        remote_results = remote_cursor.execute("SELECT * FROM models ORDER BY input_file LIMIT {}".format(NUM_ENTRIES)).fetchall()

        best_results = []

        def compare(a, b):
            if a[0] > b[0]:
                return a, True, False
            if b[0] > a[0]:
                return b, False, True

            if a[2] and not b[2]:
                return a, True, True
            if not a[2] and b[2]:
                return b, True, True

            if not a[2] and not b[2]:
                if a[1] < b[1]:
                    return a, True, True
                return b, True, True
            
            if a[2] and b[2]:
                if a[1] != b[1]:
                    print("DANGER: entries claim to both be optimal with different costs")
                    print(a)
                    print(b)
                return a, True, True


        while len(local_results) > 0 and len(remote_results) > 0:
            res_l = local_results[0]
            res_r = remote_results[0]

            better_result, pop_local, pop_remote = compare(res_l, res_r)

            best_results.append(better_result)
            if pop_local:
                local_results.pop(0)
            if pop_remote:
                remote_results.pop(0)

        best_results += local_results + remote_results            
        
        remote_conn.close()
    local_conn.close()

    new_table = input("Where to save new output? ")
    new_conn = sqlite3.connect(new_table)
    new_cursor = new_conn.cursor()
    new_cursor.execute("CREATE TABLE IF NOT EXISTS models (input_file TEXT PRIMARY KEY, best_objective_bound NUMERIC, optimal INTEGER)")
    for result in best_results:
        new_cursor.execute('REPLACE INTO models (input_file, best_objective_bound, optimal) VALUES (?, ?, ?)', result)
    new_conn.close()
    
    print("Local: ")
    [print(i) for i in orig_local_res]
    print()

    print("Best: ")
    [print(i) for i in best_results]
    print()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('command', type=str, choices=['print', 'merge', 'query'], help='The command to run')
    args = parser.parse_args()
    if args.command == 'print':
        print_local_table()
    elif args.command == 'merge':
        merge_tables()
    elif args.command == 'query':
        run_queries()
    else:
        print("Unsupported command")