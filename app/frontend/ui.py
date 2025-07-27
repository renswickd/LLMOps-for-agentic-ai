import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Customizable Multi-Agent Chatbot", layout="wide")

DEBUG = True

# --- Custom CSS for scrollable chat and beautiful templates ---
st.markdown("""
    <style>
    .scrollable-chat {
        height: 400px;
        overflow-y: auto;
        padding-right: 10px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        background: #f8fafc;
        margin-bottom: 1em;
    }
    .template-card {
        background: linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%);
        border-radius: 14px;
        padding: 1.2em 1em 1em 1em;
        margin-bottom: 1.2em;
        box-shadow: 0 2px 12px rgba(80,120,255,0.07);
        border-left: 6px solid #6366f1;
        transition: box-shadow 0.2s;
    }
    .template-card:hover {
        box-shadow: 0 4px 24px rgba(80,120,255,0.13);
        border-left: 6px solid #22d3ee;
    }
    .template-title {
        font-weight: bold;
        color: #6366f1;
        font-size: 1.1em;
        margin-bottom: 0.2em;
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    .template-desc {
        color: #334155;
        font-size: 0.97em;
        margin-bottom: 0.7em;
    }
    .template-btn {
        background: #6366f1;
        color: #fff;
        border: none;
        padding: 0.4em 1.1em;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.97em;
        transition: background 0.2s;
    }
    .template-btn:hover {
        background: #22d3ee;
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Area: Heading, Subheading, Templates ---
with st.container():
    st.title("🧠 Customizable Multi-Agent Chatbot")
    st.markdown(
        """
        Welcome to the **Customizable Multi-Agent Chatbot**!  
        Define your agent's behavior using a system prompt, select a model, and interact with your AI agent.  
        Use a template below or write your own system prompt to create a unique chatbot persona.
        """
    )

    # Example/template system prompts
    template_prompts = [
        {
            "title": "🦾 Helpful Assistant",
            "prompt": "You are a helpful assistant. Answer questions clearly and concisely.",
            "desc": "General-purpose assistant for any topic."
        },
        {
            "title": "🎨 Creative Storyteller",
            "prompt": "You are a creative storyteller. Write imaginative and engaging stories based on user input.",
            "desc": "Great for generating stories, poems, or creative writing."
        },
        {
            "title": "💡 Technical Expert",
            "prompt": "You are a technical expert. Provide detailed and accurate technical explanations.",
            "desc": "Ideal for coding, engineering, or scientific queries."
        },
        {
            "title": "🌱 Motivational Coach",
            "prompt": "You are a motivational coach. Encourage and inspire users with positive advice.",
            "desc": "Perfect for wellness, productivity, and personal growth."
        }
    ]

    st.markdown("#### 🎨 Example System Prompts")
    cols = st.columns(len(template_prompts))
    for idx, t in enumerate(template_prompts):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="template-card">
                    <div class="template-title">{t['title']}</div>
                    <div class="template-desc">{t['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Use Template: {t['title']}", key=f"use_{idx}"):
                st.session_state.system_prompt = t['prompt']

# --- Sidebar: User Inputs ---
with st.sidebar:
    st.header("🛠️ Configure Your Agent")
    system_prompt = st.text_area(
        "📝 System Prompt",
        height=70,
        key="system_prompt",
        value=st.session_state.get("system_prompt", "")
    )
    selected_model = st.selectbox("🤖 Select your AI model:", settings.ALLOWED_MODEL_NAMES)

# --- Chat State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

API_URL = "http://127.0.0.1:9999/chat"

# --- User Query Input at Bottom ---
with st.container():
    # st.markdown("---")
    with st.form(key="chat_form", clear_on_submit=True):
        user_query = st.text_area("💬 Your message:", height=100, key="user_query", label_visibility="visible")
        allow_web_search = st.checkbox("🌐 Allow web search", key="allow_search")
        send_btn = st.form_submit_button("Send")

        if send_btn and user_query.strip():
            payload = {
                "model_name": selected_model,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_web_search
            }
            try:
                logger.info("Sending request to backend")
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    agent_response = response.json().get("response", "")
                    logger.info("Successfully received response from backend")
                    st.session_state.chat_history.append(("user", user_query))
                    st.session_state.chat_history.append(("agent", agent_response))
                else:
                    logger.error("Backend error")
                    st.error("Error with backend")
            except Exception as e:
                logger.error("Error occurred while sending request to backend")
                st.error(str(CustomException("Failed to communicate to backend")))

# --- Conversation Panel (Scrollable, Below User Query) ---
with st.container():
    # st.markdown("---")
    st.markdown("#### 🗨️ Conversation")
    chat_html = "<div class='scrollable-chat'>"
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            chat_html += (
                f"<div style='display:flex;justify-content:flex-end;'>"
                f"<div style='background:#e3f2fd;padding:0.9em 1.2em;border-radius:16px 16px 4px 16px;margin-bottom:0.5em;max-width:70%;'>"
                f"<b>You:</b> {message}"
                f"</div></div>"
            )
        else:
            chat_html += (
                f"<div style='display:flex;justify-content:flex-start;'>"
                f"<div style='background:#f1f8e9;padding:0.9em 1.2em;border-radius:16px 16px 16px 4px;margin-bottom:0.5em;max-width:70%;'>"
                f"<b>Agent:</b> {message}"
                f"</div></div>"
            )
    chat_html += "</div>"
    st.markdown(chat_html, unsafe_allow_html=True)