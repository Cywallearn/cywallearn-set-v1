"""Cywallearn SET - SMS Spoofing Module"""

import os
import subprocess
import requests

class SMSSpoofer:
    """Demonstrates SMS sender ID spoofing techniques"""
    
    def send_with_spoofed_id(self, number, message, sender_id):
        """
        Send SMS with custom sender ID.
        Limitations: Works only in some countries; uses SMS gateway APIs.
        """
        print(f"\n[*] Attempting to send SMS with spoofed sender ID: {sender_id}")
        print(f"[*] To: {number}")
        print(f"[*] Message: {message[:50]}...")
        
        # Method 1: Termux with SIM-based (uses actual SIM, no spoofing possible)
        print("\n[!] Note: True SMS spoofing requires SMS gateway services")
        print("[!] This demo shows the concept only")
        
        print("\nMethod available:")
        print("1. Use online SMS gateway (requires API key)")
        print("2. Save to file for manual dispatch")
        
        choice = input("\nChoice: ").strip()
        
        if choice == '1':
            api_key = input("Enter your SMS gateway API key: ").strip()
            gateway = input("Gateway URL (default: https://api.example.com/sms): ").strip()
            if not gateway:
                gateway = "https://api.example.com/sms"
            
            payload = {
                'api_key': api_key,
                'to': number,
                'from': sender_id,
                'message': message
            }
            print(f"[*] Would send: POST {gateway}")
            print(f"[*] Payload: from={sender_id}, to={number}")
            print("[✓] Spoofed SMS concept demonstrated")
        
        elif choice == '2':
            output_file = "data/logs/spoofed_sms_queue.txt"
            os.makedirs("data/logs", exist_ok=True)
            with open(output_file, "a") as f:
                f.write(f"[{sender_id}] -> {number}: {message}\n")
            print(f"[+] Queued to {output_file}")