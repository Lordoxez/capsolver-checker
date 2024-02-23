import random
import json
import ctypes
import threading
from time import sleep
import os

try:
    from colorama import Fore, init
    import pyfiglet
    import requests
    from pystyle import Write, Colors
except ModuleNotFoundError:
    os.system("pip install colorama")
    os.system("pip install pyfiglet")
    os.system("pip install requests")
    os.system("pip install pystyle")

print_lock = threading.Lock()
init(convert=True)
generated_keys = set()

generated = 0
valid = 0
errors = 0

result = pyfiglet.figlet_format("CapSolver")
print(Fore.BLUE, end="")
Write.Print(result + "\n", Colors.red_to_purple, interval=0.000)
sleep(1.5)

def generate_key():
    key = 'CAP-' + ''.join(random.choices('ABCDEF0123456789', k=32))
    if key not in generated_keys:
        generated_keys.add(key)
        return key

def check_bal():
    global generated, valid, errors
    ctypes.windll.kernel32.SetConsoleTitleW(f'CapSolver Checker | Generated ~ {generated} | Errors ~ {errors} | Valid ~ {valid} | github.com/Lordoxez')
    while True:
        api_key = generate_key()
        if api_key == None:
            api_key = generate_key()
        else:
            pass
        
        data = {
            "clientKey": api_key,
        }
        headers = {
            'Content-Type': 'application/json'
        }

        api_key = data["clientKey"]
        req = requests.post(
            'https://api.capsolver.com/getBalance',
            data=json.dumps(data), headers=headers).json()
        
        if req.get("balance"):
            bal = req["balance"]
            
            if bal > 0:
                with print_lock:
                    print(f"{Fore.GREEN}{int(bal)}$ | {api_key}")
                    generated += 1
                    valid += 1
                    with open("valid.txt", "a") as f:
                        f.write(api_key + '\n')
            else:
                with print_lock:
                    print(f"{Fore.LIGHTYELLOW_EX}{int(bal)}$ | {api_key}")
                    generated += 1
        else:
            with print_lock:
                error = req.get('errorCode')
                print(f"{Fore.RED}{error} | {api_key}")
                generated += 1
                errors += 1

num = 1000
threads = []

for i in range(int(num)):
    thread = threading.Thread(target=check_bal, name=f"Lord")
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
