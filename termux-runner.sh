#!/bin/bash
# Cywallearn SET v1 - Termux Runner
# FOR AUTHORIZED PENETRATION TESTING ONLY

clear
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${RED}"
echo "╔═══════════════════════════════════════════════╗"
echo "║     CYWALLEARN SET v1                         ║"
echo "║     Social Engineering Toolkit                ║"
echo "║     FOR AUTHORIZED TESTING ONLY               ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
if ! command -v python &> /dev/null; then
    echo -e "${RED}[!] Python not found. Run: bash setup.sh${NC}"
    exit 1
fi

# Launch
echo -e "${GREEN}[+] Launching Cywallearn SET...${NC}"
python cywallearn.py