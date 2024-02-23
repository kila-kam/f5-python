from urllib import request,parse,error
from datetime import datetime
import ssl
import base64
import json
import getpass
import os

dt=datetime.now()
start_date=dt.strftime('_%d%b%Y_%H_%M')

username= input("Username: ")
password= getpass.getpass()

headers = {
    'Content-type': 'application/json',
}

devices = list(open('devicesf5.txt'))

urls=[  
       { 'filename': 'virtual',
         'url':'https://{}/mgmt/tm/ltm/virtual/?expandSubcollections=true'},
       { 'filename': 'pool',
         'url':'https://{}/mgmt/tm/ltm/pool/?expandSubcollections=true'},
        { 'filename': 'node',
         'url':'https://{}/mgmt/tm/ltm/node'},       
       { 'filename': 'snatpool',
         'url':'https://{}/mgmt/tm/ltm/snatpool/'},
#       { 'filename': 'persistence',
#         'url':'https://{}/mgmt/tm/ltm/persistence/'},
       { 'filename': 'client-ssl',
         'url':'https://{}/mgmt/tm/ltm/profile/client-ssl/?expandSubcollections=true'},
       { 'filename': 'server-ssl',
         'url':'https://{}/mgmt/tm/ltm/profile/server-ssl/?expandSubcollections=true'},
#      { 'filename': 'monitor',
#         'url':'https://{}/mgmt/tm/ltm/monitor/'},
]

myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE

for device in devices:
    try:
        path = 'output/{}'.format(device)
        if not os.path.exists(path):
            os.makedirs(path)
        for url in urls:
            req =  request.Request(url['url'].format(device), method="GET", headers=headers)
            base64string = base64.b64encode(bytes('{}:{}'.format(username, password), 'ascii'))
            req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))
            resp = request.urlopen(req,context=myssl)
            res_body = resp.read()
            data = json.loads(res_body.decode('utf-8'))
            json_formatted_str = json.dumps(data, indent=2)
            f= open( '{}/{}-{}{}.json'.format(path,device,url['filename'],start_date), "w") 
            f.write(json_formatted_str)
            f.close
    except error.HTTPError as e: 
        print('HTTP Error 401: F5 Authorization Required or wrong username/password')
