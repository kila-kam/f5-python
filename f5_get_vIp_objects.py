import paramiko
from paramiko.ssh_exception import SSHException, BadHostKeyException, AuthenticationException
import socket
import time
import re
import csv

device = 'localhost'
username = 'username'
password = 'password'
max_buffer= 65535

with open('target_devices/{}/commands.txt'.format(device)) as file:
    commands =list(file)

remote_pre_conn = paramiko.SSHClient()
remote_pre_conn.set_missing_host_key_policy(
         paramiko.AutoAddPolicy()
    )
try:
    remote_pre_conn.connect(device,
    username=username,
    password=password,
    look_for_keys=False,
    allow_agent=False
    )
    remote_conn = remote_pre_conn.invoke_shell()
    output_list=[]
    for command in commands:
        command = f"list ltm virtual {command}"
        remote_conn.send(f"{command}\n")
        time.sleep(2)
        output = remote_conn.recv(max_buffer).decode().strip()
        output_list.append(output)
    remote_conn.close()
    remote_pre_conn.close()
except AuthenticationException:
    print(" text")
except SSHException as sshException:
    print('text')
except BadHostKeyException as badHostKeyException:
    print('text')
except socket.error as exc:
    print ('text')

output_list_dict=[]
for output in output_list:
    output_dict={}
    output_dict['name'] = re.search(r'\r\nltm virtual\s(\S+)',output).group(1)
    try:
        output_dict['pool'] = re.search(r'\r\n\s\s\s\spool\s(\S+)', output).group(1)
    except:
        print("no pool assigned")
    try:
         output_dict['snat'] = re.search(r'\r\n\s\s\s\s\s\s\s\spool\s(\S+)',output).group(1)
    except:
         print("no snat assigned")
    output_list_dict.append(output_dict)
print(output_list_dict)

#with  open('paramiko-vip-status.csv','w') as file:
#    csv_file=csv.writer(file)
#    csv_file.writerow(['name','availability','status'])
#    for item in output_list_dict:
#        try:
#            csv_file.writerow([item['name'], item['availability'],item['state']])
#        except KeyError:
#            print('hmm')

#with open('output.txt','w') as command_output:
#    for output in output_list:
#        command_output.write(output +'\n')


#parse pool and snat data 

