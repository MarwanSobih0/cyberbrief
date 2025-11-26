import feedparser
import json
import os
import requests
from datetime import datetime, timedelta
from time import sleep

# Change to working directory
os.chdir(r"D:\news")

# 1. Delete files older than 2 days to save space
for file in os.listdir():
    if file.startswith("cybersecurity_news_") or file.startswith("Daily_Cybersecurity_Report_"):
        try:
            date_part = file.split("_")[-1].replace(".json", "").replace(".txt", "")
            file_date = datetime.strptime(date_part, "%Y-%m-%d")
            if datetime.now() - file_date > timedelta(days=2):
                os.remove(file)
                print(f"Deleted old file: {file}")
        except:
            pass

# Headers to bypass blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130.0.0.0 Safari/537.36'
}

# Read RSS sources
with open('sources.txt', 'r', encoding='utf-8', errors='replace') as f:
    rss_urls = [line.strip() for line in f if line.strip()]

print(f"[{datetime.now().strftime('%H:%M')}] Collecting news from {len(rss_urls)} sources...")

all_news = []
for url in rss_urls:
    try:
        print(f"→ {url}")
        response = requests.get(url, headers=headers, timeout=20)
        feed = feedparser.parse(response.content)
        if feed.entries:
            for entry in feed.entries[:15]:
                all_news.append({
                    "title": entry.get('title', 'No title'),
                    "link": entry.get('link', ''),
                    "summary": (entry.get('summary') or entry.get('description') or '')[:500]
                })
        sleep(1)
    except Exception as e:
        print(f"   Failed: {e}")
        continue

# Save raw data as JSON
today = datetime.now().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(all_news, f, ensure_ascii=False, indent=2)

# 2. Smart selection of top 5 most important news
keywords = ["breach", "ransomware", "zero-day", "exploit", "phishing", "attack", "vulnerability", "leak", "malware", "hack"]

def importance_score(item):
    text = (item['title'] + " " + item['summary']).lower()
    score = len(text)
    hits = sum(word in text for word in keywords)
    return score + hits * 50

all_news.sort(key=importance_score, reverse=True)
top_5 = all_news[:5]

# 3. Generate clean English daily report
report = [
    "DAILY CYBERSECURITY BRIEF",
    f"Date: {datetime.now().strftime('%B %d, %Y')}",
    "=" * 60,
    ""
]

for i, news in enumerate(top_5, 1):
    report.append(f"{i}. {news['title']}")
    report.append(f"   Link: {news['link']}")
    report.append("")

report += [
    "Quick Security Tips:",
    "• Never click suspicious links",
    "• Enable Two-Factor Authentication (2FA)",
    "• Keep your software and OS updated",
    "",
    "This report is automatically generated every day at 8:00 AM",
    "Stay safe online!"
]

# Save the final English report
txt_file = f"Daily_Cybersecurity_Report_{today}.txt"
with open(txt_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(report))

print("\n" + "═" * 70)
print("SUCCESS! Everything completed.")
print(f"Collected {len(all_news)} articles → {json_file}")
print(f"Top 5 English report saved → {txt_file}")
print("Old files will be auto-deleted after 2 days")
print("═" * 70)