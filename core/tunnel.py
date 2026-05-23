"""Cywallearn SET - Tunnel Manager (Serveo/Cloudflare)"""

import os
import subprocess
import threading
import time

class TunnelManager:
    def __init__(self):
        self.process = None
        self.url = None
        self.type = None
    
    def start_serveo(self, local_port=5000, subdomain=""):
        """Start Serveo tunnel (free, only SSH required)"""
        if not subdomain:
            subdomain = f"cywallearn{int(time.time())%10000}"
        
        cmd = f"ssh -o StrictHostKeyChecking=no -R {subdomain}:80:localhost:{local_port} serveo.net"
        
        print(f"[+] Starting Serveo tunnel: {subdomain}.serveo.net -> localhost:{local_port}")
        
        self.process = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.url = f"https://{subdomain}.serveo.net"
        self.type = "serveo"
        
        # Read output to confirm
        try:
            line = self.process.stdout.readline().decode()
            if "forwarding" in line.lower():
                print(f"[✓] Tunnel active: {self.url}")
        except:
            pass
        
        return self.url
    
    def start_localhost_run(self, local_port=5000):
        """Use localhost.run (alternative to serveo)"""
        cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{local_port} nokey@localhost.run"
        
        print(f"[+] Starting localhost.run tunnel...")
        self.process = subprocess.Popen(
            cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.type = "localhostrun"
        
        # Read output for URL
        try:
            output = self.process.stdout.readline().decode()
            if "https://" in output:
                self.url = output.split("https://")[1].split()[0]
                self.url = f"https://{self.url}"
                print(f"[✓] Tunnel active: {self.url}")
        except:
            pass
        
        return self.url
    
    def stop(self):
        """Kill tunnel"""
        if self.process:
            self.process.kill()
            self.url = None
            self.type = None
            print("[+] Tunnel stopped")
    
    def interactive(self):
        print("\n=== Tunnel Manager ===")
        print(f"Current: {self.url or 'None'}")
        print("1. Start Serveo tunnel")
        print("2. Start localhost.run tunnel")
        print("3. Stop tunnel")
        
        choice = input("\nChoice: ").strip()
        port = input("Local port (default 5000): ").strip() or "5000"
        
        if choice == '1':
            sub = input("Subdomain (optional): ").strip()
            self.start_serveo(int(port), sub)
        elif choice == '2':
            self.start_localhost_run(int(port))
        elif choice == '3':
            self.stop()