import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#url = input('Enter - ')
url = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrive all anchor tags
tags = soup('a') #<a....>...</a>
s = 0
c = 0
for tag in tags:
    print(tag)
    print(tag.get('href', None))
    print(tag.contents[0])
    print(tag.attrs)
