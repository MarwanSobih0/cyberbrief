import streamlit as st
import json
import os
from datetime import datetime
from glob import glob
import pandas as pd
import re
from urllib.parse import urlparse

# Configure Streamlit page
st.set_page_config(page_title="CYBERBRIEF", page_icon="🛡️", layout="wide")

# ================== GLOBAL STYLE (CSS / UI THEME) ==================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Rajdhani:wght@500;700&display=swap');

.stApp {
    background: radial-gradient(circle at 0% 0%, #001a33 0, #000814 40%, #00010f 100%);
    color: #f5f5f5;
}

/* HEADER */

.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.2rem;
    text-align: center;
    letter-spacing: 0.25rem;
    background: linear-gradient(90deg,#00e0ff,#ff00ff);
    -webkit-background-clip: text;
    color: transparent;
    text-shadow: 0 0 25px rgba(0,224,255,0.5);
    margin-bottom: 0.1rem;
    margin-top: 0.3rem;
}

.main-subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    text-align: center;
    color: #b3ecff;
    margin-bottom: 1.0rem;
}

.news-date {
    text-align: center;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.9rem;
    color: #8be9ff;
    margin-bottom: 0.8rem;
}

/* TOP ALERT BAR */

.top-alert {
    position: fixed;
    top: 0; left: 0; right: 0;
    background: linear-gradient(90deg,#ff0055,#ff7700);
    color: white;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    text-align: center;
    padding: 0.35rem 1rem;
    z-index: 1000;
    box-shadow: 0 0 30px rgba(255,0,85,0.8);
}

/* METRIC CARDS */

.metric-card {
    border-radius: 0.9rem;
    padding: 0.8rem 1rem;
    background: linear-gradient(145deg,rgba(0,0,0,0.85),rgba(0,40,80,0.92));
    border: 1px solid rgba(0,255,255,0.25);
    box-shadow: 0 12px 26px rgba(0,0,0,0.8);
}

.metric-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    color: #a0aec0;
    letter-spacing: 0.08em;
}

.metric-value {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.7rem;
    color: #00e0ff;
}

.metric-extra {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.8rem;
    color: #cbd5f5;
    margin-top: 0.3rem;
}

/* THREAT PILL */

.threat-pill {
    display: inline-block;
    padding: 0.15rem 0.55rem;
    border-radius: 1000px;
    font-size: 0.75rem;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 0.08em;
    border: 1px solid rgba(255,255,255,0.3);
    margin-top: 0.35rem;
}

.threat-low {
    background: rgba(0,255,120,0.08);
    border-color: rgba(0,255,120,0.6);
    color: #7CFFB2;
    box-shadow: 0 0 12px rgba(0,255,120,0.35);
}
.threat-medium {
    background: rgba(0,210,255,0.08);
    border-color: rgba(0,210,255,0.7);
    color: #7AD8FF;
    box-shadow: 0 0 12px rgba(0,210,255,0.35);
}
.threat-high {
    background: rgba(255,170,0,0.1);
    border-color: rgba(255,170,0,0.9);
    color: #FFD27F;
    box-shadow: 0 0 14px rgba(255,170,0,0.5);
}
.threat-critical {
    background: rgba(255,0,90,0.12);
    border-color: rgba(255,0,90,0.95);
    color: #FF99C2;
    box-shadow: 0 0 16px rgba(255,0,90,0.7);
}

/* NEWS CARDS – smaller & cleaner */

.news-card {
    position: relative;
    border-radius: 0.9rem;
    padding: 0.9rem 1rem 0.8rem 1rem;
    margin-bottom: 0.7rem;
    background: radial-gradient(circle at 0% 0%,rgba(0,255,255,0.08),transparent 45%),
                radial-gradient(circle at 100% 100%,rgba(255,0,255,0.10),transparent 50%),
                rgba(10,10,20,0.96);
    border: 1px solid rgba(0,255,255,0.18);
    box-shadow: 0 8px 18px rgba(0,0,0,0.7);
    overflow: hidden;
}

/* rank badge – moved to RIGHT */

.news-rank {
    position: absolute;
    top: 0.45rem;
    right: 0.9rem;
    background: #020617;
    color: #22d3ee;
    border: 1px solid #22d3ee;
    padding: 0.05rem 0.55rem;
    border-radius: 999px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    box-shadow: 0 0 10px rgba(34,211,238,0.6);
    z-index: 5;
    text-align: right;
}

.news-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.05rem;
    color: #e6f6ff;
    margin-bottom: 0.2rem;
    margin-left: 0.2rem;
    margin-top: 0.2rem;
}

.news-meta {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.8rem;
    color: #9ae6ff;
    margin-bottom: 0.25rem;
    margin-left: 0.2rem;
}

/* small favicon icon (image) for each source */

.source-icon {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    margin-right: 6px;
    vertical-align: middle;
}

.news-summary {
    font-size: 0.85rem;
    line-height: 1.5;
    color: #e2e8f0;
    margin-left: 0.2rem;
    margin-right: 0.2rem;
}

.news-footer {
    margin-top: 0.6rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-left: 0.2rem;
    margin-right: 0.2rem;
}

/* زر فتح الخبر الأصلي */

.btn-link {
    display: inline-block;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: #0ea5e9;
    text-decoration: none;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    border: 1px solid rgba(56,189,248,0.7);
    background: rgba(15,23,42,0.9);
}
.btn-link:hover {
    background: rgba(56,189,248,0.1);
}

.btn-bookmark {
    font-size: 0.8rem;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.35);
    background: transparent;
    color: #f5f5f5;
}
.btn-bookmark:hover {
    background: rgba(255,255,255,0.1);
}

.chip {
    display:inline-block;
    padding:0.15rem 0.6rem;
    border-radius:999px;
    font-size:0.7rem;
    border:1px solid rgba(148,163,184,0.9);
    color:#cbd5f5;
    margin-right:0.25rem;
    margin-top:0.2rem;
}

.learning-box {
    border-radius: 1.0rem;
    padding: 0.9rem 1.0rem;
    background: rgba(8,47,73,0.85);
    border: 1px solid rgba(56,189,248,0.7);
    margin-bottom: 0.7rem;
}

.small-muted {
    font-size: 0.8rem;
    color: #94a3b8;
}
</style>
    """,
    unsafe_allow_html=True,
)

# ================== DATA LOADING HELPERS ==================

def find_latest_news_file(pattern: str = "cybersecurity_news_*.json"):
    """Find the most recent news JSON file based on the date in the filename."""
    files = glob(pattern)
    if not files:
        return None, None

    def extract_date(fname: str):
        try:
            d = fname.split("_")[-1].replace(".json", "")
            return datetime.strptime(d, "%Y-%m-%d").date()
        except Exception:
            return datetime.min.date()

    latest = max(files, key=extract_date)
    return latest, extract_date(latest)


def classify_category(text: str) -> str:
    """Simple keyword-based classifier to assign a high-level category."""
    t = text.lower()
    if any(w in t for w in ["ransomware","locker","encrypt","decryptor"]):
        return "Ransomware"
    if any(w in t for w in ["data breach","leak","database exposed","records exposed","stolen data"]):
        return "Data Breach"
    if any(w in t for w in ["cve-","vulnerability","zero-day","remote code execution","rce","privilege escalation"]):
        return "Vulnerability"
    if any(w in t for w in ["phishing","smishing","vishing","scam","fraud","social engineering"]):
        return "Phishing / Scams"
    if any(w in t for w in ["regulation","law","bill","compliance","gdpr","fine","penalty"]):
        return "Policy / Law"
    if any(w in t for w in [" ai "," llm ","model","neural network","machine learning"]):
        return "AI & Security"
    if any(w in t for w in ["critical infrastructure","power grid","pipeline","hospital","water plant"]):
        return "Critical Infrastructure"
    return "Other"


def fallback_score(item: dict) -> int:
    """Compute an importance score if JSON doesn't have 'importance_score'."""
    title = item.get("title","")
    summary = item.get("summary","")
    text = (title + " " + summary).lower()

    base = min(len(summary), 800) // 4
    score = base

    for word in ["zero-day","0-day","actively exploited","rce","remote code execution"]:
        if word in text:
            score += 600

    for word in ["ransomware","data breach","extortion","supply chain attack"]:
        if word in text:
            score += 450

    for word in ["phishing","smishing","malware","spyware","token theft","account takeover"]:
        if word in text:
            score += 250

    for marker in ["cisa","fbi","nsa","microsoft","google","apple"]:
        if marker in text:
            score += 150

    return score


def strip_html_tags(text: str) -> str:
    """Remove HTML tags from text (to avoid showing <div>… ككود)."""
    if not text:
        return ""
    # لو في كارت قديم متخزن جوه الـ summary نقطع من أول الـ footer
    text = text.split('<div class="news-footer">')[0]
    clean = re.sub(r"<[^>]+>", "", text)
    clean = re.sub(r"\s+", " ", clean)
    return clean.strip()


def prepare_news():
    """Load latest JSON + ensure each item has category + importance_score."""
    fname, fdate = find_latest_news_file()
    if not fname:
        st.error("No news data found. Run the collector script first.")
        st.stop()

    with open(fname, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        st.error("Invalid news JSON format (expected a list of items).")
        st.stop()

    for item in data:
        # handle old JSON keys (source_name, domain...)
        if "source" not in item:
            src = item.get("source_name") or item.get("domain") or "Unknown"
            item["source"] = src

        if "category" not in item:
            item["category"] = classify_category(
                f"{item.get('title','')}. {item.get('summary','')}"
            )
        if "importance_score" not in item:
            item["importance_score"] = fallback_score(item)

    return data, fdate, fname


news, news_date, news_file = prepare_news()

# ================== THREAT LEVEL & STATS ==================

def score_to_level(score: int):
    """Map numeric score to (label, css_class)."""
    if score >= 2000:
        return "CRITICAL", "threat-critical"
    if score >= 1400:
        return "HIGH", "threat-high"
    if score >= 800:
        return "MEDIUM", "threat-medium"
    return "LOW", "threat-low"


max_score = max(item.get("importance_score",0) for item in news) if news else 0
threat_label, threat_css = score_to_level(max_score)

category_counts = {}
for item in news:
    cat = item.get("category","Other")
    category_counts[cat] = category_counts.get(cat, 0) + 1

# ================== TOP ALERT BAR ==================

st.markdown(
    f"<div class='top-alert'>AUTO UPDATE TARGET: 08:00 PM LOCAL • CURRENT SNAPSHOT: {news_date.isoformat()}</div>",
    unsafe_allow_html=True,
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ================== HEADER ==================

st.markdown("<div class='main-title'>CYBERBRIEF</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Daily Cybersecurity Brief • Curated Threat Intelligence</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='news-date'>Data snapshot: {news_date.strftime('%A %d %B %Y')}</div>",
    unsafe_allow_html=True,
)

# ================== SIDEBAR CONTROLS ==================

all_categories = sorted({item.get("category","Other") for item in news})
default_cats = all_categories.copy()

with st.sidebar:
    st.markdown("### ⚙️ Display controls")

    view_mode = st.radio(
        "Main view mode",
        ["Top Threats", "All News", "Simple Mode"],
        index=0,
    )

    st.markdown("---")

    selected_categories = st.multiselect(
        "Filter by category",
        options=all_categories,
        default=default_cats,
    )

    search_query = st.text_input("Search in title / summary / source", "")

    st.markdown("---")

    severity_filter = st.multiselect(
        "Filter by severity level",
        options=["CRITICAL","HIGH","MEDIUM","LOW"],
        default=["CRITICAL","HIGH","MEDIUM","LOW"],
    )

    top_n = st.slider("Number of items in Top Threats view", 3, 15, 7)

    st.markdown("---")
    st.markdown(f"**Data file:** `{os.path.basename(news_file)}`")
    st.markdown(f"**Total stories:** `{len(news)}`")

# ================== METRICS ROW ==================

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-label">TOPICS TODAY</div>
    <div class="metric-value">{len(news)}</div>
    <div class="metric-extra">Unique stories in this snapshot</div>
</div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-label">ACTIVE CATEGORIES</div>
    <div class="metric-value">{len(all_categories)}</div>
    <div class="metric-extra">{", ".join(all_categories)}</div>
</div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f"""
<div class="metric-card">
    <div class="metric-label">THREAT LEVEL</div>
    <div class="metric-value">{threat_label}</div>
    <span class="threat-pill {threat_css}">CURRENT SNAPSHOT</span>
    <div class="metric-extra">Based on the highest severity story</div>
</div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ================== FILTER LOGIC ==================

def item_level(item):
    label, _css = score_to_level(item.get("importance_score",0))
    return label


def filter_items(items):
    filtered = []
    q = search_query.strip().lower()

    for it in items:
        cat = it.get("category","Other")
        if cat not in selected_categories:
            continue

        lvl = item_level(it)
        if lvl not in severity_filter:
            continue

        if q:
            text = " ".join(
                [
                    it.get("title",""),
                    it.get("summary",""),
                    it.get("source",""),
                    it.get("category",""),
                ]
            ).lower()
            if q not in text:
                continue

        filtered.append(it)

    return filtered


filtered_news = filter_items(news)

# ================== BOOKMARK SUPPORT ==================

if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = []


def make_item_id(item):
    return item.get("link") or item.get("title") or str(item.get("importance_score",""))


def toggle_bookmark(item):
    item_id = make_item_id(item)
    bookmarks = st.session_state["bookmarks"]

    if any(b["id"] == item_id for b in bookmarks):
        st.session_state["bookmarks"] = [b for b in bookmarks if b["id"] != item_id]
    else:
        st.session_state["bookmarks"].append(
            {
                "id": item_id,
                "title": item.get("title",""),
                "source": item.get("source",""),
                "link": item.get("link",""),
                "category": item.get("category",""),
                "importance_score": item.get("importance_score",0),
                "summary": item.get("summary",""),
                "domain": item.get("domain",""),
            }
        )


def is_bookmarked(item):
    item_id = make_item_id(item)
    return any(b["id"] == item_id for b in st.session_state["bookmarks"])

# ================== SIMPLE EXPLAINER ==================

def simple_explainer(item):
    cat = item.get("category","Other")
    mapping = {
        "Ransomware": "Malware that encrypts victim files and demands a ransom (often crypto) to decrypt.",
        "Data Breach": "Unauthorized access or leak of a database containing sensitive information.",
        "Vulnerability": "Security flaw in software or systems that attackers can exploit if not patched.",
        "Phishing / Scams": "Fake emails/sites/messages trying to trick you into giving passwords or OTP codes.",
        "Policy / Law": "New regulations, legal actions, or fines related to cybersecurity and data privacy.",
        "AI & Security": "Use or abuse of AI models in cyber attacks or defensive security.",
        "Critical Infrastructure": "Attacks targeting essential services like energy, water, hospitals or transport."
    }
    return mapping.get(cat, "Cybersecurity-related story in a general category.")

# favicon helper
def get_domain(item):
    dom = item.get("domain")
    if dom:
        return dom
    link = item.get("link","")
    if not link:
        return ""
    netloc = urlparse(link).netloc
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc

# ================== TABS LAYOUT ==================

tab_feed, tab_dashboard, tab_bookmarks, tab_learning = st.tabs(
    ["📰 News Feed", "📊 Dashboard", "⭐ Bookmarks", "📚 Learning Mode"]
)

# ---------- TAB: News Feed ----------
with tab_feed:
    if not filtered_news:
        st.warning("No results match the current filters / search.")
    else:
        if view_mode == "Top Threats":
            items = sorted(filtered_news, key=lambda x: x.get("importance_score",0), reverse=True)[:top_n]
        else:
            items = sorted(filtered_news, key=lambda x: x.get("importance_score",0), reverse=True)

        for idx, item in enumerate(items, start=1):
            lbl, css = score_to_level(item.get("importance_score",0))
            source = item.get("source","Unknown")
            category = item.get("category","Other")

            raw_summary = item.get("summary","") or ""
            clean_summary = strip_html_tags(raw_summary)
            summary_short = clean_summary if len(clean_summary) <= 520 else clean_summary[:520] + "…"

            link = item.get("link","#")
            bookmarked = is_bookmarked(item)

            dom = get_domain(item)
            favicon_url = f"https://www.google.com/s2/favicons?domain={dom}&sz=64" if dom else ""
            icon_html = f"<img class='source-icon' src='{favicon_url}' alt='icon' />" if favicon_url else ""

            extra = ""
            if view_mode == "Simple Mode":
                extra = f"<br><br><span class='small-muted'><b>Simple explanation:</b> {simple_explainer(item)}</span>"

            card_html = f"""
<div class="news-card">
<div class="news-rank">#{idx}</div>
<div class="news-title">{item.get('title','')}</div>
<div class="news-meta">
{icon_html}Source: <b>{source}</b> • Category: <b>{category}</b> • Severity:
<span class="threat-pill {css}">{lbl}</span>
</div>
<div class="news-summary">
{summary_short}
{extra}
</div>
<div class="news-footer">
<a class="btn-link" href="{link}" target="_blank">🔗 Open full article</a>
<span><span class="chip">Score: {item.get('importance_score',0)}</span></span>
</div>
</div>
            """

            st.markdown(card_html, unsafe_allow_html=True)

            bm_label = "★ Remove bookmark" if bookmarked else "☆ Add to bookmarks"
            if st.button(bm_label, key=f"bm_{idx}"):
                toggle_bookmark(item)

# ---------- TAB: Dashboard ----------
with tab_dashboard:
    st.subheader("Threat landscape overview")
    st.write("Quick view of how today's stories are distributed by category and severity.")

    if category_counts:
        df_cat = pd.DataFrame(
            {"Category": list(category_counts.keys()), "Count": list(category_counts.values())}
        ).sort_values("Count", ascending=False)
        st.bar_chart(df_cat.set_index("Category"))
    else:
        st.info("No category distribution available.")

    levels_map = {"LOW":0,"MEDIUM":0,"HIGH":0,"CRITICAL":0}
    for it in news:
        lvl = item_level(it)
        levels_map[lvl] = levels_map.get(lvl,0) + 1

    df_lvl = pd.DataFrame(
        {"Level": list(levels_map.keys()), "Count": list(levels_map.values())}
    ).sort_values("Count", ascending=False)
    st.bar_chart(df_lvl.set_index("Level"))

    st.markdown("### Reading tips")
    st.markdown(
        "- A spike in **Ransomware** stories can indicate high activity from ransomware gangs.\n"
        "- Many **Vulnerabilities** with high scores means patch management needs to be fast and strict.\n"
        "- If there is even one **CRITICAL**-level story, it's worth reading carefully and checking impact on you/your org."
    )

# ---------- TAB: Bookmarks ----------
with tab_bookmarks:
    st.subheader("Your bookmarked stories")
    bookmarks = st.session_state.get("bookmarks", [])
    if not bookmarks:
        st.info("You have no bookmarked stories yet. Use **Add to bookmarks** in the News Feed tab.")
    else:
        for idx, item in enumerate(bookmarks, start=1):
            lbl, css = score_to_level(item.get("importance_score",0))

            raw_summary = item.get("summary","") or ""
            clean_summary = strip_html_tags(raw_summary)
            summary_short = clean_summary if len(clean_summary) <= 360 else clean_summary[:360] + "…"

            link = item.get("link","#")

            dom = item.get("domain") or get_domain(item)
            favicon_url = f"https://www.google.com/s2/favicons?domain={dom}&sz=64" if dom else ""
            icon_html = f"<img class='source-icon' src='{favicon_url}' alt='icon' />" if favicon_url else ""

            card_html = f"""
<div class="news-card">
<div class="news-rank">#{idx}</div>
<div class="news-title">{item.get('title','')}</div>
<div class="news-meta">
{icon_html}Source: <b>{item.get('source','Unknown')}</b> • Category: <b>{item.get('category','Other')}</b> • Severity:
<span class="threat-pill {css}">{lbl}</span>
</div>
<div class="news-summary">
{summary_short}
</div>
<div class="news-footer">
<a class="btn-link" href="{link}" target="_blank">🔗 Open full article</a>
<span class="chip">Score: {item.get('importance_score',0)}</span>
</div>
</div>
            """

            st.markdown(card_html, unsafe_allow_html=True)

            if st.button("🗑 Remove", key=f"rm_{idx}"):
                st.session_state["bookmarks"] = [
                    b for b in bookmarks if b["id"] != item["id"]
                ]
                st.experimental_rerun()

# ---------- TAB: Learning ----------
with tab_learning:
    st.subheader("Learning mode")
    st.write(
        "Use this tab to build your cybersecurity vocabulary and get used to reading threat intel stories."
    )

    st.markdown("### Glossary")
    terms = {
        "Ransomware": "Malicious software that encrypts your files and demands a ransom to restore access.",
        "Zero-day": "A vulnerability that is unknown or unpatched, sometimes actively exploited in the wild.",
        "Data Breach": "Leak or theft of sensitive data from a company or service (emails, passwords, card numbers...).",
        "Phishing": "Fake messages or websites impersonating trusted brands to steal your credentials.",
        "CISA / FBI alert": "Official advisories from government agencies about active and serious threats.",
        "Patch": "A security update that fixes a vulnerability.",
    }
    for k, v in terms.items():
        st.markdown(f"**{k}** — {v}")

    st.markdown("### Based on today's feed")
    seen_cats = {item.get("category","Other") for item in news}
    for cat in sorted(seen_cats):
        st.markdown(
            f"""
<div class="learning-box">
    <b>{cat}</b><br>
    <span class="small-muted">{simple_explainer({'category': cat})}</span>
</div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "<p class='small-muted'>Tip: every day, try to read at least one full story and ask yourself: "
        "who is affected, what type of attack is it, and how could it be prevented?</p>",
        unsafe_allow_html=True,
    )
