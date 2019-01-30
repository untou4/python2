import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

def follow(tek,count,pos,url):

    if tek >count:
        return ''

    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('a')
    tag = tags[pos-1]
    return tag.contents[0] + ' ' + follow(tek+1,count,pos,tag.get('href', None))

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = input('Enter - ')
#count = input('Enter count:')
#position = input('Enter position')

url = 'http://py4e-data.dr-chuck.net/known_by_Alekzander.html'
count = 7
position = 18

print(follow(0,count-1,position,url))


