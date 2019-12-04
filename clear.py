import sqlite3
conn = sqlite3.connect('models.sqlite')
c = conn.cursor()
c.execute("DELETE FROM models")
conn.commit()
conn.close()