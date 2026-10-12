# ============================================================
# T_Property_Analytics_Chatbot — Gradio App for Hugging Face Spaces
# ============================================================
# Black & Gold themed chatbot that queries the TENETIC Supervisor Agent
# hosted on Databricks.
#
# DEPLOYMENT: Hugging Face Spaces (free, public)
# AUTH: Databricks Service Principal (auto-refreshing OAuth) or PAT
#
# REQUIRED ENVIRONMENT VARIABLES (set as HF Space Secrets):
#   DATABRICKS_HOST       = https://dbc-xxxxx.cloud.databricks.com
#   DATABRICKS_TOKEN      = your personal access token (simple method)
#   --- OR (better, no expiry) ---
#   DATABRICKS_HOST       = https://dbc-xxxxx.cloud.databricks.com
#   DATABRICKS_CLIENT_ID  = service principal client ID
#   DATABRICKS_CLIENT_SECRET = service principal client secret
#
#   SUPERVISOR_AGENT_NAME = supervisor-agents/xxxxxxxx (from Databricks SDK)
# ============================================================

import os
import json
import requests
import gradio as gr

# ============================================================
# Configuration (read from environment variables / secrets)
# ============================================================
DATABRICKS_HOST = os.environ.get("DATABRICKS_HOST", "")
DATABRICKS_TOKEN = os.environ.get("DATABRICKS_TOKEN", "")
DATABRICKS_CLIENT_ID = os.environ.get("DATABRICKS_CLIENT_ID", "")
DATABRICKS_CLIENT_SECRET = os.environ.get("DATABRICKS_CLIENT_SECRET", "")
SUPERVISOR_AGENT_NAME = os.environ.get("SUPERVISOR_AGENT_NAME", "")

# ============================================================
# Token Management (Service Principal OAuth auto-refresh)
# ============================================================
_cached_token = None
_token_expiry = 0

def get_access_token():
    global _cached_token, _token_expiry
    import time
    if DATABRICKS_TOKEN and not DATABRICKS_CLIENT_ID:
        return DATABRICKS_TOKEN
    if DATABRICKS_CLIENT_ID and DATABRICKS_CLIENT_SECRET:
        if _cached_token and time.time() < _token_expiry - 60:
            return _cached_token
        token_url = f"{DATABRICKS_HOST}/oidc/v1/token"
        response = requests.post(
            token_url,
            data={"grant_type": "client_credentials"},
            auth=(DATABRICKS_CLIENT_ID, DATABRICKS_CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status_code == 200:
            token_data = response.json()
            _cached_token = token_data["access_token"]
            _token_expiry = time.time() + token_data.get("expires_in", 3600)
            return _cached_token
        else:
            raise Exception(f"OAuth token request failed: {response.status_code} - {response.text}")
    raise Exception("No authentication configured. Set DATABRICKS_TOKEN or DATABRICKS_CLIENT_ID/SECRET.")


# ============================================================
# Query the Supervisor Agent
# ============================================================
def query_supervisor_agent(question, history):
    if not DATABRICKS_HOST or not SUPERVISOR_AGENT_NAME:
        return "Configuration error: DATABRICKS_HOST and SUPERVISOR_AGENT_NAME must be set."
    try:
        token = get_access_token()
        agent_id = SUPERVISOR_AGENT_NAME.split("/")[-1]
        endpoint_url = f"{DATABRICKS_HOST}/api/2.0/serving-endpoints/supervisor-{agent_id}/invocations"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        messages = []
        for h in history or []:
            if isinstance(h, list) and len(h) == 2:
                messages.append({"role": "user", "content": h[0]})
                messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": question})
        payload = {"messages": messages}
        response = requests.post(endpoint_url, headers=headers, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            elif "content" in result:
                return result["content"]
            elif "response" in result:
                return result["response"]
            else:
                return json.dumps(result, indent=2)
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================
# Custom CSS — Black & Gold Theme
# ============================================================
CUSTOM_CSS = """
:root {
    --gold: #d4af37; --gold-light: #f0d264; --gold-dark: #b8941f;
    --black: #0a0a0a; --dark-gray: #1a1a1a; --gray: #2a2a2a;
    --white: #ffffff; --text-muted: #a0a0a0;
}
.gradio-container {
    background: var(--black) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}
#navbar {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    border-bottom: 2px solid var(--gold);
    padding: 12px 30px; display: flex; align-items: center;
    justify-content: space-between; position: sticky; top: 0; z-index: 1000;
}
#navbar-logo { font-size: 28px; font-weight: 800; color: var(--gold); letter-spacing: 2px; display: flex; align-items: center; gap: 10px; }
#navbar-links { display: flex; gap: 25px; }
#navbar-links a { color: var(--text-muted); text-decoration: none; font-size: 15px; transition: color 0.3s; }
#navbar-links a:hover { color: var(--gold); }
#hero { background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0a0a0a 100%); padding: 40px 30px; text-align: center; border-bottom: 1px solid #2a2a2a; }
#hero h1 { color: var(--gold); font-size: 36px; font-weight: 800; margin-bottom: 10px; }
#hero p { color: var(--text-muted); font-size: 16px; max-width: 600px; margin: 0 auto; }
#property-gallery { display: flex; justify-content: center; gap: 20px; padding: 30px; flex-wrap: wrap; }
#property-gallery img { width: 300px; height: 200px; object-fit: cover; border-radius: 10px; border: 2px solid var(--gold); box-shadow: 0 4px 20px rgba(212,175,55,0.2); transition: transform 0.3s, box-shadow 0.3s; }
#property-gallery img:hover { transform: scale(1.05); box-shadow: 0 6px 30px rgba(212,175,55,0.4); }
#chat-section { background: var(--dark-gray); border: 1px solid var(--gold-dark); border-radius: 15px; padding: 20px; margin: 20px 30px; }
#chat-section h2 { color: var(--gold); font-size: 24px; margin-bottom: 15px; }
#chat-input textarea { background: var(--gray) !important; color: var(--white) !important; border: 1px solid var(--gold-dark) !important; border-radius: 10px !important; padding: 12px !important; font-size: 15px !important; }
#chat-input textarea:focus { border-color: var(--gold) !important; box-shadow: 0 0 10px rgba(212,175,55,0.3) !important; }
.message.user { background: var(--gray) !important; border: 1px solid var(--gold-dark) !important; color: var(--white) !important; border-radius: 10px !important; }
.message.bot { background: var(--dark-gray) !important; border-left: 3px solid var(--gold) !important; color: var(--white) !important; border-radius: 10px !important; }
.gr-button { background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%) !important; color: var(--black) !important; font-weight: 600 !important; border: none !important; border-radius: 10px !important; padding: 10px 30px !important; cursor: pointer !important; transition: all 0.3s !important; }
.gr-button:hover { background: linear-gradient(135deg, var(--gold-light) 0%, var(--gold) 100%) !important; box-shadow: 0 4px 15px rgba(212,175,55,0.4) !important; }
.gr-tab-nav { background: var(--dark-gray) !important; border-bottom: 2px solid var(--gold) !important; }
.gr-tab-nav button { color: var(--text-muted) !important; font-size: 15px !important; padding: 12px 25px !important; }
.gr-tab-nav button.selected { color: var(--gold) !important; border-bottom: 3px solid var(--gold) !important; }
#about-section { padding: 30px; color: var(--text-muted); line-height: 1.8; }
#about-section h2 { color: var(--gold); font-size: 24px; margin-bottom: 15px; }
#about-section .info-card { background: var(--dark-gray); border: 1px solid var(--gold-dark); border-radius: 10px; padding: 20px; margin-bottom: 15px; }
#about-section .info-card h3 { color: var(--gold); font-size: 18px; margin-bottom: 10px; }
#stats-grid { display: flex; justify-content: center; gap: 20px; padding: 20px 30px; flex-wrap: wrap; }
.stat-card { background: var(--dark-gray); border: 2px solid var(--gold-dark); border-radius: 15px; padding: 25px; text-align: center; min-width: 200px; transition: transform 0.3s; }
.stat-card:hover { transform: translateY(-5px); border-color: var(--gold); box-shadow: 0 5px 20px rgba(212,175,55,0.3); }
.stat-card .number { font-size: 32px; font-weight: 800; color: var(--gold); }
.stat-card .label { font-size: 14px; color: var(--text-muted); margin-top: 5px; }
#footer { background: var(--dark-gray); border-top: 2px solid var(--gold); padding: 20px 30px; text-align: center; color: var(--text-muted); font-size: 13px; }
#footer a { color: var(--gold); text-decoration: none; }
"""

# ============================================================
# Property Images (Unsplash free stock photos)
# ============================================================
PROPERTY_IMAGES = [
    "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800",
    "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800",
    "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800",
    "https://images.unsplash.com/photo-1542621334-a254cf47733d?w=800",
]

# ============================================================
# HTML Components
# ============================================================
navbar_html = """
<div id="navbar">
    <div id="navbar-logo"><span style="font-size:32px">🏢</span><span>TENETIC</span><span style="font-size:14px;color:#a0a0a0;font-weight:400">Property Analytics</span></div>
    <div id="navbar-links"><a href="#chat-section">💬 Chat</a><a href="#property-gallery">🏠 Properties</a><a href="#about-section">ℹ️ About</a></div>
</div>
"""
hero_html = '<div id="hero"><h1>🏡 TENETIC Property Analytics</h1><p>Ask anything about property sales, inventory, agent performance, city trends, price tiers, and sales velocity. Powered by AI.</p></div>'
stats_html = '''<div id="stats-grid">
<div class="stat-card"><div class="number">21,971</div><div class="label">Total Properties</div></div>
<div class="stat-card"><div class="number">12,755</div><div class="label">Properties Sold</div></div>
<div class="stat-card"><div class="number">150</div><div class="label">Real Estate Agents</div></div>
<div class="stat-card"><div class="number">347</div><div class="label">City-Month Records</div></div>
</div>'''
gallery_html = f'''<div id="property-gallery">
<img src="{PROPERTY_IMAGES[0]}" alt="Modern House">
<img src="{PROPERTY_IMAGES[1]}" alt="Apartment">
<img src="{PROPERTY_IMAGES[2]}" alt="Luxury Property">
<img src="{PROPERTY_IMAGES[3]}" alt="Real Estate">
</div>'''
about_html = '''<div id="about-section">
<h2>About TENETIC Property Analytics</h2>
<div class="info-card"><h3>📊 What is this?</h3><p>TENETIC is a property analytics platform that analyzes real estate data using a multi-layer architecture (Bronze → Silver → Gold → Platinum → Semantic). This chatbot is powered by a Supervisor Agent that routes your questions to specialized subagents.</p></div>
<div class="info-card"><h3>🤖 How does the AI work?</h3><p>The Supervisor Agent has 3 specialized subagents:<br>• <strong style="color:#d4af37">Genie Space</strong> — answers all structured data questions (sales, inventory, agents, trends)<br>• <strong style="color:#d4af37">Price Tier Function</strong> — classifies properties as Budget / Mid-Range / Premium / Luxury<br>• <strong style="color:#d4af37">Sales Velocity Function</strong> — classifies sales speed as Rapid / Normal / Slow</p></div>
<div class="info-card"><h3>💾 Data Architecture</h3><p>Bronze (raw) → Silver (cleaned) → Gold (star schema) → Platinum (OBT marts) → Semantic (Genie views) → Supervisor Agent → This Chatbot</p></div>
<div class="info-card"><h3>🛠️ Tech Stack</h3><p>Databricks (Unity Catalog, Model Serving, Supervisor Agent) + Gradio (UI) + Hugging Face Spaces (hosting)</p></div>
</div>'''
footer_html = '<div id="footer"><p>TENETIC Property Analytics — Powered by Databricks Supervisor Agent & Gradio</p><p>Built with <span style="color:#d4af37">♦</span> for property data intelligence</p></div>'

# ============================================================
# Create the Gradio Blocks Interface
# ============================================================
with gr.Blocks(css=CUSTOM_CSS, title="TENETIC Property Analytics") as app:
    gr.HTML(navbar_html)
    with gr.Tabs():
        with gr.Tab("💬 Chat"):
            gr.HTML(hero_html)
            gr.HTML(stats_html)
            with gr.Column(elem_id="chat-section"):
                gr.HTML("<h2>Ask the TENETIC AI Assistant</h2>")
                chatbot = gr.ChatInterface(
                    fn=query_supervisor_agent,
                    chatbot=gr.Chatbot(height=400, label="", elem_id="chat-messages"),
                    textbox=gr.Textbox(placeholder="Ask about property sales, prices, trends, agents...", elem_id="chat-input", lines=2),
                    examples=[
                        "What is the average sale price in Mumbai?",
                        "Who is the top performing agent by sales volume?",
                        "How many 3BHK properties are currently available?",
                        "Show me monthly sales trends by city for 2024",
                        "Is a property priced at 80,00,000 considered luxury?",
                        "Did a property that sold in 15 days sell fast?",
                    ],
                )
        with gr.Tab("🏠 Properties"):
            gr.HTML("<div id='hero'><h1>Featured Properties</h1><p>A glimpse of the properties in our TENETIC database.</p></div>")
            gr.HTML(gallery_html)
            gr.HTML(stats_html)
        with gr.Tab("ℹ️ About"):
            gr.HTML(about_html)
    gr.HTML(footer_html)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False, show_error=True)