import sqlite3
conn = sqlite3.connect('models.sqlite')
c = conn.cursor()
results = c.execute("SELECT * FROM models ORDER BY input_file").fetchall()
optimal = c.execute("SELECT * FROM models WHERE optimal = 1").fetchall()
[print(i) for i in results]

print()
print("There are {} out of {} optimal results".format(len(optimal), len(results)))
conn.commit()
conn.close()