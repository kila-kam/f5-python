import json
import csv
import re

devices = list(open('devicesf5.txt'))
for device in devices:

    pool_names = list()
    snat_names = list()
    node_names = list()

    device = device.rstrip()

    #Open json file to extract pool and snat pool data 
    json_file = open('audit/{}/{}-virtual.json'.format(device,device))
    json_data = json.load(json_file)
    
    #List vip names 
    virtuals = list(open('target_devices/{}/vips.txt'.format(device)))

    #Parse pool data
    for i in json_data['items']:
        for virtual in virtuals:
            virtual = virtual.replace('\n','')
            if i['name'] == virtual and i['disabled'] == True:
                try:
                    pool_name =i['pool']
                    pool_names.append(pool_name)
                except KeyError:
                    pass

    pool_names = list(set(pool_names))

    #Parse snat data 
    for i in json_data['items']:
        for virtual in virtuals:
            virtual = virtual.replace('\n','')
            if i['name'] == virtual and i['disabled'] == True:
                try:
                    snat_name = i['sourceAddressTranslation']['pool']
                    snat_names.append(snat_name)
                except KeyError:
                    pass

    snat_names = list(set(snat_names))

    #Open json file to extract node data
    pool_json_file = open('audit/{}/{}-pool.json'.format(device,device))
    pool_json_data = json.load(pool_json_file)
    pool_data_list = list()

 #Pool Data
    for i in pool_json_data['items']:
        for pool in pool_names:
            pool = pool.rstrip()
            if i['fullPath'] == pool:
                print(pool)
                pool_data_list.append(i['membersReference']['items'])

    for i in pool_data_list:
        for j in i:
            node_name = j['name'].split(':')[0]
            print(node_name)
            node_names.append(node_name)
            #yo = re.search(r"~Common~(.*)/members/~Common~",j['selfLink']).group(1)
            #print(yo)

    
    node_names = list(set(node_names))

    #Save data in target device directory 
    with open('target_devices/{}/pools.txt'.format(device),'w') as file:
         for pool in pool_names:
             file.write('{}\n'.format(pool))

    with open('target_devices/{}/snatpools.txt'.format(device),'w') as file:
         for snat in snat_names:
             file.write('{}\n'.format(snat))

    with open('target_devices/{}/nodes.txt'.format(device),'w') as file:
         for node in node_names:
             file.write('{}\n'.format(node))
