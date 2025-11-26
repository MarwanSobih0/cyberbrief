import streamlit as st
import json
from datetime import date
import os

st.set_page_config(page_title="CYBERBRIEF", page_icon="Shield", layout="wide")

# ====== الباك جراوند السايبر اللي هيخلّي الكل يقول "ياااه" ======
st.markdown("""
<style>
    .stApp {
        background: #000;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(0, 255, 255, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 90% 80%, rgba(255, 0, 255, 0.15) 0%, transparent 20%),
            radial-gradient(circle at 50% 50%, rgba(0, 255, 150, 0.1) 0%, transparent 30%),
            url('https://i.ibb.co/HnY0Z8k/cyber-grid-final.jpg');
        background-size: cover;
        background-attachment: fixed;
    }
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');
    
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 7.5rem;
        text-align: center;
        background: linear-gradient(90deg, #00ffea, #00d0ff, #ff00ff, #ffff00, #00ffea);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 60px #00ffff;
        animation: glow 3s ease-in-out infinite alternate;
    }
    @keyframes glow { from {filter: drop-shadow(0 0 30px #00ffff)} to {filter: drop-shadow(0 0 80px #ff00ff)} }
    
    .subtitle {font-family: Rajdhani; font-size: 2rem; text-align: center; color: #00ffff; text-shadow: 0 0 25px #00ffff;}
    
    .card {
        background: rgba(8, 15, 40, 0.95);
        border-radius: 20px;
        padding: 24px;
        margin: 22px auto;
        max-width: 960px;
        border: 1px solid #00ffff;
        backdrop-filter: blur(16px);
        box-shadow: 0 15px 50px rgba(0, 255, 255, 0.3);
        transition: all 0.5s ease;
        position: relative;
        overflow: hidden;
    }
    .card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0, 255, 255, 0.6);
        border-color: #00ffff;
    }
    .rank {
        position: absolute;
        top: -12px; right: 16px;
        background: #ff00ff;
        color: black;
        padding: 9px 18px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 0 30px #ff00ff;
    }
    .level {
        padding: 7px 18px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 0.95rem;
        margin-bottom: 12px;
    }
    .critical {background:#ff0044; box-shadow:0 0 25px #ff0044; animation:pulse 2s infinite;}
    .high {background:#ff6600; box-shadow:0 0 18px #ff6600;}
    @keyframes pulse {50%{box-shadow:0 0 45px #ff0044}}
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-Time Global Threat Intelligence • Updated Daily</div>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#00ffff;margin:40px 0'>{date.today():%A, %B %d, %Y}</h4>", unsafe_allow_html=True)

# تحميل البيانات
today = date.today().strftime("%Y-%m-%d")
json_file = f"cybersecurity_news_{today}.json"

if not os.path.exists(json_file):
    st.error("تحديث تلقائي الساعة 8 صباحًا")
    st.stop()

with open(json_file, encoding="utf-8") as f:
    news = json.load(f)

# الترتيب
CRITICAL = ["zero-day","cisa","rce","actively exploited","kev","ransomware","apt","fbi"]
def score(x):
    t = (x.get('title','') + ' ' + x.get('summary','')).lower()
    return len(t) + sum(w in t for w in CRITICAL)*300

top7 = sorted(news, key=score, reverse=True)[:7]
st.success(f"تم فحص **{len(news)}** حدث • عرض أخطر **{len(top7)}** تهديدات")

for i, item in enumerate(top7):
    level = "critical" if any(k in item['title'].lower() for k in CRITICAL) else "high"
    txt = "CRITICAL" if level=="critical" else "HIGH"
    summary = (item.get('summary') or "")[:410] + ("..." if len(item.get('summary',''))>410 else "")
    source = item.get('link','').split('/')[2].replace('www.','').split('.')[0].title()

    st.markdown(f"""
    <div class="card">
        <div class="rank">#{i+1}</div>
        <span class="level {level}">{txt}</span>
        <h3 style="color:#00ffff;margin:12px 0">{item['title']}</h3>
        <p style="color:#00ff9d;font-weight:bold;margin:8px 0">Source: {source}</p>
        <p style="line-height:1.8;color:#e0e0e0">{summary}</p>
        <br>
        <a href="{item['link']}" target="_blank" style="color:#ff00ff;font-weight:bold;font-size:1.25rem;text-decoration:none">
            READ FULL REPORT →
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:60px;color:#00ffff;font-family:Orbitron;font-size:1.7rem'>"
            "System Status: ONLINE • Next Update: 08:00 AM UTC</div>", unsafe_allow_html=True)
