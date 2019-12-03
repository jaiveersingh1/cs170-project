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
    saved_tables = utils.get_files_with_extension("models/", 'sqlite')

    local_conn = sqlite3.connect('models.sqlite')
    local_cursor = local_conn.cursor()
    for table in saved_tables:
        print(table)
        remote_conn = sqlite3.connect(table)
        remote_cursor = remote_conn.cursor()

        local_results = local_cursor.execute("SELECT * FROM models ORDER BY input_file LIMIT 5").fetchall()
        remote_results = remote_cursor.execute("SELECT * FROM models ORDER BY input_file LIMIT 5 ").fetchall()

        combined_results = []
        #print(local_results)
        print(remote_results)


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