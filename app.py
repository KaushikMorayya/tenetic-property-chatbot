import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="TENETIC | Luxury Real Estate", page_icon="🏢", initial_sidebar_state="collapsed")

# 1. Luxury CSS, Sticky Nav, Floating Button & Carousel
st.markdown("""
<style>
:root { --gold: #d4af37; --gold-light: #f0d264; --bg-dark: #0a0a0a; --card-bg: #1a1a1a; }
html, body, [class*="css"] { 
    background-color: var(--bg-dark) !important; color: #ffffff; 
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; scroll-behavior: smooth; 
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
    color: #ffffff; text-decoration: none; margin-left: 30px; font-weight: 400; font-size: 13px; 
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

/* Layout Formatting */
.hero-text { font-size: 4.5rem; font-weight: 200; line-height: 1.1; margin-bottom: 20px; }
.section-padding { padding: 80px 0 40px 0; }
.metric-card { background: var(--card-bg); padding: 30px; border: 1px solid #333; text-align: center; }
.metric-value { font-size: 2.5rem; color: var(--gold); font-weight: 200; }
.metric-label { color: #888; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 10px; }

/* Benefits Section Cards */
.benefit-card { background: var(--card-bg); padding: 40px 30px; border-radius: 10px; border: 1px solid #333; text-align: center; height: 100%; transition: transform 0.3s; }
.benefit-card:hover { transform: translateY(-5px); border-color: var(--gold); }
.benefit-icon { font-size: 3rem; margin-bottom: 20px; }

/* CSS Carousel */
.carousel-container { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 20px; padding: 20px 0; scrollbar-width: thin; scrollbar-color: var(--gold) var(--bg-dark); }
.carousel-container::-webkit-scrollbar { height: 8px; }
.carousel-container::-webkit-scrollbar-thumb { background: var(--gold); border-radius: 4px; }
.carousel-item { min-width: 400px; scroll-snap-align: start; background: var(--card-bg); border: 1px solid #333; }
.carousel-img { width: 100%; height: 250px; object-fit: cover; }
.carousel-info { padding: 20px; }
.carousel-title { font-size: 1.5rem; color: var(--gold); margin: 0 0 10px 0; }
.carousel-desc { color: #888; font-size: 0.9rem; margin: 0; line-height: 1.5; }

/* Property Listing Cards (List View) */
.listing-card { display: flex; background: #151515; border: 1px solid #333; border-radius: 8px; margin-bottom: 25px; overflow: hidden; flex-wrap: wrap; }
.listing-img-container { width: 40%; position: relative; min-width: 300px; flex-grow: 1; }
.listing-img-container img { width: 100%; height: 100%; object-fit: cover; min-height: 250px; }
.badge-verified { position: absolute; top: 15px; left: 15px; background: rgba(0,0,0,0.8); color: #fff; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; border: 1px solid #d4af37; display: flex; align-items: center; gap: 5px; }
.listing-details { width: 60%; padding: 30px; display: flex; flex-direction: column; flex-grow: 2; min-width: 300px; }
.listing-price { font-size: 32px; color: #fff; font-weight: bold; margin-bottom: 10px; }
.listing-specs { color: #ccc; font-size: 16px; margin-bottom: 10px; font-weight: 300; }
.listing-specs span { margin-right: 15px; }
.listing-tags { color: #5bc0be; font-size: 14px; margin-bottom: 15px; }
.listing-location { color: #888; font-size: 15px; margin-bottom: 15px; display: flex; align-items: center; gap: 5px; }
.listing-validation { background: #222; padding: 8px 15px; border-radius: 5px; font-size: 12px; color: #aaa; width: fit-content; margin-bottom: 25px; display: flex; align-items: center; gap: 8px; }
.listing-actions { display: flex; gap: 15px; margin-top: auto; }
.action-btn { padding: 10px 0; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 14px; text-align: center; flex: 1; cursor: pointer; transition: 0.3s; }
.btn-email { background: transparent; border: 1px solid #007bb5; color: #007bb5; }
.btn-email:hover { background: rgba(0,123,181,0.1); }
.btn-call { background: transparent; border: 1px solid #00a651; color: #00a651; }
.btn-call:hover { background: rgba(0,166,81,0.1); }
.btn-wa { background: #25d366; border: 1px solid #25d366; color: #fff; }
.btn-wa:hover { background: #20bd5a; }

/* Inputs & Buttons */
div[data-testid="stToolbar"] { display: none; }
.stTextInput>div>div>input { background-color: #1a1a1a; color: #fff; border: 1px solid #d4af37; border-radius: 0px; padding: 15px; }
.stTextArea>div>div>textarea { background-color: #1a1a1a; color: #fff; border: 1px solid #333; border-radius: 0px; }
.stButton>button { background: var(--gold); color: #000; font-weight: bold; border-radius: 0px; border: none; width: 100%; padding: 10px; text-transform: uppercase; transition: 0.3s; }
.stButton>button:hover { background: var(--gold-light); color: #000; }
</style>

<!-- Top Navigation -->
<div class="top-nav">
    <div class="nav-brand">TENETIC</div>
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#benefits">Why Us</a>
        <a href="#portfolio">Portfolio</a>
        <a href="#listings">Properties</a>
        <a href="#market-insights">Insights</a>
        <a href="#contact">Contact</a>
    </div>
</div>

<!-- Floating Chat Button -->
<a href="#ai-assistant" class="floating-chat-btn" id="ask-ai-btn">💬 Ask Tenetic AI</a>
<div id="home" style="margin-top: 80px;"></div>
""", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("""
<div class="section-padding" style="text-align: center; background-image: linear-gradient(rgba(10,10,10,0.8), rgba(10,10,10,0.9)), url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=1600&q=80'); background-size: cover; background-position: center; padding: 150px 20px;">
    <div class="hero-text">Curated Estates.<br>Driven by Intelligence.</div>
    <p style="font-size: 1.2rem; color: #ccc; max-width: 600px; margin: 0 auto; font-weight: 300; letter-spacing: 1px;">
        Explore the world's most prestigious properties, backed by an analytical foundation of 22,000 verified listings and 12,755 closed market transactions.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown("<div class='metric-card'><div class='metric-value'>21,971</div><div class='metric-label'>Active Listings</div></div>", unsafe_allow_html=True)
with col2: st.markdown("<div class='metric-card'><div class='metric-value'>12,755</div><div class='metric-label'>Closed Sales</div></div>", unsafe_allow_html=True)
with col3: st.markdown("<div class='metric-card'><div class='metric-value'>347</div><div class='metric-label'>Cities Covered</div></div>", unsafe_allow_html=True)
with col4: st.markdown("<div class='metric-card'><div class='metric-value'>150</div><div class='metric-label'>Elite Agents</div></div>", unsafe_allow_html=True)

# 3. Benefits of Choosing Us
st.markdown("<div id='benefits' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Benefits of Choosing Us</h2>", unsafe_allow_html=True)

ben1, ben2, ben3 = st.columns(3)
with ben1:
    st.markdown("""
    <div class='benefit-card'>
        <div class='benefit-icon'>🏅</div>
        <h3 style='font-size: 1.3rem; margin-bottom: 15px;'>Extensive Expertise</h3>
        <p style='color: #888; font-size: 0.95rem; line-height: 1.6;'>With decades of experience in high-end property valuations and a dedicated team of specialized data engineers, TENETIC offers a wealth of market expertise. Our professionals handle diverse portfolio needs across global markets.</p>
    </div>
    """, unsafe_allow_html=True)
with ben2:
    st.markdown("""
    <div class='benefit-card'>
        <div class='benefit-icon'>⭐</div>
        <h3 style='font-size: 1.3rem; margin-bottom: 15px;'>Trusted Reputation</h3>
        <p style='color: #888; font-size: 0.95rem; line-height: 1.6;'>Recognized as an industry leader in property intelligence, our track record speaks volumes. Choosing us means opting for a trusted, reliable partner with a proven history of delivering analytical excellence.</p>
    </div>
    """, unsafe_allow_html=True)
with ben3:
    st.markdown("""
    <div class='benefit-card'>
        <div class='benefit-icon'>🛡️</div>
        <h3 style='font-size: 1.3rem; margin-bottom: 15px;'>Speed & Security</h3>
        <p style='color: #888; font-size: 0.95rem; line-height: 1.6;'>We understand the importance of efficiency and confidentiality. Our streamlined Databricks Medallion architecture enables lightning-fast insights while ensuring your portfolio data is handled with the utmost security.</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Portfolio Section (Carousel with Fixed Image URLs)
st.markdown("<div id='portfolio' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>Exclusive Portfolio</h2>", unsafe_allow_html=True)

st.markdown("""
<div class="carousel-container">
    <div class="carousel-item">
        <img class="carousel-img" src="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80" alt="Villa">
        <div class="carousel-info">
            <h3 class="carousel-title">The Azure Villa</h3>
            <p class="carousel-desc">Mumbai • 5 Beds • 8,500 Sq Ft<br><strong style="color:#d4af37; font-size:1.2rem;">₹24.5 Cr</strong></p>
        </div>
    </div>
    <div class="carousel-item">
        <img class="carousel-img" src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&q=80" alt="Penthouse">
        <div class="carousel-info">
            <h3 class="carousel-title">Skyline Penthouse</h3>
            <p class="carousel-desc">Bengaluru • 4 Beds • 5,200 Sq Ft<br><strong style="color:#d4af37; font-size:1.2rem;">₹18.2 Cr</strong></p>
        </div>
    </div>
    <div class="carousel-item">
        <img class="carousel-img" src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&q=80" alt="Estate">
        <div class="carousel-info">
            <h3 class="carousel-title">Heritage Estate</h3>
            <p class="carousel-desc">Delhi • 6 Beds • 12,000 Sq Ft<br><strong style="color:#d4af37; font-size:1.2rem;">₹32.0 Cr</strong></p>
        </div>
    </div>
    <div class="carousel-item">
        <img class="carousel-img" src="https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=800&q=80" alt="Coastal">
        <div class="carousel-info">
            <h3 class="carousel-title">Coastal Retreat</h3>
            <p class="carousel-desc">Goa • 5 Beds • 7,500 Sq Ft<br><strong style="color:#d4af37; font-size:1.2rem;">₹21.5 Cr</strong></p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. Detailed Property Listings (List View)
st.markdown("<div id='listings' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 25px;">
    <h2 style='margin: 0;'>Available Properties</h2>
    <div style="color: #d4af37; font-size: 14px; border: 1px solid #d4af37; padding: 5px 15px; border-radius: 20px;">Sort by: <b>Popular</b> ▼</div>
</div>

<!-- Listing Card 1 -->
<div class="listing-card">
    <div class="listing-img-container">
        <div class="badge-verified">✓ Tenetic Verified™</div>
        <img src="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80" alt="Apartment View">
    </div>
    <div class="listing-details">
        <div class="listing-price">₹ 12,50,00,000</div>
        <div class="listing-specs">
            <span>Apartment</span> <span>🛏 3</span> <span>🛁 3</span> <span>Area: 2,450 sqft</span>
        </div>
        <div class="listing-tags">Full Sea View | Brand New | High Floor</div>
        <div class="listing-location">📍 Worli Sea Face, South Mumbai, MH</div>
        <div class="listing-validation">✦ Agent last visited this property on 18th of October</div>
        <div class="listing-actions">
            <div class="action-btn btn-email">✉ Email</div>
            <div class="action-btn btn-call">📞 Call</div>
            <div class="action-btn btn-wa">💬 WhatsApp</div>
        </div>
    </div>
</div>

<!-- Listing Card 2 -->
<div class="listing-card">
    <div class="listing-img-container">
        <div class="badge-verified" style="background: rgba(80,80,80,0.9); border-color:#888;">✓ Checked</div>
        <img src="https://images.unsplash.com/photo-1600566752355-35792bedcfea?w=800&q=80" alt="Penthouse View">
    </div>
    <div class="listing-details">
        <div class="listing-price">₹ 18,25,00,000</div>
        <div class="listing-specs">
            <span>Penthouse</span> <span>🛏 4</span> <span>🛁 5</span> <span>Area: 4,100 sqft</span>
        </div>
        <div class="listing-tags">Private Terrace | Park Facing | Skyline View</div>
        <div class="listing-location">📍 Jubilee Hills, Central Park, Hyderabad</div>
        <div class="listing-validation">✦ Property authenticity was validated on 12th of October</div>
        <div class="listing-actions">
            <div class="action-btn btn-email">✉ Email</div>
            <div class="action-btn btn-call">📞 Call</div>
            <div class="action-btn btn-wa">💬 WhatsApp</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Market Insights Section
st.markdown("<div id='market-insights' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 40px;'>Market Insights</h2>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.markdown("<h4 style='text-align: center;'>Top Markets by Volume</h4>", unsafe_allow_html=True)
    city_data = pd.DataFrame({"City": ["Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad"], "Revenue (Billion ₹)": [47.2, 33.0, 31.6, 27.9, 22.6]}).set_index("City")
    st.bar_chart(city_data, color="#d4af37")

with chart_col2:
    st.markdown("<h4 style='text-align: center;'>Average Days on Market (Velocity)</h4>", unsafe_allow_html=True)
    velocity_data = pd.DataFrame({"Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "Days": [42, 38, 35, 31, 28, 25]}).set_index("Month")
    st.line_chart(velocity_data, color="#f0d264")

# 7. AI Assistant Section (Supervised Agent)
st.markdown("<div id='ai-assistant' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='background-color: #111; border: 1px solid #333; padding: 50px; text-align: center; margin-bottom: 30px;'>
    <h2>Tenetic Concierge AI</h2>
    <p style='color: #888; max-width: 600px; margin: 0 auto; line-height: 1.6;'>
        Experience real estate analytics elevated by artificial intelligence. Ask our Concierge AI about regional market trends, top-performing cities, or active property availability to receive instant, data-driven insights.
    </p>
</div>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

chat_col, history_col = st.columns([2, 1])

with chat_col:
    user_question = st.text_input("Enter your query:", placeholder="e.g., Which city generated the highest sales revenue last quarter?", key="chat_input")
    
    if st.button("Submit Inquiry") and user_question:
        DATABRICKS_HOST = st.secrets.get('DATABRICKS_HOST', '')
        DATABRICKS_TOKEN = st.secrets.get('DATABRICKS_TOKEN', '')
        ENDPOINT_NAME = st.secrets.get('ENDPOINT_NAME', '')

        if not DATABRICKS_HOST or not ENDPOINT_NAME or not DATABRICKS_TOKEN:
            st.error('Offline Mode: Authentication credentials missing.')
        else:
            with st.spinner('Consulting intelligence network...'):
                payload = {"input": [{"role": "user", "content": user_question}]}
                headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}", "Content-Type": "application/json"}
                try:
                    resp = requests.post(f"{DATABRICKS_HOST}/serving-endpoints/{ENDPOINT_NAME}/invocations", headers=headers, json=payload, timeout=120)
                    if resp.status_code == 200:
                        chat_response = "Unable to parse response."
                        for item in reversed(resp.json().get("output", [])):
                            if item.get("type") == "message":
                                for c in item.get("content", []):
                                    if c.get("type") == "output_text" and c.get("text"):
                                        chat_response = c["text"]
                                        break
                                if chat_response != "Unable to parse response.":
                                    break
                        st.session_state['chat_history'].append((user_question, chat_response))
                    else:
                        st.error(f"Network Error {resp.status_code}: {resp.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

    if st.session_state['chat_history']:
        latest_q, latest_a = st.session_state['chat_history'][-1]
        st.markdown(f"""
        <div style='background:#1a1a1a; padding:30px; border-top:3px solid #d4af37; margin-top:20px;'>
            <h4 style='margin-top:0; font-size:12px; color:#888; text-transform:uppercase;'>Concierge Response</h4>
            <div style='font-size: 1.1rem; line-height: 1.6; color:#fff;'>{latest_a}</div>
        </div>
        """, unsafe_allow_html=True)

with history_col:
    st.markdown("<h4 style='font-size:14px; text-transform:uppercase; color:#888;'>Recent Inquiries</h4>", unsafe_allow_html=True)
    st.markdown("<div style='height: 300px; overflow-y: auto; padding-right:15px;'>", unsafe_allow_html=True)
    for q, a in reversed(st.session_state['chat_history'][:-1]):
        st.markdown(f"<div style='background:#111; padding:15px; margin-bottom:10px; border:1px solid #333; font-size:14px;'><b>Q:</b> {q}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Contact Us Section
st.markdown("<div id='contact' class='section-padding'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>Contact Us</h2>", unsafe_allow_html=True)

contact_col1, contact_col2, contact_col3 = st.columns([1, 2, 1])
with contact_col2:
    st.markdown("<p style='text-align: center; color: #888; margin-bottom: 20px;'>Get in touch with our elite advisory team for bespoke portfolio solutions.</p>", unsafe_allow_html=True)
    with st.form("contact_form"):
        st.text_input("Full Name")
        st.text_input("Email Address")
        st.text_area("Message", height=120)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            st.success("Thank you. A TENETIC advisor will contact you shortly.")

# Footer
st.markdown("<div style='padding: 80px 0 40px 0; text-align: center; color: #555; font-size: 12px; text-transform: uppercase;'>© 2026 TENETIC Intelligence. All Rights Reserved.</div>", unsafe_allow_html=True)

# JavaScript for Autofocusing the Chat Input on Floating Button Click
components.html("""
<script>
    const parentDoc = window.parent.document;
    const askButton = parentDoc.getElementById('ask-ai-btn');
    
    if (askButton) {
        askButton.addEventListener('click', function(e) {
            setTimeout(() => {
                const inputField = parentDoc.querySelector('input[aria-label="Enter your query:"]');
                if (inputField) {
                    inputField.focus();
                }
            }, 600);
        });
    }
</script>
""", height=0, width=0)
