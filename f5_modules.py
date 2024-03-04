from urllib import request,parse,error
import ssl
import base64
import json
import csv
import getpass
import logging

def POST_F5_data(device,uri,data):
    logging.basicConfig(filename='f5-post.log', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    json_formatted_string = json.dumps(data,indent=2)
    print(json_formatted_string)
    data = json_formatted_string.encode()

    myssl = ssl.create_default_context();
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE

    url = 'https://{}/mgmt/tm/ltm/{}/'
    headers = {
    'Content-type': 'application/json',
    }
    try:
        req =  request.Request(url.format(device,uri),data=data,method='POST',headers=headers)
        base64string = base64.b64encode(bytes('{}:{}'.format(username, password), 'ascii'))
        req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))
        response = request.urlopen(req,context=myssl)
        response_body = response.read().decode()
        print(response_body)
    except error.HTTPError as e:
        logger.error(e.read())
        pass

def DELETE_F5_data(device,uri,data):
    logging.basicConfig(filename='f5-delete.log', filemode='w', level=logging.DEBUG)
    logger = logging.getLogger(__name__)    
    myssl = ssl.create_default_context();
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE

    url = 'https://{}/mgmt/tm/ltm/{}/{}'
    headers = {
    'Content-type': 'application/json',
    }
    try:
        req =  request.Request(url.format(device,uri,data),method='DELETE',headers=headers)
        base64string = base64.b64encode(bytes('{}:{}'.format(username, password), 'ascii'))
        req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))
        response = request.urlopen(req,context=myssl)
        message = f'{uri.upper()} {data} was successfully deleted on {device}'
        logger.info(message.replace('\n',' '))
    except error.HTTPError as e:
        logger.error(e.read())
        pass
