"""Cywallearn SET - IP Tracking & Geolocation"""

import os
import sys
import requests
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.config import Config


class IPTracker:
    def __init__(self):
        self.tracking_file = os.path.join(Config.CAPTURE_DIR, "visits.json")

    def track_visit(self, ip, user_agent, referer, page):
        """Log a visit with geolocation data"""
        geo = self.geolocate(ip)

        visit = {
            'timestamp': datetime.now().isoformat(),
            'ip': ip,
            'user_agent': user_agent,
            'referer': referer,
            'page': page,
            'geo': geo
        }

        visits = []

        if os.path.exists(self.tracking_file):
            with open(self.tracking_file) as f:
                visits = json.load(f)

        visits.append(visit)

        with open(self.tracking_file, 'w') as f:
            json.dump(visits, f, indent=2)

        return geo

    def geolocate(self, ip):
        """Get geolocation data for IP"""

        if ip in ('127.0.0.1', '::1', 'localhost'):
            return {
                'city': 'Localhost',
                'country': 'Local',
                'isp': 'Local'
            }

        try:
            resp = requests.get(
                f'http://ip-api.com/json/{ip}',
                timeout=5
            )

            data = resp.json()

            if data.get('status') == 'success':
                return {
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'org': data.get('org', 'Unknown')
                }

        except Exception:
            pass

        return {
            'city': 'Unknown',
            'country': 'Unknown',
            'isp': 'Unknown'
        }

    def generate_tracking_pixel(self):
        """Generate invisible tracking pixel HTML"""
        return '<img src="/track" width="1" height="1" style="display:none" />'

    def interactive(self):
        print("\n=== IP Tracker ===")
        print("1. Track specific IP")
        print("2. View all tracked visits")
        print("3. Generate tracking pixel")

        choice = input("\nChoice: ").strip()

        if choice == '1':
            ip = input("IP address: ").strip()
            geo = self.geolocate(ip)

            print(f"\n[+] Location: {geo.get('city')}, {geo.get('country')}")
            print(f"[+] ISP: {geo.get('isp')}")
            print(f"[+] Coordinates: {geo.get('lat')}, {geo.get('lon')}")

        elif choice == '2':

            if os.path.exists(self.tracking_file):

                with open(self.tracking_file) as f:
                    visits = json.load(f)

                for v in visits[-10:]:
                    print(
                        f"\n[{v['timestamp']}] "
                        f"{v['ip']} - "
                        f"{v['geo'].get('city', '?')}"
                    )

            else:
                print("[!] No visits tracked yet")

        elif choice == '3':
            print(f"\n[+] Tracking pixel HTML:\n")
            print(self.generate_tracking_pixel())
            print("\n[+] Server endpoint needed: /track")