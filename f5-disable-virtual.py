from urllib import request,parse,error
import ssl
import base64
import json
import csv
import getpass

username= input("Username: ")
password= getpass.getpass()

headers = {
    'Content-type': 'application/json',
}

devices = list(open('devicesf5.txt'))

myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE

url = 'https://{}/mgmt/tm/ltm/virtual/{}' # Set destination URL here
body = {"disabled" : True }     # Set POST fields here
data = json.dumps(body).encode()

#iterate through devices 
for device in devices:
    response_data_list= list()
    try:
        virtuals = list(open('f5-virtual-servers/{}-vs.txt'.format(device)))
        for virtual in virtuals:
#iterate through virtual servers per device 
            response_data_dict=dict()
            req =  request.Request(url.format(device,virtual),data=data,method='PATCH',headers=headers)
            base64string = base64.b64encode(bytes('{}:{}'.format(username, password), 'ascii'))
            req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))
            response = request.urlopen(req,context=myssl)
            response_body = response.read().decode()
            response_data = json.loads(response_body)
# add virtual server name and disable status to the response_data_list 
            response_data_dict['device'] = device
            response_data_dict['name'] = response_data['name']
            response_data_dict['disabled'] = response_data.get('disabled', 'N/A')
            response_data_dict['enabled'] = response_data.get('enabled', 'N/A')
            print(response_data_dict)
# append dictionary data to list for post validation 
            response_data_list.append(response_data_dict)
  #          json_formatted_str = json.dumps(response_data, indent=2)
    except error.HTTPError as e:
        print(e.code)
        print(e.read())

# add response body to empty list and print create dynamic csv file per device for post validation 
with open('f5_disable_post_validation.csv','w') as file:
     writer = csv.writer(file)
     writer.writerow(["device","name", "destination", "rules", "pool", "SNAT" , "enabled"])
     for item in response_data_list:
          print(item)
          writer.writerow([item['device'],item['name'], item['disabled'],item['enabled']])
