import sqlite3

conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

cur.execute('SELECT sender, sent_at, message FROM Messages')

messages = list()
for message_row in cur:
    messages.append((message_row[0],message_row[1],message_row[2]))

print("Loaded messages=",len(messages))

counts = dict()
months = list()
senders = list()

for item in messages:
    sender = item[0]
    month = item[1][3:5] #7
    year = item[1][6:10]  # 7
    date = year+'.'+month
    if date not in months : months.append(date)
    if sender not in senders: senders.append(sender)
    key = (date, sender)
    counts[key] = counts.get(key,0) + 1

months.sort()

fhand = open('gline.js','w' ,encoding='utf8')
fhand.write("gline = [ ['Month'")
for sender in senders:
    fhand.write(",'"+sender+"'")
fhand.write("]")

for month in months:
    fhand.write(",\n['"+month+"'")
    for sender in senders:
        key = (month, sender)
        val = counts.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")
