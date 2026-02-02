import socket
import json
import time
from termcolor import colored

CLOUD_IP = '127.0.0.1'
CLOUD_PORT = 7000
USER = "user_satoshi"

print(colored("🌧️  LONDON CHARGING STATION", "blue", attrs=['bold']))

while True:
    input("\nPRESS ENTER TO CHARGE DEVICE...") 
    
    power_needed = 25.0 # We need 25 Wh to charge
    
    print(f"   🔌 Authenticating Global Account...")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CLOUD_IP, CLOUD_PORT))
            
            payload = json.dumps({"type": "BURN", "user": USER, "amount": power_needed})
            s.sendall(payload.encode())
            
            data = s.recv(1024)
            response = json.loads(data.decode())
            
            if response['status'] == 'approved':
                print(colored("   ✅ ACCESS GRANTED. WIRELESS POWER ACTIVE.", "green", attrs=['bold']))
                print(f"      Remaining Balance: {response['remaining']:.2f} Wh")
            else:
                print(colored("   ❌ ACCESS DENIED. INSUFFICIENT FUNDS.", "red"))
                print("      (Wait for the sun to rise in Delhi)")
    except:
        print("   ⚠️ Network Error")