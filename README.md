# Cywallearn SET v1 - Social Engineering Toolkit

> **FOR AUTHORIZED PENETRATION TESTING AND SECURITY EDUCATION ONLY**
> Unauthorized use against systems you don't own is illegal.

## Overview

Cywallearn SET is a complete social engineering framework for Termux with:

| Module | Features |
|--------|----------|
| **Web Phishing** | 12+ cloned login pages (Instagram, Facebook, Google, Twitter, LinkedIn, TikTok, Netflix, Amazon, PayPal + Quiz/Captcha) |
| **SMS Tools** | Send SMS via Termux-API, SMS spoofing, mass campaigns, template library |
| **Email Tools** | Send/spoof emails via Gmail SMTP, mass campaigns, HTML templates |
| **Credential Harvesting** | JS keylogger injection, form grabbers, OTP bypass pages |
| **Reconnaissance** | IP geolocation, OSINT gathering, device fingerprinting |
| **Payload Generation** | QR codes, shortened links with tracking, fake update pages |
| **Live Dashboard** | Real-time monitoring of captures, visits, and geolocation |
| **Tunnel Manager** | Serveo/Cloudflare tunnel integration for public URLs |
| **Telegram Alerts** | Real-time credential alerts sent to your Telegram |

## Quick Install

```bash
pkg update -y && pkg upgrade -y
pkg install git python -y
git clone https://github.com/YOUR_USERNAME/cywallearn-set-v1
cd cywallearn-set-v1
bash setup.sh
python cywallearn.py