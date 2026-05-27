              DARKTHORN v3.2.7

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg">
  <img src="https://img.shields.io/badge/License-Educational%20Only-red.svg">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen.svg">
  <img src="https://img.shields.io/badge/Edition-SIGNATURE-gold.svg">
</p>

<p align="center">
  <b> Advanced Multi-Vector Denial of Service Testing Toolkit </b><br>
  <i>Signature Edition | Professional-grade penetration testing utility</i>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=F70000&center=true&vCenter=true&width=435&lines=DARKTHORN;The+Unseen+Sting;Piercing+Any+Defense" alt="Typing SVG">
</p>

Advanced Multi-Vector Denial of Service Testing Toolkit

---

📖 Tentang Darkthorn | About

🇮🇩 INDONESIA

Darkthorn Signature adalah toolkit pengujian ketahanan server untuk praktisi keamanan siber. Dirancang untuk stress testing dan analisis performa infrastruktur secara SAH.

Fitur utama:

| Fitur | Spesifikasi |
|-------|-------------|
| Multi-Protocol | HTTP/2, HTTP/3, HTTPS, TCP, UDP, DNS, SSL, WS |
| Bypass Engine | Cloudflare L3/L4/L7 + WAF Evasion |
| Proxy Chain | 10,000+ proxy rotation |
| Concurrent Threads | Up to 100,000 |
| Monitoring | RPS, bandwidth, error rate |

🇬🇧 ENGLISH

Darkthorn Signature is a server resilience testing toolkit for cybersecurity practitioners. Designed for lawful stress testing and infrastructure performance analysis.

---

📦 Instalasi | Installation

🇮🇩 Prasyarat:

```bash
# Minimal Python 3.8
python3 --version

# Install pip (Debian/Ubuntu)
sudo apt install python3-pip -y
```

Langkah instalasi:

```bash
git clone https://github.com/KalzzEngine/darkthorn.git
cd darkthorn
pip3 install -r requirements.txt
python3 darkthorn.py
```

Instalasi manual dependencies:

```bash
pip3 install cloudscraper colorama requests aiohttp websocket-client
```

---

🎮 Cara Penggunaan | Usage

🇮🇩 Penggunaan dasar:

```bash
python3 darkthorn.py
```

## Parameter yang Dapat Disesuaikan

| Parameter | Deskripsi | Contoh |
|-----------|-----------|--------|
| Target URL | Alamat target | https://example.com |
| Mode | AUTO (rekomendasi) / MANUAL | 1 atau 2 |
| Metode | 1-18, 30, atau auto | 1 |
| Thread | Jumlah konkurensi | 2000 |
| Durasi | Detik (0 = infinite) | 60 |

**Catatan:**

- **Mode 1 (AUTO)** - Tools akan mendeteksi WAF/CDN dan memilih metode terbaik secara otomatis
- **Mode 2 (MANUAL)** - Anda memilih metode sendiri dari daftar yang tersedia
- **Thread** - Semakin tinggi, semakin berat beban ke target. Sesuaikan dengan spesifikasi komputer Anda
- **Durasi 0** - Serangan akan berjalan terus hingga Anda tekan CTRL+C

🇬🇧 Basic usage:

```bash
python3 darkthorn.py
```

---

## ⚔️ Daftar Metode Serangan | Attack Methods

| ID | Method | Protocol | Description |
|----|--------|----------|-------------|
| 1 | HTTP/2 Rapid Reset | HTTP/2 | CVE-2023-44487 |
| 2 | Slowloris Advanced | HTTP | Partial request hold |
| 3 | SYN Flood | TCP | IP spoofing raw packet |
| 4 | UDP Amplification | UDP | DNS/NTP/SSDP |
| 5 | SSL Renegotiation | TLS | Crypto exhaustion |
| 6 | WebSocket Flood | WS | Persistent connection |
| 7 | GraphQL Depth | GraphQL | Recursive query |
| 8 | Range Header DoS | HTTP | CVE-2018-6389 |
| 9 | HTTP Pipeline | HTTP | Request pipelining |
| 10 | JSON Bomb | HTTP | Deep nesting |
| 11 | HTTP Smuggling | HTTP | CL.TE/TE.CL |
| 12 | IP Spoofing | L3 | Cloudflare L3 bypass |
| 13 | Port Hopping | L4 | Cloudflare L4 bypass |
| 14 | Fragmentation | IP | Packet fragment |
| 15 | curl_cffi Impersonate | HTTP | Chrome fingerprint |
| 16 | FlareSolverr | HTTP | JS challenge solver |
| 17 | ACME Path Bypass | HTTP | Cloudflare 0-day |
| 18 | Origin Direct | HTTP | Complete CF bypass |
| 30 | All Methods Combined | Mixed | All vectors |

> **Auto-detection (ID 99):** Smart recommendation based on WAF/CDN scan

---

## 💻 Persyaratan Sistem | System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 cores | 4+ cores |
| RAM | 2 GB | 4+ GB |
| Network | 10 Mbps | 100+ Mbps |
| Python | 3.8 | 3.10+ |
| OS | Linux / Windows / macOS | Kali Linux / Ubuntu |

🇮🇩 Optimasi performa Linux:

```bash
# Kernel tuning
sudo sysctl -w net.ipv4.tcp_tw_reuse=1
sudo sysctl -w net.core.rmem_max=134217728
sudo sysctl -w net.core.wmem_max=134217728
sudo sysctl -w net.ipv4.ip_local_port_range="1024 65535"

# File descriptor limit
ulimit -n 999999

# Untuk raw socket (SYN flood, IP spoofing)
sudo python3 darkthorn.py
```

---

## 🎯 Target Testing yang Didukung | Supported Targets

| Platform | Efektivitas | Keterangan |
|----------|-------------|-------------|
| Apache / Nginx / IIS | 100% | Standard web server |
| Cloudflare | 95% | L3/L4/L7 bypass active |
| AWS WAF / CloudFront | 85% | HTTP/2 rapid reset |
| Akamai | 80% | Header tampering |
| Imperva / Incapsula | 75% | IP spoofing + slow connection |
| Sucuri | 70% | Proxy rotation required |
| Vercel / Netlify | 80% | Function timeout exploit |
| WordPress | 90% | XML-RPC amplification |

---

## ⚖️ Dasar Hukum | Legal Basis

---

**🇮🇩 INDONESIA**

| Pasal | Ancaman |
|-------|---------|
| UU ITE Pasal 30 Ayat (1-5) | Penjara 6-12 tahun |
| UU ITE Pasal 33 Ayat (1-2) | Penjara 8-10 tahun |
| UU ITE Pasal 35 | Penjara 12 tahun |
| UU ITE Pasal 36 | Penjara 10 tahun |
| UU ITE Pasal 46-50 | Denda Rp600 juta - Rp12 miliar |

---

**🇬🇧 USA - CFAA 18 U.S.C. § 1030**

| Section | Penalty |
|---------|---------|
| (a)(2) - Unauthorized access | 1-5 years |
| (a)(3) - Government computers | 1-10 years |
| (a)(5)(A) - Damage to computers | 10-20 years |
| (c)(4) - Repeat offenders | Up to 20 years |

---

**🌐 Budapest Convention on Cybercrime (Council of Europe Treaty No.185)**

| Article | Offense |
|---------|---------|
| Art. 2-3 | Illegal access/interception |
| Art. 4-5 | Data/system interference |
| Art. 6 | Misuse of devices |
| Art. 9 | Computer-related offenses |

---

📋 Lisensi | License

```
EDUCATIONAL USE ONLY LICENSE
Copyright (c) 2026 KalzzEngine | Darkthorn Signature

PERMITTED:
✓ Cybersecurity learning and research
✓ Authorized penetration testing (written permission required)
✓ Isolated laboratory environment analysis

PROHIBITED:
✗ Attacking third-party services without permission
✗ Redistributing for illegal purposes
✗ Removing watermarks or attribution
✗ Commercial use without explicit permission

VIOLATIONS WILL BE PROSECUTED TO THE FULL EXTENT OF THE LAW
```

---

## 🔧 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| [!] Invalid method, using ALL METHODS | Method ID 99 hanya di AUTO mode. Gunakan mode MANUAL method 30 sebagai alternatif |
| Permission denied pada raw socket | Jalankan dengan `sudo python3 darkthorn.py` |
| Module not found | `pip3 install [nama_module]` |
| Rate limiting terdeteksi | Gunakan proxy rotation (method 16) |
| FlareSolverr error | Install FlareSolverr di localhost:8191 |

---

## 📞 Kontak | Contact

| Platform | Handle |
|----------|--------|
| GitHub | @KalzzEngine |
| Issues | Repository issue tracker |

---

<p align="center">
  <b>⚔️ "The Unseen Sting that Pierces Any Defense" ⚔️</b><br>
  <i>DARKTHORN SIGNATURE - Because not all thorns are seen</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/For%20Educational%20Purposes%20Only-FF0000.svg">
  <img src="https://img.shields.io/badge/SIGNATURE%20EDITION-Gold.svg?color=gold&labelColor=black">
  <img src="https://img.shields.io/badge/Legal%20Compliance%20Required-Orange.svg">
</p>

---

Version 3.2.7 | Last Updated: 05 • 27 • 2026