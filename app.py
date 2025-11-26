import streamlit as st
import json
from datetime import date
import os

# === Page Config ===
st.set_page_config(
    page_title="CYBERBRIEF • Daily Threat Intelligence",
    page_icon="Shield",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === Matrix-Style Animated Background Video ===
def set_background_video():
    video_url = "https://assets.mixkit.co/videos/preview/mixkit-matrix-style-binary-code-loop-2970-large.mp4"
    return f"""
    <video autoplay muted loop id="matrixBg" style="
        position: fixed;
        right: 0; bottom: 0;
        min-width: 100%; min-height: 100%;
        z-index: -1;
        opacity: 0.35;
        filter: hue-rotate(130deg);
    ">
        <source src="{video_url}" type="video/mp4">
    </video>
    """
st.markdown(set_background_video(), unsafe_allow_html=True)

# === Epic Cyberpunk CSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');

    .main {background: transparent !important;}
    
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 7rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #00ff9d, #00d0ff, #ff00ff, #ffff00, #00ff9d);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 4s ease-in-out infinite alternate, float 6s ease-in-out infinite;
        text-shadow: 0 0 40px #00ffff;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 20px #00ffff); }
        to   { filter: drop-shadow(0 0 60px #ff00ff); }
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-25px); }
    }
    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.9rem;
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 15px #00ffff;
        margin: -20px 0 10px 0;
    }
    .card {
        background: rgba(10, 20, 50, 0.75);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        border: 1px solid rgba(0, 255, 255, 0.4);
        backdrop-filter: blur(16px);
        transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    .card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0,255,255,0.3), transparent);
        transition: 0.8s;
    }
    .card:hover::before { left: 100%; }
    .card:hover {
        transform: translateY(-12px) scale(1.04);
        box-shadow: 0 30px 70px rgba(0, 255, 255, 0.5);
        border-color: #00ffff;
    }
    .rank {
        position: absolute;
        top: -12px; right: 18px;
        background: #ff00ff;
        color: black;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 50px;
        font-size: 1.4rem;
        box-shadow: 0 0 25px #ff00ff;
    }
    .level {
        padding: 6px 16px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.95rem;
        margin-bottom: 10px;
        display: inline-block;
    }
    .critical { background: #ff0044; box-shadow: 0 0 20px #ff0044; animation: pulse 2s infinite; }
    .high     { background: #ff6600; box-shadow: 0 0 15px #ff6600; }
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px #ff0044; }
        50% { box-shadow: 0 0 40px #ff0044; }
    }
</style>
""", unsafe_allow_html=True)

# === Hero Title ===
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-Time Global Threat Intelligence • Updated Daily • AI-Powered</p>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center; color:#00ffff; margin-bottom:30px;'>{date.today().strftime('%A, %B %d, %Y')}</h4>", unsafe_allow_html=True)
st.markdown("---")

# === Load Data ===
today = date.today().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"

if not os.path.exists(json_file):
    st.error("No threat data available yet. System updates automatically at 08:00 AM.")
    st.stop()

with open(json_file, 'r', encoding='utf-8') as f:
    news = json.load(f)

# === Smart Threat Scoring ===
CRITICAL_KEYWORDS = ["zero-day", "cisa", "rce", "actively exploited", "kev", "ransomware", "apt", "fbi", "critical vulnerability"]
HIGH_KEYWORDS = ["breach", "phishing", "malware", "exploit", "data leak", "supply chain", "attack"]

def calculate_threat_score(item):
    text = (item.get('title', '') + " " + item.get('summary', '')).lower()
    score = len(text)
    score += sum(kw in text for kw in CRITICAL_KEYWORDS) * 200
    score += sum(kw in text for kw in HIGH_KEYWORDS) * 80
    return score

top_threats = sorted(news, key=calculate_threat_score, reverse=True)[:7]

st.success(f"Scanned **{len(news)}** global cybersecurity events • Showing **Top {len(top_threats)} Active Threats**")

# === Function to get pretty source name from URL ===
def get_pretty_source(url):
    if not url:
        return "Unknown Source"
    try:
        domain = url.split('/')[2].replace('www.', '')
        name = domain.split('.')[0].lower()

        official_names = {
            'krebsonsecurity': 'Krebs on Security',
            'bleepingcomputer': 'BleepingComputer',
            'securityweek': 'SecurityWeek',
            'theregister': 'The Register',
            'darkreading': 'Dark Reading',
            'threatpost': 'Threatpost',
            'helpnetsecurity': 'Help Net Security',
            'gbhackers': 'GBHackers',
            'thecyberexpress': 'The Cyber Express',
            'cyberscoop': 'CyberScoop',
            'zdnet': 'ZDNet',
            'infosecurity-magazine': 'Infosecurity Magazine',
            'hackread': 'HackRead',
            'cybernews': 'Cybernews',
            'thehackernews': 'The Hacker News',
            'feedburner': 'FeedBurner',
        }
        return official_names.get(name, name.title())
    except:
        return "Unknown Source"

# === Display Threat Cards ===
for idx, threat in enumerate(top_threats):
    title_low = threat['title'].lower()
    summary = (threat.get('summary') or "No summary available")[:390]
    if len(threat.get('summary', '')) > 390:
        summary += "..."

    # Threat level
    if any(kw in title_low for kw in CRITICAL_KEYWORDS):
        level_class = "critical"
        level_text = "CRITICAL"
    elif any(kw in title_low for kw in HIGH_KEYWORDS):
        level_class = "high"
        level_text = "HIGH"
    else:
        level_class = "high"
        level_text = "ELEVATED"

    source_name = get_pretty_source(threat.get('link', ''))

    with st.container():
        cols = st.columns([1, 10, 1])
        with cols[1]:
            st.markdown(f"""
            <div class="card">
                <div class="rank">#{idx+1}</div>
                <span class="level {level_class}">{level_text}</span>
                <h3 style="color:#00ffff; margin:10px 0;">{threat['title']}</h3>
                <p style="opacity:0.9; font-size:1.1rem;">Source: <strong style="color:#00ff9d;">{source_name}</strong></p>
                <p style="line-height:1.75; color:#e0e0e0;">{summary}</p>
                <br>
                <a href="{threat['link']}" target="_blank" style="color:#ff00ff; font-weight:bold; font-size:1.2rem; text-decoration:none;">
                    READ FULL REPORT →
                </a>
            </div>
            """, unsafe_allow_html=True)

# === Epic Footer ===
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:40px; font-family:Orbitron; color:#00ffff;">
    <h2>System Status: ONLINE • Next Update: 08:00 AM UTC</h2>
    <p style="font-size:1.3rem; color:#ff00ff;">No Login • No Tracking • Pure Open-Source Intelligence</p>
    <p style="margin-top:20px; opacity:0.8;">Powered by Passion • Built by a Cybersecurity Professional</p>
</div>
""", unsafe_allow_html=True)