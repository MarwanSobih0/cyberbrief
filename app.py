import streamlit as st
import json
from datetime import date
import os

st.set_page_config(page_title="CYBERBRIEF", page_icon="Shield", layout="wide")

# ================== الشكل اللي هيخطف الأنفاس ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap');

    /* باك جراوند سايبر خالص بدون صور خارجية */
    .stApp {
        background: #0a001f;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 40px, rgba(0,255,255,0.04) 40px, rgba(0,255,255,0.04) 80px),
            repeating-linear-gradient(-45deg, transparent, transparent 40px, rgba(255,0,255,0.04) 40px, rgba(255,0,255,0.04) 80px),
            radial-gradient(circle at 20% 80%, rgba(0,255,255,0.25), transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255,0,255,0.25), transparent 50%),
            linear-gradient(to bottom, #0a001f, #001233);
        background-attachment: fixed;
    }

    /* العنوان اللي هيولع */
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 8.5rem;
        text-align: center;
        background: linear-gradient(90deg, #00ffff, #00ff9d, #ff00ff, #ffff00, #00ffff);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 80px #00ffff, 0 0 120px #ff00ff;
        animation: neonPulse 3s ease-in-out infinite alternate;
        margin-bottom: 0;
    }
    @keyframes neonPulse {
        from { text-shadow: 0 0 40px #00ffff, 0 0 80px #00ffff; }
        to   { text-shadow: 0 0 80px #ff00ff, 0 0 160px #ff00ff; }
    }

    .subtitle {
        font-family: 'Rajdhani', sans-serif;
        font-size: 2.2rem;
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 30px #00ffff;
        margin: 10px 0 40px 0;
    }

    /* الخط الأحمر البارز فوق كل حاجة */
    .alert-bar {
        position: fixed;
        top: 0; left: 0; right: 0;
        background: linear-gradient(90deg, #ff0044, #ff0066);
        color: white;
        text-align: center;
        padding: 12px 20px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.4rem;
        font-weight: bold;
        z-index: 9999;
        box-shadow: 0 0 40px #ff0044;
        animation: alertGlow 2s infinite alternate;
        letter-spacing: 2px;
    }
    @keyframes alertGlow {
        from { box-shadow: 0 0 20px #ff0044; }
        to   { box-shadow: 0 0 60px #ff0044; }
    }

    /* أيقونات متحركة في الخلفية */
    .floating-icons {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 1;
        overflow: hidden;
    }
    .icon {
        position: absolute;
        font-size: 2.5rem;
        opacity: 0.3;
        animation: float 15s infinite linear;
        color: #00ffff;
        text-shadow: 0 0 20px #00ffff;
    }
    @keyframes float {
        0%   { transform: translateY(100vh) rotate(0deg); }
        100% { transform: translateY(-100px) rotate(360deg); }
    }

    /* الكروت الفخمة */
    .card {
        background: rgba(10, 25, 70, 0.95);
        border-radius: 24px;
        padding: 28px;
        margin: 30px auto;
        max-width: 1000px;
        border: 2px solid #00ffff;
        backdrop-filter: blur(20px);
        box-shadow: 0 20px 70px rgba(0,255,255,0.4);
        transition: all 0.6s ease;
        position: relative;
        overflow: hidden;
    }
    .card:hover {
        transform: translateY(-20px) scale(1.04);
        box-shadow: 0 40px 100px rgba(0,255,255,0.8);
        border-color: #00ffff;
    }
    .rank {
        position: absolute;
        top: -16px; right: 20px;
        background: #ff00ff;
        color: black;
        padding: 12px 24px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.5rem;
        box-shadow: 0 0 50px #ff00ff;
        animation: rankPulse 2s infinite;
    }
    @keyframes rankPulse { 50% { transform: scale(1.15); } }

    .level {
        padding: 10px 24px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .critical {background:#ff0044; box-shadow:0 0 40px #ff0044; animation:glowRed 1.5s infinite alternate;}
    @keyframes glowRed { to { box-shadow:0 0 80px #ff0044; } }
</style>

<!-- الخط الأحمر البارز -->
<div class="alert-bar">
    AUTOMATIC UPDATE AT 08:00 AM UTC • NO DATA AVAILABLE YET
</div>

<!-- أيقونات متحركة في الخلفية -->
<div class="floating-icons">
    <div class="icon" style="left:10%;animation-delay:0s;">Shield</div>
    <div class="icon" style="left:20%;animation-delay:3s;">Bomb</div>
    <div class="icon" style="left:35%;animation-delay:6s;">Laptop</div>
    <div class="icon" style="left:50%;animation-delay:1s;">Bug</div>
    <div class="icon" style="left:65%;animation-delay:8s;">Virus</div>
    <div class="icon" style="left:80%;animation-delay:4s;">Code</div>
    <div class="icon" style="left:90%;animation-delay:7s;">Terminal</div>
</div>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-Time Global Threat Intelligence • Updated Daily</div>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#00ffff;margin:60px 0'>{date.today():%A, %B %d, %Y}</h4>", unsafe_allow_html=True)

# البيانات
today = date.today().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"

if not os.path.exists(json_file):
    st.stop()

with open(json_file, encoding="utf-8") as f:
    news = json.load(f)

CRITICAL = ["zero-day","cisa","rce","actively exploited","kev","ransomware","apt","fbi"]
def score(x):
    t = (x.get('title','') + ' ' + x.get('summary','')).lower()
    return len(t) + sum(w in t for w in CRITICAL)*400

top7 = sorted(news, key=score, reverse=True)[:7]
st.success(f"Scanned **{len(news)}** Global Events • Top {len(top7)} Active Threats Today")

for i, item in enumerate(top7):
    level = "critical" if any(k in item['title'].lower() for k in CRITICAL) else "high"
    txt = "CRITICAL" if level=="critical" else "HIGH"
    summary = (item.get('summary') or "")[:430] + ("..." if len(item.get('summary',''))>430 else "")
    source = item.get('link','').split('/')[2].replace('www.','').split('.')[0].title()

    st.markdown(f"""
    <div class="card">
        <div class="rank">#{i+1}</div>
        <span class="level {level}">{txt}</span>
        <h3 style="color:#00ffff;margin:15px 0;font-size:2rem">{item['title']}</h3>
        <p style="color:#00ffea;font-weight:bold;font-size:1.3rem">Source: {source}</p>
        <p style="line-height:1.9;color:#e8e8e8;font-size:1.2rem">{summary}</p>
        <br>
        <a href="{item['link']}" target="_blank" style="color:#ff00ff;font-weight:bold;font-size:1.5rem;text-decoration:none">
            READ FULL REPORT →
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:80px;color:#00ffff;font-family:Orbitron;font-size:2rem'>"
            "System Status: ONLINE • Next Update: 08:00 AM UTC</div>", unsafe_allow_html=True)
