"""Cywallearn SET - Link Shortener & Tracker"""

import os
import hashlib
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.config import Config

class LinkGenerator:
    def __init__(self):
        self.links_file = os.path.join(Config.CAPTURE_DIR, "generated_links.json")
        os.makedirs(Config.CAPTURE_DIR, exist_ok=True)
    
    def shorten(self, target_url, campaign=""):
        """Generate shortened link with tracking ID"""
        tracking_id = hashlib.md5(f"{target_url}{datetime.now()}".encode()).hexdigest()[:8]
        
        link_data = {
            'id': tracking_id,
            'target': target_url,
            'campaign': campaign,
            'created': datetime.now().isoformat(),
            'clicks': 0
        }
        
        links = []
        if os.path.exists(self.links_file):
            with open(self.links_file) as f:
                links = json.load(f)
        links.append(link_data)
        with open(self.links_file, 'w') as f:
            json.dump(links, f, indent=2)
        
        short_link = f"http://your-server/l/{tracking_id}"
        
        print(f"\n[+] Generated link: {short_link}")
        print(f"[+] Redirects to: {target_url}")
        print(f"[+] Tracking ID: {tracking_id}")
        
        return short_link
    
    def generate_phishing_links(self, base_url, platforms):
        """Generate multiple phishing links at once"""
        links = {}
        for platform in platforms:
            url = f"{base_url}/login?p={platform}"
            short = self.shorten(url, f"campaign_{platform}")
            links[platform] = short
        return links
    
    def interactive(self):
        print("\n=== Link Generator ===")
        url = input("Target URL to shorten: ").strip()
        campaign = input("Campaign name (optional): ").strip()
        self.shorten(url, campaign)
        input("\nPress Enter...")