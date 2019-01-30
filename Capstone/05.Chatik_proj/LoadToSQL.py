import sqlite3
from bs4 import BeautifulSoup
import glob, os

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
                body = get_child(child,'body')
                if body is None:
                    continue
                date = get_child(body, 'pull_right date details').attrs.get('title')
                sender = get_child(body, 'from_name').text.strip().replace('\n','')
                texttag = get_child(body, 'text')
                if not texttag is None:
                    text = texttag.text.strip().replace('\n','')
                    #print(date, ', ', sender, ':', text)
                    cur.execute('''INSERT OR IGNORE INTO Messages (id, Sender, sent_at, message)
                            VALUES ( ?, ?, ?, ? )''', (start, sender, date, text))
                    start +=1
    conn.commit()

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()
start = 0

cur.execute('''DROP TABLE IF EXISTS Messages''')
cur.execute('''CREATE TABLE Messages (id INTEGER UNIQUE, Sender TEXT, sent_at TEXT, message TEXT)''')

path = '/ChatExport_11_01_2019/'
os.chdir(path)
for file in os.listdir(path):
    a=file

#file = open("C:\Python\SourceFiles\Capstone\\05.Chatik_proj\ChatExport_11_01_2019\messages.html", encoding="utf-8").read()
#parsefile(file, start)

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

