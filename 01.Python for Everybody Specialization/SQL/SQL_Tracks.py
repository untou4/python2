import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('database/trackdb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Tracks;

CREATE TABLE Artists (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Albums (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Tracks (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);''')

fname = 'data/Library.xml'

def lookup(d, key): #looking for a 'key' key
    found = False
    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')# tracks in branck dict-dict-dict
print('Dict count:', len(all))
for entry in all:
    if ( lookup(entry, 'Track ID') is None) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None :
        continue

    cur.execute('''INSERT OR IGNORE INTO Artists (name)
        VALUES (?)''', (artist,)) #if it already ther then ignore it, work only in SQLite
    cur.execute('SELECT id FROM Artists WHERE name = ?', (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Albums (title, artist_id)
            VALUES (?,?)''', (album,artist_id))
    cur.execute('SELECT id FROM Albums WHERE title = ?', (album,))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Tracks
        (title, album_id, len, rating, count)
        VALUES (?,?,?,?,?)''',
        (name, album_id,length,rating,count))

    conn.commit()