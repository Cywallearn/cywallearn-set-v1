"""Cywallearn SET - SMS Sender Module"""

import os
import sys
import subprocess
import requests
import json
from datetime import datetime

class SMSSender:
    def __init__(self):
        self.sent_count = 0
    
    def send_termux(self, number, message):
        """Send SMS via Termux-API (requires termux-api installed)"""
        try:
            result = subprocess.run(
                ["termux-sms-send", "-n", number, message],
                capture_output=True, text=True, timeout=30
            )
            self.sent_count += 1
            return True, f"Sent via Termux-API to {number}"
        except FileNotFoundError:
            return False, "Termux-API not installed. Run: pkg install termux-api"
        except Exception as e:
            return False, str(e)
    
    def send_textbelt(self, number, message):
        """Send SMS via Textbelt API (1 free SMS/day)"""
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': number,
                'message': message,
                'key': 'textbelt'
            }, timeout=15)
            data = resp.json()
            if data.get('success'):
                self.sent_count += 1
                return True, f"Sent via Textbelt to {number}"
            return False, data.get('error', 'Unknown error')
        except Exception as e:
            return False, str(e)
    
    def send_bulk(self, numbers, message, method='termux'):
        """Send to multiple numbers"""
        results = []
        for num in numbers:
            if method == 'termux':
                success, msg = self.send_termux(num, message)
            else:
                success, msg = self.send_textbelt(num, message)
            results.append((num, success, msg))
        return results
    
    def interactive(self):
        """Interactive SMS sending menu"""
        print("\n=== SMS Sender ===")
        print("1. Send via Termux-API (free, requires SMS permission)")
        print("2. Send via Textbelt API (1 free/day)")
        print("3. Bulk send to file list")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            num = input("Phone number (with country code, e.g. +1234567890): ").strip()
            msg = input("Message: ").strip()
            success, result = self.send_termux(num, msg)
            print(f"[{'OK' if success else 'FAIL'}] {result}")
        
        elif choice == '2':
            num = input("Phone number: ").strip()
            msg = input("Message: ").strip()
            success, result = self.send_textbelt(num, msg)
            print(f"[{'OK' if success else 'FAIL'}] {result}")
        
        elif choice == '3':
            filepath = input("File path (one number per line): ").strip()
            msg = input("Message: ").strip()
            try:
                with open(filepath) as f:
                    numbers = [line.strip() for line in f if line.strip()]
                print(f"Sending to {len(numbers)} numbers...")
                results = self.send_bulk(numbers, msg)
                for num, ok, msg in results:
                    print(f"  [{'+' if ok else '-'}] {num}: {msg}")
            except Exception as e:
                print(f"Error: {e}")
        
        input("\nPress Enter to continue...")