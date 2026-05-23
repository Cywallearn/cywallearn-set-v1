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
        except Exception as e:
            # Log the error silently, fallback to localhost
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
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", *missing],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print(f"{G}[+] Installed successfully{N}")
                    else:
                        print(f"{R}[!] Installation failed:{N}")
                        print(result.stderr)
                except FileNotFoundError:
                    print(f"{R}[!] pip not found. Install Python pip first.{N}")
                except Exception as e:
                    print(f"{R}[!] Unexpected error during install: {e}{N}")
        else:
            print(f"{G}[✓] All dependencies satisfied{N}")

        input(f"\n{Y}[Press Enter to continue]{N}")

    def _safe_import_module(self, module_path, class_name):
        """
        Safely import a module and return the class.
        Returns (class, None) on success, (None, error_msg) on failure.
        """
        try:
            spec = importlib.util.spec_from_file_location(
                module_path.replace('/', '.').replace('\\', '.'),
                os.path.join(BASE_DIR, module_path + '.py')
            )
            if spec is None:
                return None, f"Module file not found: {module_path}.py"
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            cls = getattr(module, class_name, None)
            if cls is None:
                return None, f"Class '{class_name}' not found in {module_path}.py"
            return cls, None
        except Exception as e:
            return None, f"Import error: {e}"

    def main_menu(self):
        while self.running:
            self.print_banner()

            local_ip = self.get_ip()
            tunnel_status = f"{G}Active ✓{N}" if self.tunnel_active else f"{R}Inactive ✗{N}"

            print(f"\n  {C}Local IP:{N} {local_ip}")
            print(f"  {C}Date:{N} {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  {C}Tunnel:{N} {tunnel_status}")
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

            try:
                choice = input(f"\n{BOLD}{G}cywallearn>{N} ").strip()
            except (KeyboardInterrupt, EOFError):
                self.exit_tool()
                return

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
            else:
                print(f"{R}[!] Invalid choice. Press Enter to continue.{N}")
                input()

    # ─── WEB PHISHING MODULE ───────────────────────────────
    def module_web_phishing(self):
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
            ("11", "Quiz -> Login", "Quiz funnel redirecting to login"),
            ("12", "Captcha Verifier", "Fake captcha that grabs credentials"),
            ("13", "Custom Page", "Create your own HTML page"),
            ("14", "Multi-Phish", "Rotate through multiple pages"),
            ("B", "Back to Main Menu"),
        ]

        for num, name, desc in templates:
            self.print_menu_item(num, name, desc)

        self.print_menu_footer()

        try:
            choice = input(f"\n{BOLD}{G}web_phish>{N} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return

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
        if not template:
            print(f"{R}[!] Invalid selection.{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")
            return

        # Safe import
        PhishingServer, err = self._safe_import_module(
            'modules/web_phishing/server', 'PhishingServer'
        )
        if err:
            print(f"{R}[!] Could not load web phishing module: {err}{N}")
            print(f"{Y}[*] Ensure 'modules/web_phishing/server.py' exists.{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")
            return

        try:
            server = PhishingServer(template)
            server.run()
        except Exception as e:
            print(f"{R}[!] Error running phishing server: {e}{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")

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

        try:
            choice = input(f"\n{BOLD}{G}sms_tools>{N} ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return

        if choice == 'b':
            return

        # Map choices to (module_path, class_name, method_name)
        action_map = {
            '1': ('modules/sms_tools/sms_sender', 'SMSSender', '_sms_single'),
            '2': ('modules/sms_tools/sms_spoofer', 'SMSSpoofer', '_sms_spoof'),
            '3': ('modules/sms_tools/sms_campaign', 'SMSCampaign', '_sms_campaign'),
            '4': ('modules/sms_tools/sms_templates', 'SMSTemplates', '_sms_templates'),
            '5': ('modules/sms_tools/sms_bomber', 'SMSBomber', '_sms_bomber'),
        }

        if choice not in action_map:
            print(f"{R}[!] Invalid selection.{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")
            return

        module_path, class_name, method_name = action_map[choice]
        Cls, err = self._safe_import_module(module_path, class_name)
        if err:
            print(f"{R}[!] Could not load SMS module: {err}{N}")
            print(f"{Y}[*] Ensure '{module_path}.py' exists.{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")
            return

        try:
            instance = Cls()
            getattr(self, method_name)(instance)
        except Exception as e:
            print(f"{R}[!] Error in SMS module: {e}{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")

    def _sms_single(self, sender_instance=None):
        """Send a single SMS"""
        print(f"\n{C}[*] SMS Sender - Single Message{N}")
        number = input(f"{Y}[?] Target number (with country code): {N}").strip()
        message = input(f"{Y}[?] Message (authorized testing only): {N}").strip()

        if not number or not message:
            print(f"{R}[!] Number and message cannot be empty.{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")
            return

        if sender_instance:
            try:
                sender_instance.send(number, message)
                print(f"{G}[+] SMS sent to {number}{N}")
            except Exception as e:
                print(f"{R}[!] Failed to send SMS: {e}{N}")
            input(f"\n{Y}[Press Enter to continue]{N}")

    def _sms_spoof(self, spoofer_instance=None):
        """Placeholder for SMS spoofing"""
        print(f"\n{Y}[*] SMS Spoofing - Not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def _sms_campaign(self, campaign_instance=None):
        """Placeholder for SMS campaign"""
        print(f"\n{Y}[*] Mass SMS Campaign - Not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def _sms_templates(self, templates_instance=None):
        """Placeholder for SMS templates"""
        print(f"\n{Y}[*] SMS Template Library - Not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def _sms_bomber(self, bomber_instance=None):
        """Placeholder for SMS bomber"""
        print(f"\n{Y}[*] SMS Bomber")
def _sms_bomber(self, bomber_instance=None):
        """Placeholder for SMS bomber"""
        print(f"\n{Y}[*] SMS Bomber (Demo) - Not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    # ─── STUB MODULES (Email, Cred Harvesting, Recon, Payloads, Dashboard, Tunnel) ──
    def module_email_tools(self):
        print(f"\n{Y}[*] Email Engineering Tools - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def module_credential_harvesting(self):
        print(f"\n{Y}[*] Credential Harvesting - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def module_recon(self):
        print(f"\n{Y}[*] Reconnaissance Tools - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def module_payloads(self):
        print(f"\n{Y}[*] Payload Generation - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def module_dashboard(self):
        print(f"\n{Y}[*] Live Dashboard - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def module_tunnel(self):
        print(f"\n{Y}[*] Tunnel Manager - Module not yet implemented{N}")
        input(f"\n{Y}[Press Enter to continue]{N}")

    def exit_tool(self):
        print(f"\n{Y}[*] Shutting down Cywallearn SET...{N}")
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
        self.running = False
        print(f"{G}[+] Goodbye.{N}")
        sys.exit(0)


# ─── ENTRY POINT ─────────────────────────────────────────────
if __name__ == "__main__":
    app = CywallearnSET()
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Y}[!] Interrupted. Exiting...{N}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{R}[!] Unexpected error: {e}{N}")
        sys.exit(1)
