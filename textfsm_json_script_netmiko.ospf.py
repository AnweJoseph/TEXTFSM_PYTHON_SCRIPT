from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException
import json
import time, schedule

#password = getpass("Enter device password:")

def STATUS():
	with open('device_ips') as DEVICE_IP:
		#password = getpass("Enter device password:")
		for IP in DEVICE_IP:
			
			RTR = {
				'device_type': 'cisco_ios',
				'host': IP,
				'username': 'anwea',
				'password': '02anwe05',
				'secret': '02anwe05'}
			
			print('Checking OSPF status on ' + IP)
			try:
				net_connect = ConnectHandler(**RTR)
				net_connect.enable()
			except NetmikoTimeoutException:
				print('Device not reachable')
				continue
			except NetmikoAuthenticationException:
				print('Authentication Failed')
				continue
			except SSHException:
				print('Error reading SSH protocol banner')
				continue
			except AuthenticationException:
				print('Failed Authentication Exception')
				continue
								
			
			output = net_connect.send_command('sh ip ospf nei', use_textfsm=True)
			#print(json.dumps(output1, indent=2) + '\n\n')

			for ospf in output:
				if ospf['state'] == 'FULL/  -':
					print("OSPF Neighbor with " + f"{ospf['neighbor_id']}" + " is " +\
							f"{ospf['state']}")
					print('\n')
					#print("{} is {}".format(ospf['neighbor_id'], ospf['state']))
					time.sleep(1)
				
			
schedule.every(10).seconds.do(STATUS)

while True:
    schedule.run_pending()
    time.sleep(1)
     

