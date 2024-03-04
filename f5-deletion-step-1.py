from urllib import request,parse,error
import ssl
import base64
import json
import getpass
import logging
import time
from f5_modules import *

username= input("Username: ")
password= getpass.getpass()

headers = {
    'Content-type': 'application/json',
}

devices = list(open('devicesf5.txt'))

myssl = ssl.create_default_context();
myssl.check_hostname=False
myssl.verify_mode=ssl.CERT_NONE

if __name__ == "__main__":
    url = 'https://{}/mgmt/tm/ltm/{}/{}' # Set destination URL heres
    for device in devices:
        virtuals = list((open('target_devices/{}/virtual_servers.txt'.format(device))))
        virtual_addresses = list((open('target_devices/{}/virtual_addresses.txt'.format(device))))
        pools = list((open('target_devices/{}/pools.txt'.format(device))))
        snatpools = list((open('target_devices/{}/snatpools.txt'.format(device))))
        nodes = list((open('target_devices/{}/nodes.txt'.format(device))))
        print('deleting virtual serverss')
        for virtual in virtuals:
            DELETE_F5_data(device,'virtual', virtual)
            time.sleep(2)
        print('deleting vip addresses')
        for virtual_address in virtual_addresses:
            DELETE_F5_data(device,'virtual-address', virtual_address)
            time.sleep(2)
        print('deleting pools')
        for pool in pools:
            DELETE_F5_data(device,'pool', pool)
            time.sleep(2)
        print('deleting snatpools')
        for snatpool in snatpools:
            DELETE_F5_data(device,'snatpool', snatpool)
            time.sleep(2)
