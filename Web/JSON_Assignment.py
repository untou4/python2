import json
import urllib.request, urllib.error

url = 'http://py4e-data.dr-chuck.net/comments_57695.json'

text = urllib.request.urlopen(url).read()
data = json.loads(text)
list=data['comments']
sum = 0
for item in list:
    sum += int(item['count'])

print(sum)


