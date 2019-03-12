import urllib.request, urllib.parse, urllib.error
from twurl import augment #generate url augments for url with secret tokens
import ssl
import json

TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

while True:
    acct = input('Enter account name:')
    if (len(acct) < 1): break
    url = twurl.augment(TWITTER_URL, {'screen_name': acct,'count':'5'})
    connection = urllib.request.urlopen(url, context=ctx) # ctx - security check off
    data = connection.read()
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    js = json.loads(data)
    print(json.dumps(js, indent=4))
    for u in js['users']:
        print(u['screen_name'])
        s=u['status']['text']
