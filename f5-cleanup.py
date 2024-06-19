from urllib import request,parse,error
from concurrent.futures import ProcessPoolExecutor, wait
from datetime import datetime
import ssl
import base64
import logging
import time


# Dictionary of F5 devices

f5 = {
    "host": "localhost",
    "username": "xxx",
    "password": "xxx",
}

#List of Devices
device_list = [f5]

# REST API function to delete  F5 resources

def rest_api_f5_delete(device,uri,data):
    logging.basicConfig(filename=f"target_devices/{device['host']}/f5-delete-{device['host']}.log", filemode='w', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    myssl = ssl.create_default_context();
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE

    url = 'https://{}/mgmt/tm/ltm/{}/{}'
    headers = {'Content-type': 'application/json'}

    try:
        req =  request.Request(url.format(device['host'],uri,data),method='DELETE',headers=headers)
        base64string = base64.b64encode(bytes('{}:{}'.format(device['username'], device['password']), 'ascii'))
        req.add_header('Authorization', 'Basic {}'.format(base64string.decode('utf-8')))
        request.urlopen(req,context=myssl)

        message = f"{uri.upper()} {data} was successfully deleted on {device['host']}"
        logger.info(message.replace('\n',' '))

        time.sleep(1)
    except error.HTTPError as e:
        logger.error(e.read())
        pass

# Iterate and delete resources 
def f5_cleanup(device):
    virtuals = list((open(f"target_devices/{device['host']}/parsed_vips.txt")))
    for virtual in virtuals:
        rest_api_f5_delete(device,'virtual', virtual.rstrip())

    pools = list((open(f"target_devices/{device['host']}/pools.txt")))
    for pool in pools:
        rest_api_f5_delete(device,'pool', pool.rstrip().replace('/','~'))

    snatpools = list(open(f"target_devices/{device['host']}/snatpools.txt"))
    for snatpool in snatpools:
        rest_api_f5_delete(device,'snatpool', snatpool.rstrip().replace('/','~'))

    nodes = list(open(f"target_devices/{device['host']}/nodes.txt"))
    for node in nodes:
        rest_api_f5_delete(device,'node', node.rstrip())


# Add concurrency to F5 module 
if __name__ == "__main__":

    start_time = datetime.now()
    max_threads = len(device_list)

    pool = ProcessPoolExecutor(max_threads)

    future_list = []
    for device in device_list:
        future = pool.submit(f5_cleanup, device)
        future_list.append(future)

    # Waits until all the pending threads are done
    wait(future_list)

    for future in future_list:
        print(future.result())

    end_time = datetime.now()
    print(end_time - start_time)
