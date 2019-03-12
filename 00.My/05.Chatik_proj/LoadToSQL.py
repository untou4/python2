import sqlite3, os
from bs4 import BeautifulSoup

def get_child(tag,classname):
    for i in range(len(tag.contents)):
        if tag.contents[i] != '\n' and tag.contents[i].get('class',0) != 0\
                and ' '.join(tag.contents[i].get('class', 0)) == classname:
            return tag.contents[i]
    return None

def parsefile(file, start):
    soup = BeautifulSoup(file, 'html.parser')
    history = soup.html.body.div.contents[3].div
    for child in history.children:
        if child != '\n' and child.get('class', 0) != 0 :
            с = ' '.join(child.attrs.get('class'))
            if с == 'message default clearfix':
                body = get_child(child, 'body')
                if body is None:
                    continue
                date = get_child(body, 'pull_right date details').attrs.get('title')
                sender = get_child(body, 'from_name').text.strip().replace('\n', '')
                #Сусов Роман via @ya
                if sender.find('via') != -1:
                    sender = sender[:sender.find('via')]
                sender = sender.strip()
                texttag = get_child(body, 'text')
                if not texttag is None:
                    text = texttag.text.strip().replace('\n','')
                    cur.execute('''INSERT OR IGNORE INTO Messages (id, Sender, sent_at, message)
                            VALUES ( ?, ?, ?, ? )''', (start, sender, date, text))
                    start +=1
            elif с == 'message default clearfix joined':
                body = get_child(child, 'body')
                if body is None:
                    continue
                date = get_child(body, 'pull_right date details').attrs.get('title')
                texttag = get_child(body, 'text')
                if not texttag is None:
                    text = texttag.text.strip().replace('\n', '')
                    cur.execute('''INSERT OR IGNORE INTO Messages (id, Sender, sent_at, message)
                                           VALUES ( ?, ?, ?, ? )''', (start, sender, date, text))
                    start += 1
    conn.commit()
    return start

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
start = 0

cur.execute('''DROP TABLE IF EXISTS Messages''')
cur.execute('''CREATE TABLE Messages (id INTEGER UNIQUE, Sender TEXT, sent_at TEXT, message TEXT)''')

path = 'C:/ChatExport_11_01_2019/'
os.chdir(path)
for filename in os.listdir(path):
    file = open(os.path.join(path, filename), encoding="utf-8").read()
    start = parsefile(file, start)

cur.execute('SELECT COUNT(*) FROM Messages ')
row = cur.fetchone()
if row is None:
    print('There are no messages')
else:
    print('There are', row[0], 'messages in database')

cur.close()

#classes = list()
#['message service', 'message default clearfix', 'message default clearfix joined', 'pagination block_link']
# for child in history.children:
#     if child != '\n' and child.attrs.get('class',0) != 0 :
#         с = ' '.join(child.attrs.get('class'))
#         if с == 'message service':
#             print(child.text.strip().replace('\n',''))
#         if с not in classes:
#             classes.append(с)
#print(classes)

