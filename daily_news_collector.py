import os
import json
from datetime import datetime, timedelta
from urllib.parse import urlparse

import feedparser

# ================== GLOBAL CONFIG ==================

# Base directory where JSON/TXT will be saved and where sources.txt lives.
# You can override this with an environment variable CYBERBRIEF_DIR.
BASE_DIR = os.environ.get("CYBERBRIEF_DIR", os.getcwd())
os.chdir(BASE_DIR)

TODAY = datetime.utcnow().date()
TODAY_STR = TODAY.strftime("%Y-%m-%d")

SOURCES_FILE = "sources.txt"
JSON_FILE = f"cybersecurity_news_{TODAY_STR}.json"
REPORT_FILE = f"CYBERBRIEF_{TODAY_STR}.txt"

# ================== CLEANUP OLD FILES ==================

def cleanup_old_files(days: int = 2):
    """
    Remove old JSON files older than 'days' from BASE_DIR.
    Keeps only the last <days> days of cybersecurity_news_*.json.
    Does NOT touch CYBERBRIEF_*.txt.
    """
    today = datetime.utcnow().date()
    cutoff = today - timedelta(days=days)

    for fname in os.listdir(BASE_DIR):
        # نتعامل فقط مع ملفات الـ JSON الخاصة بالأخبار
        if not (fname.startswith("cybersecurity_news_") and fname.endswith(".json")):
            continue

        try:
            # cybersecurity_news_YYYY-MM-DD.json
            date_part = fname.replace("cybersecurity_news_", "").replace(".json", "")
            file_date = datetime.strptime(date_part, "%Y-%m-%d").date()
        except Exception:
            # Ignore files with unexpected naming
            continue

        if file_date < cutoff:
            try:
                os.remove(os.path.join(BASE_DIR, fname))
                print(f"[CLEANUP] Removed old JSON: {fname} (date: {file_date}, cutoff: {cutoff})")
            except OSError as e:
                print(f"[CLEANUP] Failed to remove {fname}: {e}")

# ================== LOAD RSS SOURCES ==================

def load_sources(path: str):
    """
    Load RSS feed URLs from sources.txt (ignores empty lines and lines starting with '#').
    """
    urls = []
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    return urls

# Keywords for scoring importance based on content
KEYWORDS = {
    "critical": [
        "zero-day", "0-day", "actively exploited", "rce", "remote code execution",
        "pre-auth", "preauth", "wormable"
    ],
    "high": [
        "ransomware", "data breach", "extortion", "double extortion",
        "supply chain attack", "credential stuffing"
    ],
    "medium": [
        "phishing", "smishing", "vishing", "malware", "spyware",
        "backdoor", "token theft", "account takeover"
    ],
}

# Optional: per-source weight to boost more authoritative feeds
SOURCE_WEIGHTS = {
    # Big vendor / official sources
    "security.googleblog.com": 1.4,
    "googleprojectzero.blogspot.com": 1.5,
    "microsoft.com": 1.4,
    "blogs.microsoft.com": 1.4,
    "blog.talosintelligence.com": 1.4,
    "unit42.paloaltonetworks.com": 1.4,
    "crowdstrike.com": 1.3,
    "fortinet.com": 1.3,
    "trendmicro.com": 1.3,
    "nakedsecurity.sophos.com": 1.2,
    "securelist.com": 1.3,
    "welivesecurity.com": 1.2,

    # Official advisories / gov CSIRTs (if you add their feeds)
    "cisa.gov": 1.6,
    "us-cert.gov": 1.6,
    "ncsc.gov.uk": 1.5,

    # Classic news outlets
    "thehackernews.com": 1.1,
    "bleepingcomputer.com": 1.1,
    "krebsonsecurity.com": 1.2,
    "securityweek.com": 1.1,
}

# ================== CATEGORY CLASSIFICATION ==================

def classify_category(text: str) -> str:
    """
    Simple keyword-based classifier to assign a high-level category
    to each news item, based on its title + summary text.
    """
    t = text.lower()
    if any(w in t for w in ["ransomware", "locker", "encrypt", "decryptor"]):
        return "Ransomware"
    if any(w in t for w in ["data breach", "leak", "database exposed", "records exposed", "stolen data"]):
        return "Data Breach"
    if any(w in t for w in ["cve-", "vulnerability", "zero-day", "remote code execution", "rce", "privilege escalation"]):
        return "Vulnerability"
    if any(w in t for w in ["phishing", "smishing", "vishing", "scam", "fraud", "social engineering"]):
        return "Phishing / Scams"
    if any(w in t for w in ["regulation", "law", "bill", "compliance", "gdpr", "fine", "penalty"]):
        return "Policy / Law"
    if any(w in t for w in [" ai ", " llm ", "model", "neural network", "machine learning"]):
        return "AI & Security"
    if any(w in t for w in ["critical infrastructure", "power grid", "pipeline", "hospital", "water plant"]):
        return "Critical Infrastructure"
    return "Other"

# ================== IMPORTANCE SCORING ==================

def importance_score(title: str, summary: str, published):
    """
    Compute a numeric importance score based on:
    - summary length
    - critical/high/medium keywords
    - important entities
    - recency (how many hours ago)
    """
    text = f"{title} {summary}".lower()
    score = 0

    # Base length contribution (capped so it doesn't explode on very long summaries)
    base_len = min(len(summary), 800)
    score += base_len // 4

    # Keyword bonuses
    for kw in KEYWORDS["critical"]:
        if kw in text:
            score += 600
    for kw in KEYWORDS["high"]:
        if kw in text:
            score += 450
    for kw in KEYWORDS["medium"]:
        if kw in text:
            score += 250

    # Important entities (vendors, agencies)
    for marker in ["cisa", "nsa", "fbi", "microsoft", "google", "apple", "fortinet", "vmware", "citrix"]:
        if marker in text:
            score += 150

    # Recency bonus: more recent = higher score
    if published is not None:
        hours_ago = (datetime.utcnow() - published).total_seconds() / 3600.0
        if hours_ago <= 24:
            score += 300
        elif hours_ago <= 72:
            score += 150

    return score

# ================== TITLE NORMALIZATION & SOURCE PARSING ==================

def normalize_title(title: str) -> str:
    """
    Normalize a title for de-duplication:
    - lowercase
    - remove punctuation
    - keep first ~10 words
    """
    t = title.lower()
    for ch in ".,:;!?()[]{}|/\\'\"":
        t = t.replace(ch, " ")
    words = [w for w in t.split() if len(w) > 2]
    return " ".join(words[:10])

def parse_published(entry):
    """
    Try to parse the published date from an RSS entry.
    """
    for key in ("published_parsed", "updated_parsed"):
        val = entry.get(key)
        if val:
            try:
                return datetime(*val[:6])
            except Exception:
                continue
    return None

def source_from_link(link: str):
    """
    Extract domain (netloc) from a URL to use as 'source'.
    """
    try:
        netloc = urlparse(link).netloc
    except Exception:
        netloc = ""
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc or "Unknown"

# ================== MAIN COLLECTION LOGIC ==================

def collect():
    """
    Main collector:
    - Clean old JSON files (> 2 days)
    - Load RSS sources
    - Fetch feeds and parse entries
    - Compute importance_score and category
    - Apply source weight
    - De-duplicate similar titles into 'topics'
    - Save JSON + classic TXT report
    """
    # هنا هنمسح الجيسون القديمة (أقدم من يومين)
    cleanup_old_files(days=2)

    sources = load_sources(SOURCES_FILE)
    print(f"[+] Loaded {len(sources)} RSS feeds")

    topics = {}
    scanned_count = 0

    for url in sources:
        print(f"\n[+] Fetching: {url}")
        feed = feedparser.parse(url)
        if feed.bozo:
            print("   ! Error parsing feed")
            continue

        # Limit per-feed to avoid huge volumes from a single source
        entries = feed.entries[:20]
        print(f"   Got {len(entries)} entries")

        for entry in entries:
            link = entry.get("link", "").strip()
            if not link:
                continue

            title = (entry.get("title") or "No title").strip()
            summary = (entry.get("summary") or entry.get("description") or "").strip()
            if isinstance(summary, list):
                # Some feeds may deliver summary as a list of dicts
                summary = summary[0].get("value", "") if summary else ""
            summary = summary or "No summary available"

            published_dt = parse_published(entry)
            cat = classify_category(f"{title}. {summary}")
            src = source_from_link(link)

            # Base importance from content + time
            s = importance_score(title, summary, published_dt)

            # Apply optional per-source weight
            weight = SOURCE_WEIGHTS.get(src, 1.0)
            s = int(s * weight)

            key = normalize_title(title)
            scanned_count += 1

            item = {
                "title": title,
                "summary": summary,
                "link": link,
                "published": published_dt.isoformat() if published_dt else entry.get("published", "Unknown"),
                "source": src,
                "category": cat,
                "importance_score": s,
                "also_covered_by": []
            }

            # De-duplicate topics
            if key not in topics:
                topics[key] = item
            else:
                existing = topics[key]
                if s > existing["importance_score"]:
                    item["also_covered_by"] = existing.get("also_covered_by", []) + [existing.get("source", "")]
                    topics[key] = item
                else:
                    existing.setdefault("also_covered_by", [])
                    if src not in existing["also_covered_by"]:
                        existing["also_covered_by"].append(src)

    all_news = sorted(topics.values(), key=lambda x: x["importance_score"], reverse=True)
    print(f"\n[+] Total scanned articles: {scanned_count}")
    print(f"[+] Unique topics after de-duplication: {len(all_news)}")

    if not all_news:
        print("No news collected, abort.")
        return

    # Save JSON file with all topics
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(all_news, f, ensure_ascii=False, indent=2)

    top7 = all_news[:7]

    # ================== CLASSIC TXT REPORT (UPGRADED) ==================

    def score_to_severity(score: int) -> str:
        """
        Map numeric score to severity label.
        """
        if score >= 2000:
            return "CRITICAL"
        if score >= 1400:
            return "HIGH"
        if score >= 800:
            return "MEDIUM"
        return "LOW"

    # Count severities for a small overview
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for item in all_news:
        sev = score_to_severity(item["importance_score"])
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # Map severity to a simple icon/keyword (text only, compatible with plain TXT)
    SEVERITY_ICON = {
        "CRITICAL": "Alert Triangle",
        "HIGH": "Shield Check",
        "MEDIUM": "Shield",
        "LOW": "Info"
    }

    # Optional: map some known sources to a short "type label"
    SOURCE_TYPE = {
        "thehackernews.com": "Newspaper",
        "krebsonsecurity.com": "Newspaper",
        "bleepingcomputer.com": "Newspaper",
        "securityweek.com": "Shield",
        "helpnetsecurity.com": "Shield",
        "thecyberexpress.com": "Link",
        "cyberscoop.com": "Link",
    }

    lines = []
    lines.append("CYBERBRIEF • DAILY THREAT INTELLIGENCE")
    lines.append(f"Generated: {datetime.utcnow().strftime('%A, %B %d, %Y - %H:%M')} UTC")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Total topics: {len(all_news)}    •    Scanned raw articles: {scanned_count}")
    lines.append("Severity breakdown:")
    lines.append(
        f"  CRITICAL: {severity_counts['CRITICAL']}  |  HIGH: {severity_counts['HIGH']}  |  "
        f"MEDIUM: {severity_counts['MEDIUM']}  |  LOW: {severity_counts['LOW']}"
    )
    lines.append("")
    lines.append("Top 7 active threats:")
    lines.append("")

    for idx, item in enumerate(top7, start=1):
        sev = score_to_severity(item["importance_score"])
        sev_icon = SEVERITY_ICON.get(sev, "Info")
        src = item["source"]
        src_type = SOURCE_TYPE.get(src, "News Site")
        title = item["title"]
        published = item.get("published", "Unknown")
        link = item["link"]
        category = item["category"]

        lines.append(f"{idx}. {sev_icon}  {src}  [{src_type}]")
        lines.append(f"   Title    : {title}")
        lines.append(f"   Category : {category}    •    Severity: {sev} (score: {item['importance_score']})")
        lines.append(f"   Published: {published}")
        lines.append(f"   Link     : {link}")

        if item.get("also_covered_by"):
            also = ", ".join(item["also_covered_by"])
            lines.append(f"   Also covered by: {also}")

        lines.append("")

    lines.append("Security Tips:")
    lines.append("• Never trust unsolicited links or attachments in email or messaging apps.")
    lines.append("• Enable multi-factor authentication (MFA) on email, banking, and admin accounts.")
    lines.append("• Keep browsers, VPNs, and endpoint security fully patched.")
    lines.append("")
    lines.append(f"Scanned {scanned_count} articles • Top 7 topics selected")
    lines.append("Next planned auto-update: 08:00 AM UTC")
    lines.append("Stay safe, stay sharp!")

    # Save TXT report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n[+] JSON saved  →", JSON_FILE)
    print("[+] Text report →", REPORT_FILE)
    print("[+] Done. Stay safe.")

# ================== ENTRY POINT ==================

if __name__ == "__main__":
    collect()
