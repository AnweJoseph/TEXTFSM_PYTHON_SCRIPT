from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from paramiko.ssh_exception import SSHException
from paramiko.ssh_exception import AuthenticationException
import json
import time

#password = getpass("Enter device password:")

with open('device_ips') as DEVICE_IP:
	password = getpass("Enter device password:")
	for IP in DEVICE_IP:
		
		RTR = {
			'device_type': 'cisco_ios',
			'host': IP,
			'username': 'anwea',
			'password': '02anwe05',
			'secret': password}
		
		print('######Connecting to the device ' + IP)
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
		output = net_connect.send_config_from_file(config_file = 'config_command')
				
		print('\nsaving the configuration##########\n')
		output = net_connect.save_config()

		output = net_connect.send_command('sh ip int brief', use_textfsm=True)
		print(json.dumps(output, indent=2) + '\n\n')

		status = (output[4]['status'])
		interface = (output[4]['intf'])
		if  status == 'up':
			print('Finishing the configuration...\n')
			print(interface + ' is UP')
			
		else: 			
			new_state = net_connect.send_config_from_file(config_file = 'interface_status')
			time.sleep(15)
			print(new_state)
			print('Backup interface {state} is now Up and active'.format(state = output[10]['intf']))

