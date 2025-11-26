import streamlit as st
import json
from datetime import date
import os

st.set_page_config(page_title="CYBERBRIEF", page_icon="Shield", layout="wide")

# ====== باك جراوند سايبر خرافي بدون أي صور خارجية (يشتغل في مصر 100%) ======
st.markdown("""
<style>
    .stApp {
        background: #000814;
        background-image: 
            repeating-linear-gradient(45deg, transparent, transparent 35px, rgba(0,255,255,0.03) 35px, rgba(0,255,255,0.03) 70px),
            repeating-linear-gradient(-45deg, transparent, transparent 35px, rgba(255,0,255,0.03) 35px, rgba(255,0,255,0.03) 70px),
            radial-gradient(circle at 20% 80%, rgba(0,255,255,0.2), transparent 40%),
            radial-gradient(circle at 80% 20%, rgba(255,0,255,0.2), transparent 40%),
            linear-gradient(to bottom, #000814, #001d3d);
        background-attachment: fixed;
    }
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600&display=swap');
    
    .title {
        font-family: 'Orbitron', sans-serif;
        font-size: 7.5rem;
        text-align: center;
        background: linear-gradient(90deg, #00ffea, #00d4ff, #ff00ff, #ffff00, #00ffea);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 70px #00ffff;
        animation: neon 3s ease-in-out infinite alternate;
    }
    @keyframes neon {
        from { text-shadow: 0 0 20px #00ffff, 0 0 40px #00ffff; }
        to   { text-shadow: 0 0 40px #ff00ff, 0 0 80px #ff00ff; }
    }
    
    .subtitle {
        font-family: Rajdhani, sans-serif;
        font-size: 2rem;
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 30px #00ffff;
        margin: -20px 0 40px 0;
    }
    
    .card {
        background: rgba(10, 25, 60, 0.95);
        border-radius: 22px;
        padding: 26px;
        margin: 25px auto;
        max-width: 980px;
        border: 2px solid #00ffff;
        backdrop-filter: blur(18px);
        box-shadow: 0 20px 60px rgba(0, 255, 255, 0.4);
        transition: all 0.5s ease;
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
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 40px 90px rgba(0, 255, 255, 0.7);
        border-color: #00ffff;
    }
    
    .rank {
        position: absolute;
        top: -14px; right: 18px;
        background: #ff00ff;
        color: black;
        padding: 10px 20px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1.3rem;
        box-shadow: 0 0 40px #ff00ff;
    }
    .level {
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    .critical {background:#ff0044; box-shadow:0 0 30px #ff0044; animation:pulse 2s infinite;}
    .high     {background:#ff6600; box-shadow:0 0 20px #ff6600;}
    @keyframes pulse {50%{box-shadow:0 0 50px #ff0044}}
</style>
""", unsafe_allow_html=True)

# العنوان
st.markdown("<h1 class='title'>CYBERBRIEF</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-Time Global Threat Intelligence • Updated Daily</div>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align:center;color:#00ffff;margin:50px 0'>{date.today():%A, %B %d, %Y}</h4>", unsafe_allow_html=True)

# البيانات
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
    return len(t) + sum(w in t for w in CRITICAL)*300

top7 = sorted(news, key=score, reverse=True)[:7]
st.success(f"تم فحص **{len(news)}** حدث • عرض أخطر **{len(top7)}** تهديدات")

for i, item in enumerate(top7):
    level = "critical" if any(k in item['title'].lower() for k in CRITICAL) else "high"
    txt = "CRITICAL" if level=="critical" else "HIGH"
    summary = (item.get('summary') or "")[:420] + ("..." if len(item.get('summary',''))>420 else "")
    source = item.get('link','').split('/')[2].replace('www.','').split('.')[0].title()

    st.markdown(f"""
    <div class="card">
        <div class="rank">#{i+1}</div>
        <span class="level {level}">{txt}</span>
        <h3 style="color:#00ffff;margin:15px 0">{item['title']}</h3>
        <p style="color:#00ffea;font-weight:bold;margin:10px 0">Source: {source}</p>
        <p style="line-height:1.9;color:#e0e0e0">{summary}</p>
        <br>
        <a href="{item['link']}" target="_blank" style="color:#ff00ff;font-weight:bold;font-size:1.3rem;text-decoration:none">
            READ FULL REPORT →
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;padding:70px;color:#00ffff;font-family:Orbitron;font-size:1.8rem'>"
            "System Status: ONLINE • Next Update: 08:00 AM UTC</div>", unsafe_allow_html=True)
