import requests

r = request.get(‘http://www.reddit.com/user/spilcm/comments/.json’)

data = r.json()
