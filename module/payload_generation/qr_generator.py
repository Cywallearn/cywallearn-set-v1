"""Cywallearn SET - QR Code Phishing Generator"""

import os
import sys
import qrcode
from io import BytesIO
import base64
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class QRGenerator:
    def generate(self, url, label="", output_dir="data/reports"):
        """Generate QR code image"""
        os.makedirs(output_dir, exist_ok=True)
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"qr_{timestamp}.png"
        filepath = os.path.join(output_dir, filename)
        img.save(filepath)
        
        print(f"[+] QR code saved: {filepath}")
        print(f"[+] URL encoded: {url}")
        
        # Generate HTML with embedded QR
        html = f"""<!DOCTYPE html><html><head><title>Scan to Verify</title>
<style>body{{display:flex;justify-content:center;align-items:center;min-height:100vh;
background:#f5f5f5;font-family:sans-serif;text-align:center;}}
.card{{background:white;padding:40px;border-radius:20px;box-shadow:0 10px 40px rgba(0,0,0,0.1);}}
.qr{{width:250px;height:250px;margin:20px auto;}}</style></head><body>
<div class="card"><h2>Scan to Claim Your Reward</h2>
<div class="qr"><img src="data:image/png;base64,{self._img_to_b64(img)}" width="250"></div>
<p style="color:#666;">Scan with your phone camera to verify</p></div></body></html>"""
        
        html_path = filepath.replace('.png', '.html')
        with open(html_path, 'w') as f:
            f.write(html)
        print(f"[+] QR landing page: {html_path}")
        
        return filepath
    
    def _img_to_b64(self, img):
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()
    
    def interactive(self):
        print("\n=== QR Phishing Generator ===")
        url = input("Target URL (e.g., http://your-server/login): ").strip()
        label = input("Label (optional): ").strip()
        self.generate(url, label)
        input("\nPress Enter...")