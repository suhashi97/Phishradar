<div align="center">

# 🛡️ PhishRadar

### Autonomous Cyber Fraud Threat Intelligence System

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![LLaMA](https://img.shields.io/badge/AI-LLaMA%203.3%2070B-00A67E?style=for-the-badge&logo=meta&logoColor=white)
![VirusTotal](https://img.shields.io/badge/VirusTotal-70%2B%20Engines-394EFF?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-C0392B?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-27AE60?style=for-the-badge)

<br/>

> **"6,000 cyber fraud cases daily. Manual investigation: IMPOSSIBLE. AI investigation: 30 SECONDS."**

<br/>

[🚀 Features](#-features) • [📸 Demo](#-demo) • [⚙️ Installation](#-installation) • [🏗️ Architecture](#-architecture) • [🔌 API](#-api-reference) • [🗺️ Roadmap](#-roadmap)

</div>

---

## 🚨 The Problem

India alone reports **6,000+ cyber fraud cases every single day** — phishing sites impersonating banks, fake investment apps, fraudulent social media posts stealing credentials from real people.

Manual OSINT investigation takes **2–3 days per case**. By then:
- ❌ The phishing site is already offline
- ❌ Evidence is gone forever
- ❌ The criminal has moved to a new domain
- ❌ Victims keep getting scammed

**No human team can investigate 6,000 cases a day. PhishRadar can.**

---

## ✅ What PhishRadar Does

PhishRadar is a **fully autonomous AI-driven OSINT platform** that hunts, investigates, and reports cyber fraud threats — completely without human input.

```
Phishing URL Discovered → Analyzed in 30 seconds → Law Enforcement PDF Ready
```

- 🔍 **Autonomously discovers** phishing URLs from 4 live OSINT feeds every 90 seconds
- 🦠 **Scans with VirusTotal** across 70+ antivirus engines simultaneously  
- 🌐 **Maps full infrastructure** — IP, ASN, hosting provider, WHOIS, domain age
- 🕵️ **Assesses C2 servers** — identifies if phishing site is part of a larger criminal network
- 🤖 **AI classifies threats** — CRITICAL / HIGH / MEDIUM / LOW with confidence score
- 📸 **Screenshots phishing pages** as forensic evidence before they disappear
- 📄 **Generates law enforcement PDFs** with all evidence in one professional report
- 📧 **Emails evidence packages** directly to cybercrime authorities
- 🔄 **Runs 24/7 with zero human input** after a single click

---

## 🎯 Features

| Feature | Details |
|---|---|
| **4-Source OSINT Ingestion** | OpenPhish + URLhaus + PhishTank + Telegram channels |
| **VirusTotal Integration** | 70+ AV engines — malicious, suspicious, harmless counts |
| **Infrastructure Mapping** | IP address, country, city, ISP, ASN, hosting provider |
| **WHOIS Analysis** | Registrar, domain creation date, expiry — catches newly registered fraud domains |
| **C2 Server Assessment** | AI evaluates if site is part of Command & Control network |
| **LLaMA 3.3 70B AI** | State-of-the-art threat classification via Groq (free, 300+ tokens/sec) |
| **Forensic Screenshots** | Headless Chromium captures live phishing pages as court evidence |
| **Law Enforcement PDF** | Professional report with all IoCs ready for submission |
| **One-Click Email** | Sends PDF + screenshot directly to any cybercrime authority email |
| **Real-Time Dashboard** | Live threat feed with auto-updating cards every 5 seconds |
| **Manual URL Analysis** | Paste any suspicious URL for instant on-demand investigation |

---

## 📸 Demo

```bash
git clone https://github.com/yourusername/phishradar.git
cd phishradar
pip install -r requirements.txt
py app.py
```

Open `http://localhost:5000` → Click **▶ AUTO-SCAN** → Watch PhishRadar hunt threats autonomously.

**What you'll see:**
- 🟢 AUTO-SCANNING status activates
- Threat cards appear with CRITICAL/HIGH/MEDIUM/LOW badges
- Click any card → full infrastructure map, AI analysis, screenshot
- Download PDF or email directly to authorities

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                             │
│                                                                  │
│   OpenPhish Feed  │  URLhaus API  │  PhishTank JSON  │ Telegram │
│   (Live phishing) │  (Malware)    │  (Verified)      │ Channels │
└────────────────────────────┬────────────────────────────────────┘
                             │  New URLs every 90 seconds
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FLASK BACKEND  (app.py)                        │
│                                                                  │
│   Background daemon thread → auto_scan_loop()                   │
│   REST API → /analyze /scan-results /report /send-report        │
└──────┬──────────────┬──────────────┬──────────────┬────────────┘
       │              │              │              │
       ▼              ▼              ▼              ▼
 ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
 │VirusTotal│  │ WHOIS +  │  │Playwright│  │  Groq API    │
 │  API     │  │ IP/ASN   │  │Screenshot│  │ LLaMA 3.3 70B│
 │ 70+ AVs  │  │ Geo-IP   │  │ Chromium │  │ Threat Intel │
 └──────────┘  └──────────┘  └──────────┘  └──────────────┘
       │              │              │              │
       └──────────────┴──────────────┴──────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      OUTPUT LAYER                                │
│                                                                  │
│   Live Dashboard  │  Threat Cards  │  PDF Report  │  Email      │
│   (Real-time UI)  │  (CRITICAL...) │  (ReportLab) │  (Gmail)    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
phishradar/
│
├── app.py                      # Flask server, auto-scan loop, all API routes
├── osint.py                    # VirusTotal, WHOIS, IP lookup, screenshot, AI analysis
├── scraper.py                  # OSINT scrapers: OpenPhish, URLhaus, PhishTank, Telegram
├── report.py                   # PDF report generator using ReportLab
├── config.py                   # Environment variable loader via python-dotenv
│
├── .env                        # API keys — NEVER commit this file
├── .gitignore                  # Excludes .env, sessions, cache
├── requirements.txt            # All Python dependencies
│
└── templates/
    └── index.html              # Real-time dark-theme dashboard UI
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- Windows / macOS / Linux

### Step 1 — Clone
```bash
git clone https://github.com/yourusername/phishradar.git
cd phishradar
```

### Step 2 — Install dependencies
```bash
pip install flask flask-cors flask-mail requests python-whois reportlab playwright anthropic telethon python-dotenv groq
playwright install chromium
```

### Step 3 — Configure `.env`
Create a `.env` file in the root directory:

```env
# Threat Intelligence
VIRUSTOTAL_API_KEY=your_virustotal_key_here
GROQ_API_KEY=your_groq_key_here

# Telegram OSINT
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash

# Email Reporting
MAIL_USERNAME=your_gmail@gmail.com
MAIL_PASSWORD=your_16_digit_app_password
REPORT_EMAIL=cybercrime@police.gov.in
```

### Step 4 — Get free API keys

| Key | Website | Time |
|---|---|---|
| `VIRUSTOTAL_API_KEY` | [virustotal.com](https://virustotal.com) → Sign up → API Key | 2 min |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys | 2 min |
| `TELEGRAM_API_ID/HASH` | [my.telegram.org](https://my.telegram.org) → API Development Tools | 2 min |
| `MAIL_PASSWORD` | myaccount.google.com → Security → App Passwords | 3 min |

### Step 5 — Run
```bash
py app.py
# or
python app.py
```

### Step 6 — Open browser
```
http://localhost:5000
```

Click **▶ AUTO-SCAN** and PhishRadar will start hunting threats autonomously!

---

## 🔌 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the real-time dashboard UI |
| `/start-auto-scan` | `POST` | Starts autonomous scanning background thread |
| `/stop-auto-scan` | `POST` | Stops the scanning loop |
| `/scan-results` | `GET` | Returns all scan results + running status |
| `/analyze` | `POST` | Analyzes a single URL on demand |
| `/report` | `POST` | Generates and downloads a PDF report |
| `/send-report` | `POST` | Emails PDF + screenshot to authorities |

### Analyze a URL
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "http://suspicious-phishing-site.com"}'
```

### Example Response
```json
{
  "url": "http://suspicious-phishing-site.com",
  "timestamp": "2026-04-24T10:30:00",
  "virustotal": {
    "malicious": 23,
    "suspicious": 5,
    "harmless": 42,
    "undetected": 25
  },
  "infrastructure": {
    "domain": "suspicious-phishing-site.com",
    "ip_address": "185.220.101.45",
    "country": "Russia",
    "city": "Moscow",
    "org": "AS12345 BulletproofHost LLC",
    "isp": "Frantech Solutions",
    "registrar": "NameCheap Inc.",
    "domain_created": "2026-04-22",
    "domain_expires": "2027-04-22"
  },
  "ai_analysis": {
    "threat_level": "CRITICAL",
    "threat_type": "Phishing",
    "confidence": 95,
    "summary": "This URL is a confirmed phishing site targeting ICICI Bank customers, registered 2 days ago on bulletproof hosting infrastructure with 23 malicious AV detections.",
    "indicators": [
      "Domain registered 2 days ago",
      "Hosted on bulletproof infrastructure in Russia",
      "23 out of 95 AV engines flagged as malicious",
      "URL path mimics ICICI Bank login page"
    ],
    "recommended_action": "Immediately block domain, report to CERT-In and I4C, notify ICICI Bank fraud team",
    "c2_likelihood": "High - bulletproof hosting provider commonly associated with C2 infrastructure"
  }
}
```

### Send Email Report
```bash
curl -X POST http://localhost:5000/send-report \
  -H "Content-Type: application/json" \
  -d '{"url": "...", "recipient_email": "cybercrime@police.gov.in", ...}'
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.14, Flask | REST API server |
| **Concurrency** | Python threading | Background auto-scan loop |
| **AI Model** | LLaMA 3.3 70B via Groq | Threat classification & intelligence |
| **Threat Intel** | VirusTotal API | 70+ AV engine consensus |
| **OSINT Feeds** | OpenPhish, URLhaus, PhishTank | Live phishing URL discovery |
| **Social OSINT** | Telegram via Telethon | Social media fraud link scraping |
| **Infrastructure** | python-whois, ipapi.co, socket | Domain & IP investigation |
| **Screenshots** | Playwright + Chromium | Forensic page capture |
| **PDF Reports** | ReportLab | Law enforcement documentation |
| **Email** | Flask-Mail + Gmail SMTP | Authority notification |
| **Frontend** | HTML5, CSS3, Vanilla JS | Real-time dashboard |

---

## ⚠️ Current Limitations

| Limitation | Impact | Planned Fix |
|---|---|---|
| In-memory storage | Results lost on server restart | PostgreSQL persistent database |
| VirusTotal free tier | 4 requests/minute rate limit | Premium API key or key rotation |
| No Twitter/X scraping | Paid API required ($100/month) | CERT-In and I4C feed integration |
| Screenshot blocking | ~40% of phishing sites block bots | Playwright stealth plugins |
| No persistent deduplication | Same URL re-analyzed after restart | Redis URL hash cache |
| Single server deployment | Not horizontally scalable yet | Celery task queue + Docker |
| False positive rate | ~5-10% borderline cases | Human review queue for MEDIUM threats |

---

## 🗺️ Roadmap

```
v1.0 (Current) ──► v2.0 ──► v3.0 ──► v4.0 ──► v5.0
```

- **v1.0** ✅ Core pipeline — OSINT scraping, AI analysis, PDF reports, email
- **v2.0** 🔄 PostgreSQL storage + historical trend analysis + deduplication
- **v2.1** 🔄 CERT-In and I4C direct API integration for automatic case filing
- **v3.0** 🔄 Campaign clustering — group related phishing sites by C2 infrastructure
- **v3.1** 🔄 Predictive detection — flag suspicious domains before they go live
- **v4.0** 🔄 Mobile app — citizen fraud reporting directly into pipeline
- **v5.0** 🔄 National deployment — handle all 6,000 daily Indian fraud cases in real time

---

## 🤝 Contributing

Contributions are welcome! PhishRadar is built for social good — help make it better.

```bash
# Fork the repository
# Create your feature branch
git checkout -b feature/YourFeature

# Make your changes and commit
git commit -m "Add: YourFeature description"

# Push and open a Pull Request
git push origin feature/YourFeature
```

**Good first issues:**
- Add more OSINT feed sources
- Improve screenshot bypass techniques
- Add database persistence layer
- Add more language support for reports

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

---

## ⚡ Disclaimer

PhishRadar is built **strictly for defensive cybersecurity research and law enforcement support**. All data sources used are public threat intelligence feeds. This tool must only be used to investigate URLs from public threat feeds or with explicit permission. Never use PhishRadar to investigate private systems without authorization.

---

## 🙏 Acknowledgements

- [OpenPhish](https://openphish.com) — Live phishing URL intelligence feed
- [URLhaus (abuse.ch)](https://urlhaus.abuse.ch) — Community malware URL database
- [PhishTank](https://phishtank.org) — Community-verified phishing URL database
- [VirusTotal](https://virustotal.com) — Multi-engine threat intelligence platform
- [Groq](https://groq.com) — Ultra-fast open-source LLM inference
- [Meta LLaMA](https://llama.meta.com) — Open-source AI foundation model
- [Playwright](https://playwright.dev) — Reliable browser automation

---

<div align="center">

**Built with ❤️ for a safer internet — Made in India 🇮🇳**

<br/>

⭐ **Star this repo if PhishRadar helped you!** ⭐

<br/>

`"PhishRadar — Because 6,000 fraud victims a day is 6,000 too many."`

</div>
