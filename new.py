import json
import sqlite3


conn = sqlite3.connect('databases/trackdb.sqlite')
cur = conn.cursor()

cur.execute('SELECT name FROM Artists WHERE name = ? ', ('asd', ))
print(cur.fetchone())