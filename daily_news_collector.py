import feedparser
import json
import os
import requests
from datetime import datetime, timedelta
from time import sleep
from urllib.parse import urlparse

# Change to working directory
os.chdir(r"D:\news")

# 1. Delete files older than 2 days
for file in os.listdir():
    if file.startswith("cybersecurity_news_") or file.startswith("CYBERBRIEF_"):
        try:
            date_part = file.split("_")[-1].replace(".json", "").replace(".txt", "")
            file_date = datetime.strptime(date_part, "%Y-%m-%d")
            if datetime.now() - file_date > timedelta(days=2):
                os.remove(file)
                print(f"Deleted old file: {file}")
        except:
            pass

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36'
}

# دالة تجميل اسم المصدر + أيقونة + وصف
def get_source_info(url):
    if not url:
        return "Unknown Source", "Globe", "Unknown"
    
    domain = urlparse(url).netloc.lower().replace('www.', '')
    
    sources = {
        'thehackernews.com':      ('The Hacker News',      'Newspaper',      'Tech News'),
        'krebsonsecurity.com':    ('Krebs on Security',   'User Secret',    'Expert Blog'),
        'bleepingcomputer.com':   ('BleepingComputer',    'Laptop Code',    'Security News'),
        'darkreading.com':        ('Dark Reading',        'Eye',            'Enterprise'),
        'theregister.com':        ('The Register',        'Server',         'Tech News'),
        'securityweek.com':       ('SecurityWeek',        'Shield Check',   'Cyber Media'),
        'cybernews.com':          ('Cybernews',           'Radioactive',    'Research'),
        'gbhackers.com':          ('GBHackers',          'Terminal',       'Hacking News'),
        'threatpost.com':         ('Threatpost',          'Alert Triangle', 'Kaspersky Lab'),
        'cisa.gov':               ('CISA Alert',          'Government',     'U.S. Government'),
        'us-cert.cisa.gov':       ('US-CERT',             'Flag',           'Official Alert'),
        'recordedfuture.com':     ('Recorded Future',     'Globe',          'Threat Intel'),
        'schneier.com':           ('Schneier on Security','Lock',           'Cryptography'),
        'helpnetsecurity.com':    ('Help Net Security',   'Shield',         'Security Portal'),
        'securityaffairs.co':     ('Security Affairs',    'Bug',            'Independent'),
        'zdnet.com':              ('ZDNet Security',      'Laptop',         'Tech Giant'),
    }
    
    for key, (name, icon, tag) in sources.items():
        if key in domain:
            return name, icon, tag
    
    clean_name = domain.split('.')[0].title().replace('-', ' ')
    return clean_name, "Link", "News Site"

# Read RSS sources
with open('sources.txt', 'r', encoding='utf-8', errors='replace') as f:
    rss_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

print(f"[{datetime.now().strftime('%H:%M')}] Starting collection from {len(rss_urls)} sources...")

all_news = []
for url in rss_urls:
    try:
        print(f"→ {url}")
        response = requests.get(url, headers=headers, timeout=25)
        feed = feedparser.parse(response.content)
        
        if not feed.entries:
            print("   No entries")
            continue
            
        for entry in feed.entries[:20]:
            link = entry.get('link', '').strip()
            published = entry.get('published') or entry.get('updated') or entry.get('date') or "Just now"
            
            title = entry.get('title', 'No title').strip()
            summary = entry.get('summary') or entry.get('description') or ""
            if isinstance(summary, list):
                summary = summary[0].get('value', '') if summary else ''
            summary = (summary or "No summary available")[:700]
            
            source_name, source_icon, source_tag = get_source_info(link)
            
            all_news.append({
                "title": title,
                "link": link,
                "summary": summary,
                "published": published,
                "source_name": source_name,
                "source_icon": source_icon,
                "source_tag": source_tag,
                "domain": urlparse(link).netloc if link else "unknown"
            })
        sleep(1.3)
    except Exception as e:
        print(f"   Error: {e}")
        continue

# Save full data
today = datetime.now().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_news, f, ensure_ascii=False, indent=2)

# Top 7 threats
keywords = ["zero-day","cisa","rce","kev","actively exploited","ransomware","apt","fbi","exploit","breach"]
def importance_score(item):
    text = (item['title'] + " " + item['summary']).lower()
    score = len(text)
    critical_hits = sum(kw in text for kw in keywords)
    return score + critical_hits * 400 + ("cisa" in text) * 1000

all_news.sort(key=importance_score, reverse=True)
top_7 = all_news[:7]

# Generate beautiful report
report = [
    "CYBERBRIEF • DAILY THREAT INTELLIGENCE",
    f"Generated: {datetime.now().strftime('%A, %B %d, %Y - %H:%M UTC')}",
    "="*80,
    ""
]

for i, item in enumerate(top_7, 1):
    report.extend([
        f"{i}. {item['source_icon']} {item['source_name']}  [{item['source_tag']}]",
        f"   Title: {item['title']}",
        f"   Published: {item['published']}",
        f"   Link: {item['link']}",
        ""
    ])

report += [
    "",
    "Security Tips:",
    "• Never trust unsolicited links",
    "• Enable 2FA everywhere",
    "• Keep systems patched",
    "",
    f"Scanned {len(all_news)} articles • Top 7 active threats selected",
    "Next auto-update: 08:00 AM UTC",
    "Stay safe, stay sharp!"
]

txt_file = f"CYBERBRIEF_{today}.txt"
with open(txt_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(report))

print("\n" + "SUCCESS!"*10)
print(f"Collected {len(all_news)} high-quality articles")
print(f"JSON saved → {json_file}")
print(f"Report saved → {txt_file}")
print("Old files cleaned • Ready for tomorrow!")
print("SUCCESS!"*10)
