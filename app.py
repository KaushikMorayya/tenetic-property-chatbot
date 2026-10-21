import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide", page_title="TENETIC | Luxury Real Estate", page_icon="🏢", initial_sidebar_state="collapsed")

# 1. Luxury Single-Page CSS, Sticky Nav & Floating Button
st.markdown("""
<style>
:root {
    --gold: #d4af37; --gold-light: #f0d264; --bg-dark: #0a0a0a; --card-bg: #1a1a1a;
}
html, body, [class*="css"] { 
    background-color: var(--bg-dark) !important; 
    color: #ffffff; 
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    scroll-behavior: smooth; 
}
h1, h2, h3, h4 { color: var(--gold) !important; font-weight: 300; letter-spacing: 1px; }

/* Sticky Top Navigation */
.top-nav {
    position: fixed; top: 0; left: 0; right: 0; background: rgba(10, 10, 10, 0.95);
    padding: 20px 60px; z-index: 9999; border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    display: flex; justify-content: space-between; align-items: center; backdrop-filter: blur(10px);
}
.nav-brand { font-size: 26px; font-weight: 900; letter-spacing: 3px; color: #d4af37; text-transform: uppercase; }
.nav-links a {
    color: #ffffff; text-decoration: none; margin-left: 40px; font-weight: 400; font-size: 14px; 
    text-transform: uppercase; letter-spacing: 1px; transition: color 0.3s;
}
.nav-links a:hover { color: var(--gold); }

/* Floating AI Assistant Button */
.floating-chat-btn {
    position: fixed; bottom: 40px; right: 40px; z-index: 9999;
    background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
    color: #000 !important; padding: 15px 25px; border-radius: 30px;
    font-weight: bold; font-size: 16px; text-decoration: none;
    box-shadow: 0 10px 25px rgba(212, 175, 55, 0.3); transition: transform 0.3s;
}
.floating-chat-btn:hover { transform: translateY(-5px); }

/* Custom Formatting */
.hero-text { font-size: 4.5rem; font-weight: 200; line-height: 1.1; margin-bottom: 20px; }
.section-padding { padding: 80px 0; }
.metric-card { background: var(--card-bg); padding: 30px; border-radius: 0px; border: 1px solid #333; text-align: center; }
.metric-value { font-size: 2.5rem; color: var(--gold); font-weight: 200; }
.metric-label { color: #888; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 10px; }

/* Streamlit Overrides */
div[data-testid="stToolbar"] { display: none; }
.stTextInput>div>div>input { background-color: #1a1a1a; color: #fff; border: 1px solid #d4af37; border-radius: 0px; padding: 15px; }
.stButton>button { background: var(--gold); color: #000; font-weight: bold; border-radius: 0px; border: none; width: 100%; padding: 10px; text-transform: uppercase; }
.stButton>button:hover { background: var(--gold-light); }
</style>

<!-- Top Navigation -->
<div class="top-nav">
    <div class="nav-brand">TENETIC</div>
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#portfolio">Exclusive Portfolio</a>
        <a href="#market-insights">Market Insights</a>
        <a href="#ai-assistant">Concierge AI</a>
    </div>
</div>

<!-- Floating Chat Button -->
<a href="#ai-assistant" class="floating-chat-btn">💬 Ask Tenetic AI</a>

<div id="home" style="margin-top: 80px;"></div>
""", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("""
<div class="section-padding" style="text-align: center; background-image: linear-gradient(rgba(10,10,10,0.8), rgba(10,10,10,0.9)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=1600'); background-size: cover; background-position: center; padding: 150px 20px;">
    <div class="hero-text">Curated Estates.<br>Driven by Intelligence.</div>
    <p style="font-size: 1.2rem; color: #ccc; max-width: 600px; margin: 0 auto; font-weight: 300; letter-spacing: 1px;">
        Explore the world's most prestigious properties, backed by an analytical foundation of 22,000 verified listings and 12,755 closed market transactions.
    </p>
</div>
""", unsafe_allow_html=True)

# Data Summary Banner (Context from your Semantic Layer)
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown("<div class='metric-card'><div class='metric-value'>21,971</div><div class='metric-label'>Active Listings</div></div>", unsafe_allow_html=True)
with col2: st.markdown("<div class='metric-card'><div class='metric-value'>12,755</div><div class='metric-label'>Closed Sales</div></div>", unsafe_allow_html=True)
with col3: st.markdown("<div class='metric-card'><div class='metric-value'>347</div><div class='metric-label'>Cities Covered</div></div>", unsafe_allow_html=True)
with col4: st.markdown("<div class='metric-card'><div class='metric-value'>150</div><div class='metric-label'>Elite Agents</div></div>", unsafe_allow_html=True)

# 3. Portfolio Section
st.markdown("<div id='portfolio' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 50px;'>Exclusive Portfolio</h2>", unsafe_allow_html=True)

port_col1, port_col2, port_col3 = st.columns(3)
with port_col1:
    st.image("https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800", use_column_width=True)
    st.markdown("<h3 style='font-size: 1.5rem; margin-top: 15px;'>The Azure Villa</h3><p style='color: #888;'>Mumbai • 5 Beds • 8,500 Sq Ft<br><strong style='color:#d4af37;'>₹24.5 Cr</strong></p>", unsafe_allow_html=True)
with port_col2:
    st.image("https://images.unsplash.com/photo-1600566753086-00f18efc2291?w=800", use_column_width=True)
    st.markdown("<h3 style='font-size: 1.5rem; margin-top: 15px;'>Skyline Penthouse</h3><p style='color: #888;'>Bengaluru • 4 Beds • 5,200 Sq Ft<br><strong style='color:#d4af37;'>₹18.2 Cr</strong></p>", unsafe_allow_html=True)
with port_col3:
    st.image("https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800", use_column_width=True)
    st.markdown("<h3 style='font-size: 1.5rem; margin-top: 1
