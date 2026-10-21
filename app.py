import streamlit as st
import requests
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="TENETIC | Luxury Analytics", page_icon="🏢", initial_sidebar_state="collapsed")

# 1. Luxury Single-Page CSS & Sticky Nav
st.markdown("""
<style>
:root {
    --gold: #d4af37; --gold-light: #f0d264; --bg-dark: #050505; --card-bg: #121212;
}
html, body, [class*="css"] { background-color: var(--bg-dark) !important; color: #ffffff; font-family: 'Helvetica Neue', sans-serif; scroll-behavior: smooth; }
h1, h2, h3 { color: var(--gold) !important; }

/* Sticky Top Navigation */
.top-nav {
    position: fixed; top: 0; left: 0; right: 0; background: rgba(5, 5, 5, 0.95);
    padding: 15px 50px; z-index: 9999; border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    display: flex; justify-content: space-between; align-items: center; backdrop-filter: blur(10px);
}
.nav-links a {
    color: #ffffff; text-decoration: none; margin-left: 30px; font-weight: 500; font-size: 16px; transition: color 0.3s;
}
.nav-links a:hover { color: var(--gold); }

/* Floating AI Chat Button area */
.floating-chat {
    position: fixed; bottom: 30px; right: 30px; z-index: 9999;
}

/* Custom Cards */
.metric-card {
    background: var(--card-bg); border: 1px solid rgba(212, 175, 55, 0.1); padding: 25px; border-radius: 10px; text-align: center;
}
.metric-value { font-size: 2.5rem; color: var(--gold); font-weight: bold; }
.metric-label { color: #888; font-size: 1rem; text-transform: uppercase; letter-spacing: 1px; }

/* Inputs & Buttons */
.stTextInput>div>div>input { background-color: #1a1a1a; color: #fff; border: 1px solid #d4af37; border-radius: 5px; }
.stButton>button { background: var(--gold); color: #000; font-weight: bold; border-radius: 5px; border: none; width: 100%; }
.stButton>button:hover { background: var(--gold-light); }
</style>

<div class="top-nav">
    <div style="font-size: 24px; font-weight: 900; letter-spacing: 2px; color: #d4af37;">TENETIC</div>
    <div class="nav-links">
        <a href="#overview">Overview</a>
        <a href="#market-insights">Market Insights</a>
        <a href="#portfolio">Portfolio</a>
        <a href="#ai-assistant">Ask Tenetic AI</a>
    </div>
</div>
<div style="margin-top: 80px;"></div>
""", unsafe_allow_html=True)

# 2. Hero Section
st.header("Overview", anchor="overview")
st.markdown("""
<div style="text-align: center; padding: 60px 0;">
    <h1 style="font-size: 4rem; margin-bottom: 10px;">Intelligence, Refined.</h1>
    <p style="font-size: 1.2rem; color: #a0a0a0; max-width: 800px; margin: 0 auto;">
        Query 22,000+ curated property records instantly. Powered by Databricks Medallion Architecture and Semantic AI.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown("<div class='metric-card'><div class='metric-value'>22K+</div><div class='metric-label'>Properties</div></div>", unsafe_allow_html=True)
with col2: st.markdown("<div class='metric-card'><div class='metric-value'>12,755</div><div class='metric-label'>Closed Sales</div></div>", unsafe_allow_html=True)
with col3: st.markdown("<div class='metric-card'><div class='metric-value'>347</div><div class='metric-label'>Cities Covered</div></div>", unsafe_allow_html=True)
with col4: st.markdown("<div class='metric-card'><div class='metric-value'>150</div><div class='metric-label'>Top Agents</div></div>", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# 3. Market Insights (Charts)
st.header("Market Insights", anchor="market-insights")
st.write("Live pipeline aggregates from `gold_city_sales` and `gold_agent_performance`[cite: 8].")

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("Top Cities by Revenue")
    # Simulated data representing your gold_city_sales[cite: 8]
    city_data = pd.DataFrame({
        "City": ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad"],
        "Revenue (Billion ₹)": [47.2, 33.0, 31.6, 27.9, 22.6]
    }).set_index("City")
    st.bar_chart(city_data, color="#d4af37")

with chart_col2:
    st.subheader("Sales Velocity Trends")
    trend_data = pd.DataFrame({
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
        "Days on Market": [45, 42, 38, 35, 30, 28]
    }).set_index("Month")
    st.line_chart(trend_data, color="#f0d264")

st.markdown("<br><hr style='border-color: rgba(212,175,55,0.2);'><br>", unsafe_allow_html=True)

# 4. Premium Portfolio Gallery
st.header("Featured Portfolio", anchor="portfolio")
st.write("Explore active inventory classified by our Semantic Platinum views[cite: 8].")
img_col1, img_col2, img_col3 = st.columns(3)
with img_col1:
    st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800", caption="Luxury Villa • ₹24.5 Cr")
with img_col2:
    st.image("https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800", caption="Premium Apartment • ₹8.2 Cr")
with img_col3:
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800", caption="Commercial Space • ₹15.0 Cr")

st.markdown("<br><br><br>", unsafe_allow_html=True)

# 5. AI Assistant Section (The Supervised Agent)
st.header("Tenetic AI Assistant", anchor="ai-assistant")
st.markdown("""
<div style='background:#121212; padding:30px; border-radius:10px; border-left: 5px solid #d4af37; margin-bottom: 20px;'>
    <h3 style='margin-top:0;'>Ask the Supervisor Agent</h3>
    <p style='color:#a0a0a0;'>The agent automatically routes your query to the correct Semantic view (`vw_sales_analytics` or `vw_inventory_analytics`) applying business logic guardrails[cite: 8].</p>
</div>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_question = st.text_input("Enter your query:", placeholder="e.g., Which top 5 cities generated the highest sales revenue?")

if st.button("Submit Query") and user_question:
    DATABRICKS_HOST = st.secrets.get('DATABRICKS_HOST', '')
    DATABRICKS_TOKEN = st.secrets.get('DATABRICKS_TOKEN', '')
    ENDPOINT_NAME = st.secrets.get('ENDPOINT_NAME', '')

    if not DATABRICKS_HOST or not ENDPOINT_NAME or not DATABRICKS_TOKEN:
        st.error('System Offline: Databricks credentials missing in Streamlit Cloud Secrets.')
    else:
        with st.spinner('Supervised Agent is analyzing...'):
            payload = {"input": [{"role": "user", "content": user_question}]}
            headers = {
                "Authorization": f"Bearer {DATABRICKS_TOKEN}",
                "Content-Type": "application/json",
            }
            try:
                api_url = f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations"
                resp = requests.post(api_url, headers=headers, json=payload, timeout=120)
                
                if resp.status_code == 200:
                    result = resp.json()
                    chat_response = "Unable to parse response."
                    
                    for item in reversed(result.get("output", [])):
                        if item.get("type") == "message":
                            for c in item.get("content", []):
                                if c.get("type") == "output_text" and c.get("text"):
                                    chat_response = c["text"]
                                    break
                            if chat_response != "Unable to parse response.":
                                break
                                
                    st.session_state['chat_history'].append((user_question, chat_response))
                else:
                    st.error(f"Endpoint Error {resp.status_code}: {resp.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# Display Chat History
for q, a in reversed(st.session_state['chat_history']):
    st.markdown(f"<div style='background:#1a1a1a; padding:15px; margin-bottom:5px; border-radius:5px;'><b>You:</b> {q}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#2a2510; padding:15px; margin-bottom:20px; border-radius:5px; color:#f0d264;'><b>Tenetic AI:</b> {a}</div>", unsafe_allow_html=True)

# Footer Spacer
st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
