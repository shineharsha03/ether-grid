import socket
import threading
import json
from termcolor import colored

HOST = '127.0.0.1'
PORT = 7000

# The Global Ledger
accounts = {"user_satoshi": 0.0}

print(colored("☁️  ETHER-GRID: GLOBAL LEDGER ONLINE", "cyan", attrs=['bold']))

def handle_client(conn, addr):
    global accounts
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
                
                packet = json.loads(data.decode())
                user = packet.get('user')
                
                # --- CASE 1: MINTING (From Delhi) ---
                if packet['type'] == 'MINT':
                    amount = packet['amount']
                    accounts[user] += amount
                    print(f"   🇮🇳  DELHI UPLOAD: +{amount} Wh | Balance: {accounts[user]:.2f} Wh")
                    conn.sendall(json.dumps({"status": "minted", "new_balance": accounts[user]}).encode())

                # --- CASE 2: BURNING (From London) ---
                elif packet['type'] == 'BURN':
                    needed = packet['amount']
                    if accounts[user] >= needed:
                        accounts[user] -= needed
                        print(f"   🇬🇧  LONDON CHARGE: -{needed} Wh | APPROVED ✅")
                        conn.sendall(json.dumps({"status": "approved", "remaining": accounts[user]}).encode())
                    else:
                        print(f"   🇬🇧  LONDON CHARGE: -{needed} Wh | DENIED ❌")
                        conn.sendall(json.dumps({"status": "denied"}).encode())
            except Exception as e:
                break

# START SERVER
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()