import requests
import re
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH


def fetch_openphish():
    try:
        resp = requests.get("https://openphish.com/feed.txt", timeout=10)
        urls = resp.text.strip().split("\n")
        return [u.strip() for u in urls if u.strip().startswith("http")][:10]
    except:
        return []


def fetch_urlhaus():
    try:
        resp = requests.get(
            "https://urlhaus-api.abuse.ch/v1/urls/recent/",
            timeout=10
        )
        data = resp.json()
        return [entry["url"] for entry in data.get("urls", [])[:10]]
    except:
        return []


def fetch_phishtank():
    try:
        resp = requests.get(
            "https://data.phishtank.com/data/online-valid.json",
            headers={"User-Agent": "phishradar-research/1.0"},
            timeout=10
        )
        data = resp.json()
        return [entry["url"] for entry in data[:10]]
    except:
        return []


def fetch_telegram_links():
    try:
        from telethon.sync import TelegramClient
        links = []
        url_pattern = re.compile(r'https?://[^\s]+')
        with TelegramClient('phishradar_session', TELEGRAM_API_ID, TELEGRAM_API_HASH) as client:
            channels = ['cybersecuritynews', 'phishingalert']
            for channel in channels:
                try:
                    for message in client.iter_messages(channel, limit=30):
                        if message.text:
                            found = url_pattern.findall(message.text)
                            links.extend(found)
                except:
                    continue
        return list(set(links))[:10]
    except Exception as e:
        print(f"Telegram scrape error: {e}")
        return []


def get_all_urls():
    urls = []
    urls += fetch_openphish()
    urls += fetch_urlhaus()
    urls += fetch_phishtank()
    urls += fetch_telegram_links()
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique[:20]