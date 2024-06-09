import json
import csv
import re

devices = list(open('devicesf5.txt'))
for device in devices:
    vip_names = list()
    pool_names = list()
    snat_names = list()
    node_names = list()

    device = device.rstrip()

    #Open json file to extract pool and snat pool data 
    json_file = open('audit/{}/{}-virtual.json'.format(device,device))
    json_data = json.load(json_file)
    
    #List vip names 
    virtuals = list(open('target_devices/{}/vips.txt'.format(device)))

    for i in json_data['items']:
        for virtual in virtuals:
            virtual = virtual.replace('\n','')
            try:
                if i['name'] == virtual and i['disabled'] == True:
                    vip_name = i['name']
                    vip_names.append(vip_name)
            except KeyError:
                pass

    vip_names = list(set(vip_names))

    with open('target_devices/{}/parsed_vips.txt'.format(device),'w') as file:
         for vip in vip_names:
             file.write('{}\n'.format(vip))

    # new parsed VIPs to be used to extract pools,snats and node information 
    parsed_virtuals = list(open('target_devices/{}/parsed_vips.txt'.format(device)))

    #Parse Pool Data
    for i in json_data['items']:
        for virtual in parsed_virtuals:
            virtual = virtual.replace('\n','')
            if i['name'] == virtual and i['disabled'] == True:
                try:
                    pool_name =i['pool']
                    pool_names.append(pool_name)
                except KeyError:
                    pass

    pool_names = list(set(pool_names))

    with open('target_devices/{}/pools.txt'.format(device),'w') as file:
         for pool in pool_names:
             file.write('{}\n'.format(pool))

    #Parse Snat Data 
    for i in json_data['items']:
        for virtual in parsed_virtuals:
            virtual = virtual.replace('\n','')
            if i['name'] == virtual and i['disabled'] == True:
                try:
                    snat_name = i['sourceAddressTranslation']['pool']
                    snat_names.append(snat_name)
                except KeyError:
                    pass

    snat_names = list(set(snat_names))

    with open('target_devices/{}/snatpools.txt'.format(device),'w') as file:
         for snat in snat_names:
             file.write('{}\n'.format(snat))

    #Open json file to extract node data
    pool_json_file = open('audit/{}/{}-pool.json'.format(device,device))
    pool_json_data = json.load(pool_json_file)
    pool_data_list = list()

    for i in pool_json_data['items']:
        for pool in pool_names:
            pool = pool.rstrip()
            if i['fullPath'] == pool:
                pool_data_list.append(i['membersReference']['items'])

    for i in pool_data_list:
        for j in i:
            node_name = j['name'].split(':')[0]
            node_names.append(node_name)

    node_names = list(set(node_names))

    #Save data in target device directory 

    with open('target_devices/{}/nodes.txt'.format(device),'w') as file:
         for node in node_names:
             file.write('{}\n'.format(node))
