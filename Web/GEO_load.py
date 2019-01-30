import urllib.parse, urllib.request
import json, http
import sqlite3,time,ssl,sys

serviceurl = "https://py4e-data.dr-chuck.net/geojson?"

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("data/where.data")
count = 0
for line in fh:
    if count > 200:
        print('Retrieved 200 locations, restart to retrieve more')
        break

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address = ?", (memoryview(address.encode()),))

    try:
        data = cur.fetchone()[0]
        print("Found in database",address)
        continue
    except:
        pass

    params = dict()
    params["query"]=address
    url = serviceurl + urllib.parse.urlencode(params)

    print('Retrieving',url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved',len(data),'characters',data[:20].replace('\n', ' '))
    count += 1

    try:
        js = json.loads(data)
    except:
        print(data)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('==== Failure Ro Retrieve ====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
        VALUES (?,?)''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()

    if count %10 == 0:
        print('Pausing for a bit...')
        time.sleep(5)

print("Rum geodump to read the data from the database so you can vizualize it")