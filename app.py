import streamlit as st
import json
from datetime import date
import os

st.set_page_config(page_title="CYBERBRIEF", page_icon="🛡️", layout="wide")

# === الباك جراوند اللي مش هيبوظ أبدًا (Matrix أصلي + نيون) ===
st.markdown("""
<style>
    .stApp {background: #000 !important;}
    .matrix-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -2;
        pointer-events: none;
    }
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');
    
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 7rem;
        text-align: center;
        background: linear-gradient(90deg, #00ff9d, #00d0ff, #ff00ff, #ffff00);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 50px #00ffff;
        animation: float 6s ease-in-out infinite;
    }
    @keyframes float {0%,100%{transform:translateY(0)} 50%{transform:translateY(-20px)}}
    
    .subtitle {font-family:Rajdhani; font-size:1.9rem; text-align:center; color:#00ffff; text-shadow:0 0 20px #00ffff;}
    .card {
        background: rgba(10,20,50,0.92);
        border-radius: 18px;
        padding: 22px;
        margin: 20px auto;
        max-width: 950px;
        border: 1px solid #00ffff;
        backdrop-filter: blur(15px);
        box-shadow: 0 10px 40px rgba(0,255,255,0.3);
        transition: all 0.4s;
        position: relative;
        overflow: hidden;
    }
    .card:hover {transform: translateY(-10px); box-shadow: 0 25px 60px rgba(0,255,255,0.5);}
    .rank {
        position: absolute;
        top: -10px; right: 15px;
        background: #ff00ff;
        color: black;
        padding: 8px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.1rem;
        box-shadow: 0 0 25px #ff00ff;
    }
    .level {
        padding: 6px 15px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 12px;
        display: inline-block;
    }
    .critical {background:#ff0044; box-shadow:0 0 20px #ff0044; animation:pulse 2s infinite;}
    .high {background:#ff6600; box-shadow:0 0 15px #ff6600;}
    @keyframes pulse {50%{box-shadow:0 0 35px #ff0044}}
</style>

<video class="matrix-bg" autoplay muted loop playsinline>
  <source src="https://assets.mixkit.co/videos/preview/mixkit-matrix-style-binary-code-loop-2970-large.mp4" type="video/mp4">
</video>
""", unsafe_allow_html=True)

# === العنوان الفخم ===
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Real-Time Global Threat Intelligence • Updated Daily</p>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#00ffff;margin:30px 0'>{date.today():%A, %B %d, %Y}</h4>", unsafe_allow_html=True)

# === تحميل البيانات ===
today = date.today().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"

if not os.path.exists(json_file):
    st.error("تحديث يومي تلقائي الساعة 8 صباحًا")
    st.stop()

with open(json_file, encoding="utf-8") as f:
    news = json.load(f)

# === الترتيب حسب الخطورة ===
CRITICAL = ["zero-day","cisa","rce","actively exploited","kev","ransomware","apt"]
def score(x):
    t = (x.get('title','') + ' ' + x.get('summary','')).lower()
    return len(t) + sum(w in t for w in CRITICAL)*300 + t.count("exploit")*100

top7 = sorted(news, key=score, reverse=True)[:7]
st.success(f"تم فحص **{len(news)}** حدث • عرض أخطر **{len(top7)}** تهديدات")

for i, item in enumerate(top7):
    level = "critical" if any(k in item['title'].lower() for k in CRITICAL) else "high"
    txt = "CRITICAL" if level=="critical" else "HIGH"
    summary = (item.get('summary') or "")[:400] + ("..." if len(item.get('summary',''))>400 else "")
    
    st.markdown(f"""
    <div class="card">
        <div class="rank">#{i+1}</div>
        <span class="level {level}">{txt}</span>
        <h3 style="color:#00ffff;margin:10px 0">{item['title']}</h3>
        <p style="color:#00ff9d;font-weight:bold;margin:8px 0">
            Source: {item.get('link','').split('/')[2].replace('www.','').split('.')[0].title()}
        </p>
        <p style="line-height:1.8;color:#e0e0e0">{summary}</p>
        <br>
        <a href="{item['link']}" target="_blank" style="color:#ff00ff;font-weight:bold;font-size:1.2rem;text-decoration:none">
            READ FULL REPORT →
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:50px;color:#00ffff;font-family:Orbitron;font-size:1.5rem'>"
            "System Status: ONLINE • Next Update: 08:00 AM UTC</div>", unsafe_allow_html=True)
