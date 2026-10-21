import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="TENETIC | Intelligence", page_icon="🏢")

# 2. Advanced Custom CSS (SaaS UI Theme)
st.markdown("""
<style>
/* Base Theme */
:root {
    --bg-color: #0f0c29;
    --card-bg: #1a1a2e;
    --primary: #f05454;
    --accent: #f0d264;
    --text-main: #ffffff;
    --text-muted: #a0a0b0;
}
html, body, [class*="css"] { background: linear-gradient(to right, #0f0c29, #302b63, #24243e) !important; color: var(--text-main); font-family: 'Inter', sans-serif; }

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Typography & Gradients */
.hero-title {
    font-size: 4.5rem;
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 20px;
    background: -webkit-linear-gradient(45deg, #ffffff, #a0a0b0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-highlight {
    background: -webkit-linear-gradient(45deg, #f05454, #f0d264);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.section-title { font-size: 2.5rem; font-weight: 800; margin-bottom: 15px; }
.sub-text { font-size: 1.2rem; color: var(--text-muted); margin-bottom: 30px; }

/* Custom Cards */
.feature-card {
    background-color: var(--card-bg);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.2s;
}
.feature-card:hover { transform: translateY(-5px); border-color: rgba(240, 210, 100, 0.3); }
.feature-icon { font-size: 2rem; margin-bottom: 15px; color: var(--primary); }

/* Comparison List */
.compare-box { background-color: var(--card-bg); padding: 30px; border-radius: 12px; height: 100%; }
.list-item { margin-bottom: 15px; font-size: 1.1rem; display: flex; align-items: center; }
.list-x { color: #f05454; font-weight: bold; margin-right: 15px; }
.list-check { color: #f0d264; font-weight: bold; margin-right: 15px; }

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] { gap: 30px; background-color: transparent; border: none; padding-top: 10px; }
.stTabs [data-baseweb="tab"] { color: var(--text-muted); font-size: 1.1rem; font-weight: 600; padding: 15px 0; }
.stTabs [aria-selected="true"] { color: #ffffff !important; border-bottom: 3px solid var(--primary) !important; background: transparent !important; }

/* Chat Inputs */
.stTextInput>div>div>input { background-color: rgba(26,26,46,0.8); color: #fff; border-radius: 8px; border: 1px solid #4a4a6a; padding: 15px; }
.stTextInput>div>div>input:focus { border-color: var(--primary); }
.stButton > button { background: linear-gradient(45deg, #f05454, #ff7b54); color: #fff; font-weight: bold; border-radius: 30px; border: none; padding: 10px 30px; width: 100%; transition: opacity 0.3s; }
.stButton > button:hover { opacity: 0.9; }
</style>
""", unsafe_allow_html=True)

# 3. Top Navigation Bar (Logo)
st.markdown("""
<div style='padding: 20px 0; display: flex; align-items: center;'>
  <div style='width: 40px; height: 40px; border-radius: 8px; background: linear-gradient(45deg, #f05454, #f0d264); display: flex; align-items: center; justify-content: center; margin-right: 15px;'>
    <span style='color: white; font-weight: 900; font-size: 20px;'>T</span>
  </div>
  <span style='font-size:24px; font-weight:800; color:#fff;'>Tenetic</span>
</div>
""", unsafe_allow_html=True)

# 4. Page Layout using Tabs
tab_home, tab_capabilities, tab_ai = st.tabs(["Home", "Platform Capabilities", "💬 Chat with Tenetic"])

# ==========================================
# TAB 1: LANDING PAGE (Hero & Comparison)
# ==========================================
with tab_home:
    st.write("") # Spacer
    
    # Hero Section
    col_text, col_img = st.columns([1.2, 1])
    with col_text:
        st.markdown("""
        <div style='margin-top: 50px;'>
            <span style='background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 20px; font-size: 0.9rem; color: #f0d264;'>● Property Intelligence, made simple</span>
            <div class='hero-title'>Ask your<br>property data<br><span class='hero-highlight'>anything.</span></div>
            <div class='sub-text'>Tenetic turns complex property datasets into answers anyone can get. Ask in plain business language and receive a result you can trust, with no SQL and no waiting on a data team.</div>
        </div>
        """, unsafe_allow_html=True)
    with col_img:
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80", use_column_width=True)

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Problem/Solution Section
    st.markdown("<div class='section-title'>A simple question should not need an analyst</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Behind \"Which city had the highest sales?\" sit datasets, joins, metric definitions, and time rules. Tenetic closes that gap.</div>", unsafe_allow_html=True)
    
    comp_col1, comp_col2 = st.columns(2)
    with comp_col1:
        st.markdown("""
        <div class='compare-box'>
            <h3 style='margin-bottom: 25px;'>Without Tenetic</h3>
            <div class='list-item'><span class='list-x'>✕</span> Simple questions wait on analysts and engineers</div>
            <div class='list-item'><span class='list-x'>✕</span> Two people define "sales velocity" two ways</div>
            <div class='list-item'><span class='list-x'>✕</span> Wrong joins and aggregation inflate the numbers</div>
            <div class='list-item'><span class='list-x'>✕</span> Trust in results drops, and so does self-service</div>
        </div>
        """, unsafe_allow_html=True)
        
    with comp_col2:
        st.markdown("""
        <div class='compare-box'>
            <h3 style='margin-bottom: 25px;'>With Tenetic</h3>
            <div class='list-item'><span class='list-check'>✓</span> Business users ask and get answers directly</div>
            <div class='list-item'><span class='list-check'>✓</span> One agreed definition for every metric</div>
            <div class='list-item'><span class='list-check'>✓</span> Correct relationships and aggregation built in</div>
            <div class='list-item'><span class='list-check'>✓</span> Every result can be checked and validated</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: CAPABILITIES GRID
# ==========================================
with tab_capabilities:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Analysis the way business teams think</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Properties, agents, regions, and time periods, not tables and joins.</div>", unsafe_allow_html=True)
    
    r1c1, r1c2, r1c3 = st.columns(3)
    with r1c1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>👥</div>
            <h4>Agent Analysis</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>Track listing performance, closed sales, and conversion rates across your workforce.</p>
        </div>
        """, unsafe_allow_html=True)
    with r1c2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🏢</div>
            <h4>Property Analysis</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>See how each asset performs, comparing price per sqft and turnaround time side by side.</p>
        </div>
        """, unsafe_allow_html=True)
    with r1c3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📊</div>
            <h4>Category Analysis</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>Understand which property tiers (Budget vs Luxury) lead the market and which are shifting.</p>
        </div>
        """, unsafe_allow_html=True)
        
    r2c1, r2c2, r2c3 = st.columns(3)
    with r2c1:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>🌍</div>
            <h4>Geographic Analysis</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>Map revenue and active inventory down to the city and neighborhood level.</p>
        </div>
        """, unsafe_allow_html=True)
    with r2c2:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>⏱️</div>
            <h4>Time-based Analysis</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>Instantly calculate month-over-month growth and days-on-market metrics.</p>
        </div>
        """, unsafe_allow_html=True)
    with r2c3:
        st.markdown("""
        <div class='feature-card'>
            <div class='feature-icon'>📈</div>
            <h4>Rankings and Growth</h4>
            <p style='color:#a0a0b0; font-size:0.9rem;'>Identify your top-performing markets and fastest-selling inventory segments.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 3: THE SUPERVISED AGENT
# ==========================================
with tab_ai:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>From property data to a business answer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text'>Query our 22,000+ property records. Databricks handles the datasets, relationships, and metric rules out of sight.</div>", unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_col, history_col = st.columns([2, 1])
    
    with chat_col:
        user_question = st.text_input("", placeholder="e.g., Which property had the highest sales revenue last quarter?")
        
        if st.button("Query Data") and user_question:
            DATABRICKS_HOST = st.secrets.get('DATABRICKS_HOST', '')
            DATABRICKS_TOKEN = st.secrets.get('DATABRICKS_TOKEN', '')
            ENDPOINT_NAME = st.secrets.get('ENDPOINT_NAME', '')

            if not DATABRICKS_HOST or not ENDPOINT_NAME or not DATABRICKS_TOKEN:
                st.error('System Offline: Databricks secrets are missing from Streamlit Cloud.')
            else:
                with st.spinner('Analyzing...'):
                    # Fixed Payload formatting exactly as required by the Databricks API error
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
                            
                            # Fixed Parsing for Databricks nested output schema
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
                        
        if st.session_state['chat_history']:
            latest_q, latest_a = st.session_state['chat_history'][-1]
            st.markdown(f"""
            <div style='background:rgba(26,26,46,0.9); padding:25px; border-radius:12px; border:1px solid #4a4a6a; margin-top: 20px;'>
                <h4 style='color:#f0d264; margin-top:0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;'>Result</h4>
                <div style='font-size: 1.1rem; line-height: 1.6;'>{latest_a}</div>
            </div>
            """, unsafe_allow_html=True)

    with history_col:
        st.markdown("#### Recent Queries")
        st.markdown("<div style='height: 400px; overflow-y: auto; padding-right:10px;'>", unsafe_allow_html=True)
        for q, a in reversed(st.session_state['chat_history'][:-1]):
            st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:15px; margin-bottom:10px; border-radius:8px; font-size:0.9rem;'><b>Q:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
