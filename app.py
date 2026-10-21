import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(layout="wide", page_title="TENETIC Property Analytics", page_icon="🏢")

# 2. Custom CSS (Luxury Black & Gold Theme)
st.markdown("""
<style>
:root {
    --gold: #d4af37; --gold-light: #f0d264; --gold-dark: #b8941f;
    --black: #0a0a0a; --dark-gray: #1a1a1a; --gray: #2a2a2a;
    --white: #ffffff; --text-muted: #a0a0a0;
}
html, body, [class*="css"]  { background-color: #0a0a0a !important; color: #f0d264; }
strong, h1, h2, h3, h4, h5, h6 { color: #d4af37 !important; }
.stButton > button { background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%); color: #0a0a0a; font-weight: bold; border-radius:8px; border:none; width: 100%; }
.stTextInput>div>div>input { background-color: #2a2a2a; color: #fff; border-radius:8px; border:1px solid #b8941f; }
.stTabs [data-baseweb="tab-list"] { gap: 24px; }
.stTabs [data-baseweb="tab"] { color: #a0a0a0; font-size: 18px; font-weight: 600; padding: 10px 20px; }
.stTabs [aria-selected="true"] { color: #d4af37 !important; border-bottom: 2px solid #d4af37 !important; }
div[data-testid="stMetricValue"] { color: #ffffff; }
div[data-testid="stMetricLabel"] { color: #d4af37; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
<div style='padding:10px 0; border-bottom:2px solid #d4af37; margin-bottom:20px;'>
  <span style='font-size:32px; font-weight:800; color:#d4af37;'>🏢 TENETIC</span>
  <span style='font-size:20px; color:#a0a0a0; font-weight:400; vertical-align:middle; margin-left: 10px;'>Property Analytics Platform</span>
</div>
""", unsafe_allow_html=True)

# 4. Define Client-Facing Tabs Only
tab1, tab2 = st.tabs(["💬 AI Assistant", "📊 Market Insights"])

# ==========================================
# TAB 1: AI ASSISTANT (Supervisor Agent)
# ==========================================
with tab1:
    st.markdown("### Ask the Data")
    st.write("Query our 22,000+ property records. The AI automatically routes your request to the correct analytical tool.")
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_col, history_col = st.columns([2, 1])
    
    with chat_col:
        user_question = st.text_input("What would you like to know about the property market?", placeholder="e.g., Which top 5 cities generated the highest sales revenue?")
        
        if st.button("Submit Query") and user_question:
            DATABRICKS_HOST = st.secrets.get('DATABRICKS_HOST', '')
            DATABRICKS_TOKEN = st.secrets.get('DATABRICKS_TOKEN', '')
            ENDPOINT_NAME = st.secrets.get('ENDPOINT_NAME', '')

            if not DATABRICKS_HOST or not ENDPOINT_NAME or not DATABRICKS_TOKEN:
                st.error('System Offline: Databricks secrets are missing from Streamlit Cloud.')
            else:
                with st.spinner('Analyzing...'):
                    # Fixed Payload: Using "input" exactly as the Databricks error requested
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
                            
                            # Fixed Parsing: Navigating the specific Agent response schema
                            for item in reversed(result.get("output", [])):
                                if item.get("type") == "message":
                                    for c in item.get("content", []):
                                        if c.get("type") == "output_text" and c.get("text"):
                                            chat_response = c["text"]
                                            break
                                    if chat_response != "Unable to parse response.":
                                        break
                                        
                            st.session_state['chat_history'].append((user_question, chat_response))
                            st.success("Response Received")
                        else:
                            st.error(f"Endpoint Error {resp.status_code}: {resp.text}")
                    except Exception as e:
                        st.error(f"Connection Failed: {e}")
                        
        if st.session_state['chat_history']:
            latest_q, latest_a = st.session_state['chat_history'][-1]
            st.markdown(f"<div style='background:#1a1a1a; padding:20px; border-left:4px solid #d4af37; border-radius:5px;'><h4 style='margin-top:0;'>Current Response</h4>{latest_a}</div>", unsafe_allow_html=True)

    with history_col:
        st.markdown("#### Chat History")
        st.markdown("<div style='height: 400px; overflow-y: auto; padding-right:10px;'>", unsafe_allow_html=True)
        for q, a in reversed(st.session_state['chat_history'][:-1]):
            st.markdown(f"<div style='background:#262626; padding:10px; margin-bottom:5px; border-radius:5px;'><b>You:</b> {q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='background:#393619; padding:10px; margin-bottom:15px; border-radius:5px; color:#eedc82'><b>Bot:</b> {a[:150]}...</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: MARKET INSIGHTS
# ==========================================
with tab2:
    st.markdown("### Portfolio Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Properties", "21,971")
    m2.metric("Closed Sales", "12,755")
    m3.metric("Total Agents", "150")
    m4.metric("Market Coverage", "347 Cities")
    
    st.markdown("---")
    st.markdown("### Featured Properties")
    cols = st.columns(4)
    property_images = [
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800",
        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
        "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800",
        "https://images.unsplash.com/photo-1542621334-a254cf47733d?w=800",
    ]
    alts = ["Modern House", "Luxury Apartment", "Premium Estate", "Commercial Plot"]
    for i, col in enumerate(cols):
        col.image(property_images[i], use_column_width=True, caption=alts[i])
