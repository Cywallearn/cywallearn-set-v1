#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║              CYWALLEARN SET v1                                ║
║         Social Engineering Toolkit for Termux                 ║
║         FOR AUTHORIZED PENETRATION TESTING ONLY               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import datetime
import socket
import subprocess
import importlib.util

# Ensure we're in the right directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'
BOLD = '\033[1m'

VERSION = "1.0.0"
AUTHOR = "Cywallearn"

class CywallearnSET:
    def __init__(self):
        self.running = True
        self.selected_module = None
        self.tunnel_active = False
        self.tunnel_url = None
        self.server_process = None
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        self.clear_screen()
        banner = f"""
{R}╔═══════════════════════════════════════════════════════╗
║                                                       ║
║  {C}██████╗██╗   ██╗██╗    ██╗ █████╗ ██╗     ██╗     {R}║
║  {C}██╔════╝╚██╗ ██╔╝██║    ██║██╔══██╗██║     ██║     {R}║
║  {C}██║      ╚████╔╝ ██║ █╗ ██║███████║██║     ██║     {R}║
║  {C}██║       ╚██╔╝  ██║███╗██║██╔══██║██║     ██║     {R}║
║  {C}╚██████╗   ██║   ╚███╔███╔╝██║  ██║███████╗███████╗{R}║
║  {C} ╚═════╝   ╚═╝    ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚══════╝{R}║
║                                                       ║
║  {W}███████╗███████╗████████╗                         {R}║
║  {W}██╔════╝██╔════╝╚══██╔══╝                         {R}║
║  {W}█████╗  █████╗     ██║                            {R}║
║  {W}██╔══╝  ██╔══╝     ██║                            {R}║
║  {W}███████╗███████╗   ██║                            {R}║
║  {W}╚══════╝╚══════╝   ╚═╝                            {R}║
║                                                       ║
║  {G}Social Engineering Toolkit v{VERSION}{R}                    ║
║  {Y}FOR AUTHORIZED TESTING ONLY{R}                           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝{N}
"""
        print(banner)
    
    def print_menu_header(self, title):
        w = 58
        print(f"\n{BOLD}{C}┌─{'─'*w}─┐{N}")
        print(f"{BOLD}{C}│{N} {Y}{title.center(w)}{N} {C}│{N}")
        print(f"{BOLD}{C}├─{'─'*w}─┤{N}")

    def print_menu_item(self, num, name, desc, status="ready"):
        status_color = G if status == "ready" else Y
        print(f"{C}│{N} {G}{num:>2}.{N} {BOLD}{name}{N}")
        print(f"{C}│{N}    {W}{desc}{N}  [{status_color}{status}{N}]")
    
    def print_menu_footer(self):
        w = 58
        print(f"{BOLD}{C}└─{'─'*w}─┘{N}")
    
    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def check_dependencies(self):
        """Check all required packages are installed"""
        self.print_menu_header("DEPENDENCY CHECK")
        deps = {
            'flask': 'flask',
            'requests': 'requests',
            'PIL': 'pillow',
            'qrcode': 'qrcode',
            'cryptography': 'cryptography',
            'beautifulsoup4': 'beautifulsoup4',
        }
        
        missing = []
        for mod, pkg in deps.items():
            spec = importlib.util.find_spec(mod.replace('-', '_').replace('.', '_'))
            if spec is None:
                missing.append(pkg)
        
        if missing:
            print(f"{Y}[!] Missing packages: {', '.join(missing)}{N}")
            install = input(f"{Y}[?] Install now? (Y/n): {N}").lower()
            if install != 'n':
                subprocess.run([sys.executable, "-m", "pip", "install", *missing])
                print(f"{G}[+] Installed successfully{N}")
        else:
            print(f"{G}[✓] All dependencies satisfied{N}")
        
        input(f"\n{Y}[Press Enter to continue]{N}")
    
    def main_menu(self):
        while self.running:
            self.print_banner()
            
            local_ip = self.get_ip()
            print(f"\n  {C}Local IP:{N} {local_ip}")
            print(f"  {C}Date:{N} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  {C}Tunnel:{N} {G}Active ✓{N if self.tunnel_active else R'Inactive ✗'}{N}")
            if self.tunnel_url:
                print(f"  {C}Public URL:{N} {Y}{self.tunnel_url}{N}")
            
            self.print_menu_header("MAIN MENU")
            
            modules = [
                ("1", "Web Phishing Engine", "Clone & deploy 12+ social media login pages"),
                ("2", "SMS Engineering Tools", "Send, spoof, and mass-SMS campaigns"),
                ("3", "Email Engineering Tools", "Send, spoof, and mass-email campaigns"),
                ("4", "Credential Harvesting", "Keyloggers, form grabbers, OTP bypass"),
                ("5", "Reconnaissance Tools", "OSINT, IP tracking, device fingerprinting"),
                ("6", "Payload Generation", "QR codes, short links, fake updates"),
                ("7", "Live Dashboard", "Monitor captures in real-time"),
                ("8", "Tunnel Manager", "Setup Serveo/ngrok/Cloudflare tunnels"),
                ("9", "Dependency Check", "Verify and install required packages"),
                ("0", "Exit", "Quit Cywallearn SET"),
            ]
            
            for num, name, desc in modules:
                self.print_menu_item(num, name, desc)
            
            self.print_menu_footer()
            
            choice = input(f"\n{BOLD}{G}cywallearn>{N} ").strip()
            
            if choice == '0':
                self.exit_tool()
            elif choice == '1':
                self.module_web_phishing()
            elif choice == '2':
                self.module_sms_tools()
            elif choice == '3':
                self.module_email_tools()
            elif choice == '4':
                self.module_credential_harvesting()
            elif choice == '5':
                self.module_recon()
            elif choice == '6':
                self.module_payloads()
            elif choice == '7':
                self.module_dashboard()
            elif choice == '8':
                self.module_tunnel()
            elif choice == '9':
                self.check_dependencies()
    
    # ─── WEB PHISHING MODULE ───────────────────────────────
    def module_web_phishing(self):
        from modules.web_phishing.server import PhishingServer
        
        self.print_banner()
        self.print_menu_header("WEB PHISHING ENGINE")
        
        templates = [
            ("1", "Instagram", "Instagram login page"),
            ("2", "Facebook", "Facebook login page"),
            ("3", "Google/Gmail", "Google account login"),
            ("4", "Twitter/X", "Twitter/X login page"),
            ("5", "LinkedIn", "LinkedIn login page"),
            ("6", "TikTok", "TikTok login page"),
            ("7", "Snapchat", "Snapchat login page"),
            ("8", "Netflix", "Netflix login page"),
            ("9", "Amazon", "Amazon login page"),
            ("10", "PayPal", "PayPal login page"),
            ("11", "Quiz->Login", "Quiz funnel redirecting to login"),
            ("12", "Captcha Verifier", "Fake captcha that grabs credentials"),
            ("13", "Custom Page", "Create your own HTML page"),
            ("14", "Multi-Phish", "Rotate through multiple pages"),
            ("B", "Back to Main Menu"),
        ]
        
        for num, name, desc in templates:
            self.print_menu_item(num, name, desc)
        
        self.print_menu_footer()
        
        choice = input(f"\n{BOLD}{G}web_phish>{N} ").strip().lower()
        
        if choice == 'b':
            return
        
        template_map = {
            '1': 'instagram', '2': 'facebook', '3': 'google',
            '4': 'twitter', '5': 'linkedin', '6': 'tiktok',
            '7': 'snapchat', '8': 'netflix', '9': 'amazon',
            '10': 'paypal', '11': 'quiz', '12': 'captcha',
            '13': 'custom', '14': 'multi'
        }
        
        template = template_map.get(choice)
        if template:
            server = PhishingServer(template)
            server.run()
    
    # ─── SMS MODULE ────────────────────────────────────────
    def module_sms_tools(self):
        self.print_banner()
        self.print_menu_header("SMS ENGINEERING TOOLS")
        
        options = [
            ("1", "Send Single SMS", "Send SMS via Termux-API"),
            ("2", "SMS Spoofing", "Send SMS with spoofed sender ID"),
            ("3", "Mass SMS Campaign", "Send to multiple numbers"),
            ("4", "SMS Template Library", "Pre-written social engineering SMS"),
            ("5", "SMS Bomber (Demo)", "Stress test with multiple messages"),
            ("B", "Back to Main Menu"),
        ]
        
        for num, name, desc in options:
            self.print_menu_item(num, name, desc)
        
        self.print_menu_footer()
        
        choice = input(f"\n{BOLD}{G}sms_tools>{N} ").strip().lower()
        
        if choice == 'b':
            return
        elif choice == '1':
            self._sms_single()
        elif choice == '2':
            self._sms_spoof()
        elif choice == '3':
            self._sms_campaign()
        elif choice == '4':
            self._sms_templates()
        elif choice == '5':
            self._sms_bomber()
    
    def _sms_single(self):
        from modules.sms_tools.sms_sender import SMSSender
        
        print(f"\n{C}[*] SMS Sender - Single Message{N}")
        number = input(f"{Y}[?] Target number (with country code): {N}").strip()
        message = input(f"{Y}[?] Message: {N}