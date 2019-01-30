import urllib.request, urllib.parse
import json

address = input('Enter adress:')
apiurl = 'http://py4e-data.dr-chuck.net/json?'

parms = dict()
parms['address'] = address
parms['key'] = 42

url = apiurl + urllib.parse.urlencode(parms)

uh = urllib.request.urlopen(url)
data = uh.read().decode()
js = json.loads(data)

print(js['results'][0]['place_id'])