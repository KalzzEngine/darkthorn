```markdown
# DARKTHORN ATTACK SUITE v4.2.0

> **⚠️ PERINGATAN PENTING | IMPORTANT WARNING**
> 
> **Bahasa Indonesia:** Tools ini dibuat untuk **tujuan edukasi dan pengujian keamanan yang sah**. Menggunakan alat ini pada sistem atau jaringan tanpa izin tertulis adalah tindakan ilegal. Penulis tidak bertanggung jawab atas penyalahgunaan.
>
> **English:** This tool is created for **educational and lawful security testing purposes only**. Using this tool on systems or networks without written permission is illegal. The author assumes no liability for misuse.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey.svg">
  <img src="https://img.shields.io/badge/License-Educational%20Only-red.svg">
  <img src="https://img.shields.io/badge/Status-For%20Education-yellow.svg">
</p>

---

## 📖 Deskripsi | Description

**🇮🇩 Bahasa Indonesia**  
Darkthorn adalah toolkit pengujian stres server profesional yang dirancang untuk praktisi keamanan siber. Tools ini membantu mengidentifikasi kerentanan infrastruktur melalui simulasi berbagai serangan DDoS.

**🇬🇧 English**  
Darkthorn is a professional server stress testing toolkit designed for cybersecurity practitioners. This tool helps identify infrastructure vulnerabilities through simulation of various DDoS attack vectors.

---

## ⚙️ Fitur | Features

- 10 metode serangan berbeda | 10 different attack methods
- Cloudflare bypass & JS challenge solver
- Multi-threading support hingga 10.000+ thread
- Proxy chain & rotasi otomatis
- Real-time statistik bandwidth
- Cross-platform (Linux, Windows, macOS)

---

## 📦 Instalasi | Installation

```bash
# Clone repository
git clone https://github.com/username/darkthorn.git
cd darkthorn

# Install dependencies
pip3 install cloudscraper colorama requests

# Run
python3 darkthorn.py
```

---

🚀 Penggunaan | Usage

```bash
python3 darkthorn.py
```

Kemudian ikuti prompt untuk memasukkan:

1. Target URL
2. Metode serangan (1-10)
3. Jumlah thread
4. Durasi serangan

---

📋 Metode Serangan | Attack Methods

No Metode Deskripsi
1 HTTP/2 Rapid Reset Exploit HTTP/2 stream cancellation
2 Slowloris DDoS Keep connections half-open
3 Socket Flood Raw TCP/SSL socket flooding
4 Proxy Chain Attack Rotate proxies to avoid blocking
5 Multi-Vector Assault HTTP + TCP combined attack
6 CF Bypass Engine Solve Cloudflare challenges
7 SSL Renegotiation CPU-heavy crypto operations
8 DNS Amplification Spoofed DNS amplification
9 JavaScript Solver Custom anti-bot bypass
10 All Combined Execute all methods simultaneously

---

🛡️ Disclaimer

Penggunaan tools ini di luar lingkungan yang sah (milik sendiri / izin tertulis) melanggar hukum. Penulis tidak bertanggung jawab atas kerusakan atau konsekuensi hukum yang timbul.

Using this tool outside lawful environments (your own property / written permission) violates the law. The author is not responsible for damages or legal consequences.

---

📄 Lisensi | License

Educational Use Only - Tidak diizinkan untuk penggunaan komersial atau ilegal.

---

⭐ Catatan | Note

Tools ini dibuat untuk edukasi keamanan siber dan pengujian penetrasi dengan izin. Gunakan secara bertanggung jawab.

```
