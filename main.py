import streamlit as st
from ai import get_ai_response
from dotenv import load_dotenv
import os
from database import init_db, create_chat, add_message, get_messages, get_all_chats, delete_all_chats

# PAGE CONFIG MUST BE FIRST
st.set_page_config(
    page_title="Pepper",
    page_icon="⚡",
    layout="wide"
)

load_dotenv()

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

init_db()

# CUSTOM CSS
st.markdown("""
<style>

.block-container {
    padding-top: 0.8rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.main-title {
    position: relative;
    top: 23px;
    left: -5px;
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 25px;
    color: white;
}

section[data-testid="stSidebar"] > div {
    padding-top: 0px;
    padding-left: 10px;
    padding-right: 10px;
}

.sidebar-title {
    position: relative;
    top: 0px;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 0px;
    margin-top: -12px;
    color: white;
}

[data-testid="stChatInput"] {
    max-width: 750px !important;
    margin: 0 auto !important;
}

[data-testid="stChatInputSubmitButton"] button,
[data-testid="stChatInputSubmitButton"] {
    background-color: #ff4b4b !important;
    border-radius: 50% !important;
    color: white !important;
}

[data-testid="stSidebar"] label {
    font-size: 20px !important;
    color: white !important;
}

[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    flex-direction: row-reverse !important;
    text-align: right !important;
    margin-left: auto !important;
}

[data-testid="stChatMessage"] {
    width: fit-content !important;
    max-width: 70% !important;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚡ Pepper</div>',
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 8px 0; border-color: #333;'>", unsafe_allow_html=True)

    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.rerun()

    st.markdown("<hr style='margin: 8px 0; border-color: #333;'>", unsafe_allow_html=True)

    if st.button("🗑️ Clear All Chats", use_container_width=True):
        delete_all_chats()
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.rerun()

    st.markdown("<hr style='margin: 8px 0; border-color: #333;'>", unsafe_allow_html=True)

    st.markdown("**Previous Chats**")
    chats = get_all_chats()
    for chat in chats:
        if st.button(chat[1], key=f"chat_{chat[0]}", use_container_width=True):
            st.session_state.chat_id = chat[0]
            st.session_state.messages = get_messages(chat[0])
            st.rerun()

    st.markdown("<hr style='margin: 8px 0; border-color: #333;'>", unsafe_allow_html=True)

    model = st.selectbox(
        "Choose Model",
        [
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "gemma2-9b-it"
        ]
    )


# MAIN HEADER
st.markdown("""
<div class="main-title">
    ⚡ Pepper
</div>
""", unsafe_allow_html=True)

# DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# CHAT INPUT
user_input = st.chat_input("Your Text here")

if user_input:
    # Create new chat if none exists
    if st.session_state.chat_id is None:
        st.session_state.chat_id = create_chat(user_input[:30])

    # Add and show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    add_message(st.session_state.chat_id, "user", user_input)

    with st.chat_message("user"):
        st.markdown(user_input)

    # Stream AI reply
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_reply = ""

        for chunk in get_ai_response(st.session_state.messages, model, 0.7):
            full_reply += chunk
            response_placeholder.markdown(full_reply + "▌")

        response_placeholder.markdown(full_reply)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_reply
    })
    add_message(st.session_state.chat_id, "assistant", full_reply)
