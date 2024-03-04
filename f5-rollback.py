from f5_modules import *

device = '192.168.1.254'

snat_file_handle = open('audit/192.168.1.254/192.168.1.254-snatpool_26Feb2024_10_49.json')
pool_file_handle = open('audit/192.168.1.254/192.168.1.254-pool_26Feb2024_10_48')
virtual_file_handle = open('audit/192.168.1.254/192.168.1.254-snatpool_26Feb2024_10_48.json')

snat_data = json.load(snat_file_handle)
pool_data = json.load(pool_file_handle)
virtual_data = json.load(virtual_file_handle)

snatpools = list(open('target_devices/{}/snatpools.txt'.format(device)))
for snat in snatpools: 
    for item in snat_data['items']:
        if snat == item['name']:
            POST_F5_data(device,'snatpool',item)

pools = list(open('target_devices/{}/pools.txt'.format(device)))
for pool in pools:
    for item in pool_data['items']:
        if snat == item['name']:
            POST_F5_data(device,'pool',item)

virtuals = list(open('target_devices/{}/virtual_servers.txt'.format(device)))
for virtual in virtuals: 
    for item in virtual_data['items']:
        if snat == item['name']:
            POST_F5_data(device,'virtual',item)
