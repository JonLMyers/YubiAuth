import requests
import json

token = ''

print("######## Pass/Fail ########")
target = 'http://127.0.0.1:5000/registration'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'test@testing.com', 'password': 'password123'}
r = requests.post(target, data=json.dumps(data), headers=headers)
data = json.loads(r.text)
print(r.status_code, r.reason)
print(r.text)