import streamlit as st
import json
from datetime import date
import os

st.set_page_config(page_title="CYBERBRIEF", page_icon="Shield", layout="wide")

# === باك جراوند Matrix + لون احتياطي أسود-نيون (مش هيبوظ أبدًا) ===
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a001f, #001133);
        background-attachment: fixed;
    }
    .matrix-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        pointer-events: none;
        opacity: 0.4;
    }
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');
    
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 7rem;
        text-align: center;
        background: linear-gradient(90deg, #00ff9d, #00d0ff, #ff00ff, #ffff00, #00ff9d);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px #00ffff;
        animation: glow 4s ease-in-out infinite alternate;
    }
    @keyframes glow {from{filter:drop-shadow(0 0 20px #00ffff)} to{filter:drop-shadow(0 0 60px #ff00ff)}}
    
    .card {
        background: rgba(10,20,50,0.92);
        border-radius: 18px;
        padding: 22px;
        margin: 22px auto;
        max-width: 960px;
        border: 1px solid #00ffff;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 50px rgba(0,255,255,0.25);
        transition: all 0.4s;
        position: relative;
    }
    .card:hover {transform: translateY(-12px); box-shadow: 0 25px 70px rgba(0,255,255,0.5);}
    .rank {position:absolute;top:-10px;right:15px;background:#ff00ff;color:black;padding:8px 16px;border-radius:50px;font-weight:bold;font-size:1.1rem;box-shadow:0 0 30px #ff00ff;}
    .level {padding:6px 16px;border-radius:50px;font-weight:bold;font-size:0.9rem;}
    .critical {background:#ff0044; box-shadow:0 0 20px #ff0044; animation:pulse 2s infinite;}
    .high {background:#ff6600; box-shadow:0 0 15px #ff6600;}
    @keyframes pulse {50%{box-shadow:0 0 40px #ff0044}}
</style>

<!-- Matrix فيديو خفيف جدًا وسريع التحميل (مش هيبوظ) -->
<video class="matrix-overlay" autoplay muted loop playsinline>
  <source src="https://cdn.jsdelivr.net/gh/identor/matrix-bg/matrix.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# === الباقي زي ما هو ===
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;color:#00ffff;font-size:1.9rem;text-shadow:0 0 20px #00ffff'>Real-Time Global Threat Intelligence • Updated Daily</div>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#00ffff;margin:40px 0'>{date.today():%A, %B %d, %Y}</h4>", unsafe_allow_html=True)

today = date.today().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"
if not os.path.exists(json_file):
    st.error("تحديث تلقائي الساعة 8 صباحًا")
    st.stop()

with open(json_file, encoding="utf-8") as f:
    news = json.load(f)

CRITICAL = ["zero-day","cisa","rce","actively exploited","kev","ransomware","apt","fbi"]
def score(x):
    t = (x.get('title','') + ' ' + x.get('summary','')).lower()
    return len(t) + sum(w in t for w in CRITICAL)*300 + t.count("exploit")*100

top7 = sorted(news, key=score, reverse=True)[:7]
st.success(f"تم فحص **{len(news)}** حدث • أخطر **{len(top7)}** تهديدات اليوم")

for i, item in enumerate(top7):
    level = "critical" if any(k in item['title'].lower() for k in CRITICAL) else "high"
    txt = "CRITICAL" if level=="critical" else "HIGH"
    summary = (item.get('summary') or "")[:400] + ("..." if len(item.get('summary',''))>400 else "")
    source = item.get('link','').split('/')[2].replace('www.','').split('.')[0].title()

    st.markdown(f"""
    <div class="card">
        <div class="rank">#{i+1}</div>
        <span class="level {level}">{txt}</span>
        <h3 style="color:#00ffff;margin:12px 0">{item['title']}</h3>
        <p style="color:#00ff9d;font-weight:bold">Source: {source}</p>
        <p style="line-height:1.8;color:#e0e0e0">{summary}</p>
        <br>
        <a href="{item['link']}" target="_blank" style="color:#ff00ff;font-weight:bold;font-size:1.2rem;text-decoration:none">
            READ FULL REPORT →
        </a>
    </div><br>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:50px;color:#00ffff;font-family:Orbitron;font-size:1.6rem'>"
            "System Status: ONLINE • Next Update: 08:00 AM UTC</div>", unsafe_allow_html=True)
