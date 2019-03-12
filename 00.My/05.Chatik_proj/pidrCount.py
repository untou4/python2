import sqlite3, string

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT sender, sent_at, message FROM Messages')

for message_row in cur :
    if message_row[2].find(' пидр ') != -1:
        text = message_row[2].translate(str.maketrans('', '', string.punctuation))
        words =text.split()
        if words.index('пидр')!=0:
            print('meessage:',message_row[2])
            print('pidr:',words[words.index('пидр')-1])