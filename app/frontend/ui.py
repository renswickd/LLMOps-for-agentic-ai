import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Customizable Multi-Agent Chatbot", layout="wide")
st.markdown(
    """
    <style>
    .template-card {
        background: #f6f9fc;
        border-radius: 10px;
        padding: 1.2em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
        border-left: 5px solid #4F8BF9;
    }
    .template-title {
        font-weight: bold;
        color: #4F8BF9;
        margin-bottom: 0.3em;
    }
    .template-desc {
        color: #333;
        font-size: 0.97em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        "title": "Helpful Assistant",
        "prompt": "You are a helpful assistant. Answer questions clearly and concisely.",
        "desc": "General-purpose assistant for any topic."
    },
    {
        "title": "Creative Storyteller",
        "prompt": "You are a creative storyteller. Write imaginative and engaging stories based on user input.",
        "desc": "Great for generating stories, poems, or creative writing."
    },
    {
        "title": "Technical Expert",
        "prompt": "You are a technical expert. Provide detailed and accurate technical explanations.",
        "desc": "Ideal for coding, engineering, or scientific queries."
    },
    {
        "title": "Motivational Coach",
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

# System prompt input
system_prompt = st.text_area(
    "📝 Define your AI Agent (System Prompt):",
    height=70,
    key="system_prompt",
    value=st.session_state.get("system_prompt", "")
)
selected_model = st.selectbox("🤖 Select your AI model:", settings.ALLOWED_MODEL_NAMES)
allow_web_search = st.checkbox("🌐 Allow web search")

st.markdown("---")
st.markdown("#### 💬 Chat with your Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_area("Your message:", height=100, key="user_query")

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Send") and user_query.strip():
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

# Display chat history in a modern chat layout
if st.session_state.chat_history:
    st.markdown("#### 🗨️ Conversation")
    for sender, message in st.session_state.chat_history:
        if sender == "user":
            st.markdown(
                f"<div style='background:#e3f2fd;padding:0.7em 1em;border-radius:8px;margin-bottom:0.5em;text-align:right;'><b>You:</b> {message}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background:#f1f8e9;padding:0.7em 1em;border-radius:8px;margin-bottom:0.5em;text-align:left;'><b>Agent:</b> {message}</div>",
                unsafe_allow_html=True,
            )