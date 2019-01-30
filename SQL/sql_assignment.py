import re, sqlite3

conn = sqlite3.connect('database/emaildb.sqlite')
cur = conn.cursor()

#cur.execute('''DROP TABLE IF EXIST Counts''')

cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

filename = 'mbox.txt'
data = open(filename)

pattern = '@([^ ]*)'

for line in data:
    if line.startswith('From '):
        org = re.findall(pattern, line)[0]
        cur.execute('SELECT count FROM Counts WHERE org = ?', (org,))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO Counts (org,count)
               VALUES (?,1)''', (org,))
        else:
            cur.execute('UPDATE Counts SET count = count +1 WHERE org = ?', (org,))
conn.commit()
