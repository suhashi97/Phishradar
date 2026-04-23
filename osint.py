import requests
import whois
import socket
import base64
import json
from playwright.sync_api import sync_playwright
import anthropic
from config import VIRUSTOTAL_API_KEY, ANTHROPIC_API_KEY
from datetime import datetime


def get_virustotal_report(url):
    try:
        headers = {"x-apikey": VIRUSTOTAL_API_KEY}
        requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        report = requests.get(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        ).json()
        stats = report.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return {
            "malicious": stats.get("malicious", 0),
            "suspicious": stats.get("suspicious", 0),
            "harmless": stats.get("harmless", 0),
            "undetected": stats.get("undetected", 0),
        }
    except Exception as e:
        return {"error": str(e), "malicious": 0, "suspicious": 0, "harmless": 0, "undetected": 0}


def get_infrastructure(url):
    try:
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        ip = socket.gethostbyname(domain)
        geo = requests.get(f"https://ipapi.co/{ip}/json/", timeout=8).json()
        try:
            w = whois.whois(domain)
            registrar = str(w.registrar) if w.registrar else "Unknown"
            creation_date = str(w.creation_date) if w.creation_date else "Unknown"
            expiry_date = str(w.expiration_date) if w.expiration_date else "Unknown"
        except:
            registrar = creation_date = expiry_date = "Unavailable"
        return {
            "domain": domain,
            "ip_address": ip,
            "country": geo.get("country_name", "Unknown"),
            "city": geo.get("city", "Unknown"),
            "org": geo.get("org", "Unknown"),
            "isp": geo.get("isp", "Unknown"),
            "registrar": registrar,
            "domain_created": creation_date,
            "domain_expires": expiry_date,
        }
    except Exception as e:
        return {"error": str(e)}


def take_screenshot(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=10000)
            screenshot = page.screenshot()
            browser.close()
            return base64.b64encode(screenshot).decode()
    except:
        return None


def ai_threat_analysis(url, vt_report, infra):
    try:
        from groq import Groq
        import os
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        prompt = f"""You are a cybersecurity threat intelligence analyst. Analyze this potential phishing URL.

URL: {url}
VirusTotal: {json.dumps(vt_report)}
Infrastructure: {json.dumps(infra)}

Respond ONLY in this exact JSON format, no markdown, no extra text:
{{
  "threat_level": "CRITICAL/HIGH/MEDIUM/LOW",
  "threat_type": "Phishing/Malware/Scam/Investment Fraud/Legitimate",
  "confidence": 85,
  "summary": "2-3 sentence plain English summary for law enforcement",
  "indicators": ["red flag 1", "red flag 2", "red flag 3"],
  "recommended_action": "What law enforcement should do",
  "c2_likelihood": "High/Medium/Low - reason in one sentence"
}}"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        text = response.choices[0].message.content.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {
            "threat_level": "UNKNOWN",
            "threat_type": "Analysis Failed",
            "confidence": 0,
            "summary": str(e),
            "indicators": [],
            "recommended_action": "Manual review required",
            "c2_likelihood": "Unknown"
        }

def full_analysis(url):
    if not url.startswith("http"):
        url = "https://" + url
    result = {
        "url": url,
        "timestamp": datetime.now().isoformat(),
        "virustotal": get_virustotal_report(url),
        "infrastructure": get_infrastructure(url),
        "screenshot": take_screenshot(url),
    }
    result["ai_analysis"] = ai_threat_analysis(
        url, result["virustotal"], result["infrastructure"]
    )
    return result