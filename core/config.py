"""Cywallearn SET - Global Configuration"""

import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Config:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = ""  # Set via menu
    SMTP_PASS = ""  # Set via menu
    
    PHISHING_PORT = 5000
    DASHBOARD_PORT = 5001
    
    CAPTURE_DIR = os.path.join(BASE_DIR, "data", "captured")
    LOG_DIR = os.path.join(BASE_DIR, "data", "logs")
    REPORT_DIR = os.path.join(BASE_DIR, "data", "reports")
    
    TELEGRAM_BOT_TOKEN = ""
    TELEGRAM_CHAT_ID = ""
    
    @classmethod
    def ensure_dirs(cls):
        for d in [cls.CAPTURE_DIR, cls.LOG_DIR, cls.REPORT_DIR]:
            os.makedirs(d, exist_ok=True)
    
    @classmethod
    def save(cls, key, value):
        cfg_file = os.path.join(BASE_DIR, "data", "config.json")
        data = {}
        if os.path.exists(cfg_file):
            with open(cfg_file) as f:
                data = json.load(f)
        data[key] = value
        with open(cfg_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, key, default=None):
        cfg_file = os.path.join(BASE_DIR, "data", "config.json")
        if os.path.exists(cfg_file):
            with open(cfg_file) as f:
                data = json.load(f)
            return data.get(key, default)
        return default