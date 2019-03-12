import urllib.request, urllib.error
import ssl
import xml.etree.ElementTree as ET

url = 'http://py4e-data.dr-chuck.net/comments_57694.xml'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

xml = urllib.request.urlopen(url, context=ctx).read()

stuff = ET.fromstring(xml)
print(xml)

lst = stuff.findall('comments/comment')
sum =0
for item in lst:
    sum += int(item.find('count').text)

print(sum)