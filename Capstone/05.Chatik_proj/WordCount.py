import sqlite3, string

skipdict=('есть','если')
#'что','все','это','как','так','вот','там','еще','тут','для','уже',

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT message FROM Messages')
counts = dict()
c=0
for message_row in cur :
    text = message_row[0]
    text = text.translate(str.maketrans('','',string.punctuation))
    text = text.translate(str.maketrans('','','1234567890'))
    text = text.strip()
    text = text.lower()
    words = text.split()
    for word in words:
        if len(word) < 4 : continue
        if word in skipdict: continue
        if word[-1]=='о' or word[-1]=='е': continue
        counts[word] = counts.get(word,0) + 1
    c+=1
    #if c==100000:
    #    break

x = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for k in x[:100]:
    if highest is None or highest < counts[k] :
        highest = counts[k]
    if lowest is None or lowest > counts[k] :
        lowest = counts[k]
print('Range of counts:',highest,lowest)

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('gword.js','w',encoding='utf8')
fhand.write("gword = [")
first = True
for k in x[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")
fhand.close()

print("Output written to gword.js")
print("Open gword.htm in a browser to see the vizualization")