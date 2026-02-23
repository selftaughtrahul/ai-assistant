import streamlit as st
import requests
import uuid

# Configuration
API_URL = "http://localhost:8000/api/v1/chat"

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .chat-container {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .user-msg {
        background-color: #2b313e;
        color: #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        margin-left: auto;
        margin-right: 0;
        width: fit-content;
        max-width: 80%;
    }
    .bot-msg {
        background-color: #1a1c23;
        color: #e0e0e0;
        border-radius: 10px;
        padding: 10px;
        margin-left: 0;
        margin-right: auto;
        width: fit-content;
        max-width: 80%;
        border-left: 4px solid #4CAF50;
    }
    .escalated-msg {
        background-color: #ffebee;
        color: #c62828;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        text-align: center;
        border: 2px solid #ef5350;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    # First message from bot
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Support Assistant. How can I help you today?", "escalated": False}
    ]

if "is_escalated" not in st.session_state:
    st.session_state.is_escalated = False

st.title("🤖 Customer Support Chatbot")
st.markdown("---")

# Display Escalation Warning
if st.session_state.is_escalated:
    st.markdown('<div class="escalated-msg">⚠️ You have been escalated to a Human Agent. An agent will join this chat shortly.</div>', unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# User Input
if not st.session_state.is_escalated:
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add User Message to UI
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        # Send to FastAPI
        with st.spinner("Thinking..."):
            try:
                # Add LLM provider explicitly to requests payload
                provider_map = {
                    "Groq (LLaMA3)": "groq", 
                    "Google Gemini": "gemini", 
                    "Hugging Face (Remote)": "huggingface"
                }

                response = requests.post(
                    API_URL, 
                    json={
                        "session_id": st.session_state.session_id, 
                        "text": user_input, 
                        "provider": provider_map.get(st.session_state.get('selected_provider', "Groq (LLaMA3)"))
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "Sorry, I had trouble processing that.")
                    escalated = data.get("escalated", False)
                    
                    # Add Bot Message to UI
                    st.session_state.messages.append({"role": "assistant", "content": reply, "escalated": escalated})
                    with st.chat_message("assistant"):
                        st.markdown(reply)
                    
                    # Handle Escalation State
                    if escalated:
                        st.session_state.is_escalated = True
                        st.rerun() # Refresh to show the warning banner
                else:
                    st.error(f"Error communicating with API: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Failed to connect to the backend! Make sure FastAPI is running (uvicorn main:app --reload)")
else:
    st.chat_input("Chat disabled while waiting for agent.", disabled=True)
    
# Sidebar info for debugging
with st.sidebar:
    st.subheader("Model Selection")
    st.selectbox(
        "Choose an LLM Backend", 
        ["Groq (LLaMA3)", "Google Gemini", "Hugging Face (Remote)"], 
        key="selected_provider", 
        help="Select which provider the bot's generator should use under the hood."
    )
    
    st.markdown("---")
    st.subheader("Session Info")
    st.write(f"**Session ID:** `{st.session_state.session_id}`")
    st.write(f"**Status:** `{'Human Escalation' if st.session_state.is_escalated else 'Active AI'}`")
    if st.button("Restart Chat"):
        st.session_state.clear()
        st.rerun()
        
    st.markdown("---")
    st.subheader("Internal Database Access")
    st.write("Below is the mock data the system can automatically read & update:")
    
    import sqlite3
    import pandas as pd
    
    def fetch_table(table_name):
        conn = sqlite3.connect("company_data.db")
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
        
    try:
        tab1, tab2, tab3, tab4 = st.tabs(["Orders", "Demands", "Projects", "Resources"])
        
        with tab1:
             st.dataframe(fetch_table("orders"), use_container_width=True)
        with tab2:
             st.dataframe(fetch_table("demands"), use_container_width=True)
        with tab3:
             st.dataframe(fetch_table("projects"), use_container_width=True)
        with tab4:
             st.dataframe(fetch_table("resources"), use_container_width=True)
             
    except Exception as e:
        st.error(f"Cannot load database: {e}")
