import sqlite3
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open('data/2018.html', encoding='utf8')

soup = BeautifulSoup(fh, 'html.parser')

tags = soup('table')

for tag in tags:
    if tag.get('id') and tag['id'] == 'economicCalendarData':
        for childtag in tag.contents:
            if childtag.name == 'tbody':
                c=0
                for data in childtag.contents:
                    try:
                        if data.get('id'):
                            print(data, '\n')
                            c+=1
                            if c >10 : break
                    except:
                        continue


#conn = sqlite3.connect('events.sqlite')
#cur = conn.cursor()