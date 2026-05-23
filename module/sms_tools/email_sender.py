"""Cywallearn SET - Email Sender Module"""

import os
import sys
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.config import Config

class EmailSender:
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email = Config.load('smtp_user', '')
        self.password = Config.load('smtp_pass', '')
    
    def configure(self):
        """Set up email credentials"""
        print("\n=== Email Configuration ===")
        self.email = input("Gmail address: ").strip()
        self.password = input("Gmail App Password (16 chars): ").strip()
        
        Config.save('smtp_user', self.email)
        Config.save('smtp_pass', self.password)
        print("[+] Credentials saved")
    
    def send_email(self, to_email, subject, body_html, body_text=""):
        """Send HTML email via SMTP"""
        if not self.email or not self.password:
            print("[!] Email not configured. Run configure first.")
            return False
        
        msg = MIMEMultipart('alternative')
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        if body_text:
            msg.attach(MIMEText(body_text, 'plain'))
        msg.attach(MIMEText(body_html, 'html'))
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(self.email, self.password)
                server.sendmail(self.email, [to_email], msg.as_string())
            
            print(f"[+] Email sent to {to_email}")
            return True
        
        except smtplib.SMTPAuthenticationError:
            print("[!] Authentication failed. Use App Password (not regular password)")
            print("[!] Get it at: https://myaccount.google.com/apppasswords")
            return False
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def send_spoofed(self, to_email, from_name, from_email, subject, body_html):
        """Send email with spoofed sender (from field only, not true SPF bypass)"""
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body_html, 'html'))
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(self.email, self.password)
                server.sendmail(self.email, [to_email], msg.as_string())
            
            print(f"[+] Spoofed email sent: {from_name} <{from_email}> -> {to_email}")
            return True
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    def send_campaign(self, recipients, subject, body_html):
        """Mass email campaign"""
        success = 0
        fail = 0
        for i, to_email in enumerate(recipients):
            print(f"[*] ({i+1}/{len(recipients)}) Sending to {to_email}...")
            if self.send_email(to_email, subject, body_html):
                success += 1
            else:
                fail += 1
        
        print(f"\n[+] Campaign complete: {success} sent, {fail} failed")
        return success, fail
    
    def interactive(self):
        """Interactive email menu"""
        while True:
            print("\n=== Email Sender ===")
            print("1. Configure Gmail credentials")
            print("2. Send single email")
            print("3. Send spoofed email")
            print("4. Mass campaign from file")
            print("B. Back")
            
            choice = input("\nChoice: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice == '1':
                self.configure()
            elif choice == '2':
                to = input("To email: ").strip()
                subj = input("Subject: ").strip()
                print("Enter HTML body (finish with 'END' on its own line):")
                lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    lines.append(line)
                body = '\n'.join(lines)
                self.send_email(to, subj, body)
            elif choice == '3':
                to = input("Target email: ").strip()
                fname = input("Spoof as name: ").strip()
                femail = input("Spoof as email: ").strip()
                subj = input("Subject: ").strip()
                print("Enter HTML body (finish with 'END'):")
                lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    lines.append(line)
                body = '\n'.join(lines)
                self.send_spoofed(to, fname, femail, subj, body)
            elif choice == '4':
                filepath = input("File with emails (one per line): ").strip()
                subj = input("Subject: ").strip()
                print("Enter HTML body (finish with 'END'):")
                lines = []
                while True:
                    line = input()
                    if line == 'END':
                        break
                    lines.append(line)
                body = '\n'.join(lines)
                try:
                    with open(filepath) as f:
                        recipients = [line.strip() for line in f if line.strip()]
                    self.send_campaign(recipients, subj, body)
                except Exception as e:
                    print(f"[!] Error reading file: {e}")