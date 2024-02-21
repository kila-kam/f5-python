from urllib import request, parse
import ssl
import base64
import json

username="ansible"
password="Ans1bl3"
headers = {
    'Content-type': 'application/json',
}

myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE

req =  request.Request('https://192.168.1.254/mgmt/tm/ltm/virtual/?expandSubcollections=true', method="GET", headers=headers)

base64string = base64.b64encode(bytes('{}:{}'.format(username, password), 'ascii'))
req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))

resp = request.urlopen(req,context=myssl)
res_body = resp.read()
#print(res_body.decode('utf-8'))
data = json.loads(res_body.decode('utf-8'))
json_formatted_str = json.dumps(data, indent=2)
print (json_formatted_str)
f= open("data.json", "w") 
f.write(json_formatted_str)
