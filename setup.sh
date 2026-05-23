#!/bin/bash
# Cywallearn SET v1 - Setup Script
# FOR AUTHORIZED PENETRATION TESTING ONLY

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}[+] Cywallearn SET v1 - Installing...${NC}"

# Update packages
echo -e "${YELLOW}[*] Updating packages...${NC}"
pkg update -y && pkg upgrade -y

# Install core dependencies
echo -e "${YELLOW}[*] Installing core packages...${NC}"
pkg install python python-pip git openssh termux-api -y

# Create directory structure
echo -e "${YELLOW}[*] Creating directory structure...${NC}"
mkdir -p modules/web_phishing/templates/{instagram,facebook,google,twitter,linkedin,tiktok,snapchat,netflix,amazon,paypal,quiz,captcha,custom}
mkdir -p modules/sms_tools
mkdir -p modules/email_tools
mkdir -p modules/credential_harvesting
mkdir -p modules/reconnaissance
mkdir -p modules/payload_generation
mkdir -p modules/reporting
mkdir -p data/{captured,logs,reports}

# Install Python packages
echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip install flask requests pillow qrcode cryptography beautifulsoup4 colorama pyngrok

# Make launcher executable
chmod +x cywallearn.py

echo -e "${GREEN}[✓] Cywallearn SET v1 installed successfully!${NC}"
echo -e "${GREEN}[+] Run: python cywallearn.py${NC}"