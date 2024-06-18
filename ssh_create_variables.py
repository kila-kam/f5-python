import re
import csv

#parse pool and snat data 
with open('ltm_output.txt', 'r') as file:
    parsed_pool_list = list()
    parsed_snat_list = list()
    lines = file.readlines()
    for line in lines:
        if 'pool' in line and not 'snat' in line:
            try:
                pool = re.search(r'\s+pool\s+(\S+)',line).group(1)
                parsed_pool_list.append(pool)
            except Exception as e:
                print('cant find pool ')
        if 'pool' in line  and 'snat'  in line:
            try:
                snat = re.search(r'\s+pool\s+(\S+)',line).group(1)
                parsed_snat_list.append(snat)
            except Exception as e:
                print('cant find snatpool')
    parsed_pool_list= set(parsed_pool_list)
    parsed_snat_list= set(parsed_snat_list)

print(parsed_snat_list)
print(parsed_pool_list)

with open('ltm_pool_output.txt', 'r') as file:
    parsed_pool_members = list()
    lines = file.readlines()
    for line in lines:
            try:
                member = re.search(r'\s+(\S+):',line).group(1)
                parsed_pool_members.append(member)
            except Exception as e:
                print('cant find pool member')
    parsed_pool_members =set(parsed_pool_members)

with open('pools.txt','w') as file:
    for pool in parsed_pool_list:
        file.write(pool +'\n')

with open('snats.txt','w') as file:
    for snat in parsed_snat_list:
        file.write(snat +'\n')

with open('nodes.txt','w') as file:
    for node in parsed_pool_members:
        file.write(node +'\n')
