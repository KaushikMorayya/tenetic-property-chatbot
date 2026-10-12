import streamlit as st
import requests

st.set_page_config(layout="wide", page_title="TENETIC Property Analytics Chatbot")

st.markdown("""
<style>
:root {
    --gold: #d4af37; --gold-light: #f0d264; --gold-dark: #b8941f;
    --black: #0a0a0a; --dark-gray: #1a1a1a; --gray: #2a2a2a;
    --white: #ffffff; --text-muted: #a0a0a0;
}
html, body, [class*="css"]  { background-color: #0a0a0a !important; color: #f0d264; }
strong, h1, h2, h3, h4, h5 { color: #d4af37 !important; }
.stButton > button { background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%); color: #0a0a0a; font-weight: bold; border-radius:10px; border:none; }
.stTextInput>div>div>input { background-color: #2a2a2a; color: #fff; border-radius:10px; border:1px solid #b8941f; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='padding:15px 0;border-bottom:2px solid #d4af37;'>
  <span style='font-size:28px;font-weight:800;color:#d4af37;'>🏢 TENETIC</span>
  <span style='font-size:18px;color:#a0a0a0;font-weight:400;vertical-align:middle;'>Property Analytics</span>
</div>
<h1 style='margin-top:25px;'>🏡 TENETIC Property Analytics</h1>
<p>Ask anything about property sales, inventory, agent performance, city trends, price tiers, and sales velocity. Powered by AI.</p>
""", unsafe_allow_html=True)

with st.expander("Featured Properties", expanded=False):
    cols = st.columns(4)
    property_images = [
        "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800",
        "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
        "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800",
        "https://images.unsplash.com/photo-1542621334-a254cf47733d?w=800",
    ]
    alts = ["Modern House", "Apartment", "Luxury Property", "Real Estate"]
    for i, col in enumerate(cols):
        col.image(property_images[i], use_column_width=True, caption=alts[i])

# Sidebar About Section
st.sidebar.title("ℹ️ About")
st.sidebar.markdown("""
- <strong>What is this?</strong><br> TENETIC is a property analytics platform that analyzes real estate data using a multi-layer architecture (Bronze → Silver → Gold → Platinum → Semantic). This chatbot is powered by a Supervisor Agent that routes your questions to specialized subagents.<br>

- <strong>How does the AI work?</strong><br>
The Agent has three subagents:<br>
• Genie Space — answers all structured data questions<br>
• Price Tier Function — classifies property tiers<br>
• Sales Velocity Function — classifies sales speed<br>

- <strong>Tech Stack:</strong> Databricks (UC, Model Serving, Supervisor Agent), Streamlit (UI)
""", unsafe_allow_html=True)

# Chat Section
st.subheader("💬 Chat with TENETIC AI Assistant")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_question = st.text_input("Type your question:")
if st.button("Ask") and user_question:
    # Read secrets from Streamlit Cloud (or env)
    DATABRICKS_HOST = st.secrets.get('DATABRICKS_HOST', '')
    DATABRICKS_TOKEN = st.secrets.get('DATABRICKS_TOKEN', '')
    ENDPOINT_NAME = st.secrets.get('ENDPOINT_NAME', '')
    st.write("HOST:", DATABRICKS_HOST)
    st.write("TOKEN:", DATABRICKS_TOKEN[:6])  # Only show first 6 characters for debugging
    st.write("ENDPOINT:", ENDPOINT_NAME)
    if not DATABRICKS_HOST or not ENDPOINT_NAME or not DATABRICKS_TOKEN:
        st.error('Databricks secret configuration missing! Ensure DATABRICKS_HOST, DATABRICKS_TOKEN, and SERVING_ENDPOINT_NAME are set.')
    else:
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
                # Extract the final assistant message from the output array
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
                st.success(chat_response)
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")
        except Exception as e:
            st.error(f"Error during API call: {e}")

# Display chat history
if st.session_state['chat_history']:
    st.markdown("**Previous Chat:**")
    for q, a in st.session_state['chat_history']:
        st.markdown(f"<div style='background:#262626;padding:10px;margin-bottom:5px;border-radius:10px;color:#fff'><b>You:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#393619;padding:10px;margin-bottom:12px;border-radius:10px;color:#eedc82'><b>Bot:</b> {a}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#262626;padding:10px;border-radius:10px;color:#fff'><b>You:</b> {q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#393619;padding:10px;margin-bottom:12px;border-radius:10px;color:#eedc82'><b>Bot:</b> {a}</div>", unsafe_allow_html=True)
