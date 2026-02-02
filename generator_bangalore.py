import socket
import json
import time
from termcolor import colored
from ai_brain import SolarBrain

CLOUD_IP = '127.0.0.1'
CLOUD_PORT = 7000
USER = "user_satoshi"

brain = SolarBrain()
simulated_hour = 6 # Start simulation at 6 AM

print(colored("☀️  Bangalore SOLAR ARRAY: ONLINE", "yellow", attrs=['bold']))

while True:
    # 1. Ask AI for prediction
    energy = brain.predict_generation(simulated_hour)
    
    # 2. Upload to Cloud if we have sun
    if energy > 0:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((CLOUD_IP, CLOUD_PORT))
                payload = json.dumps({"type": "MINT", "user": USER, "amount": energy})
                s.sendall(payload.encode())
                print(f"   Time {simulated_hour}:00 -> Generated {energy} Wh -> BEAMED TO CLOUD ☁️")
        except:
            print("   ⚠️ Cloud Offline")
    else:
        print(f"   Time {simulated_hour}:00 -> Night Time (0 Wh)")

    # 3. Fast Forward Time (1 loop = 1 hour)
    simulated_hour += 1
    if simulated_hour > 24: simulated_hour = 0
    time.sleep(2)