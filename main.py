import streamlit as st
import groq
from dotenv import load_dotenv
import os

# PAGE CONFIG MUST BE FIRST
st.set_page_config(
    page_title="Pepper",
    page_icon="⚡",
    layout="wide"
)

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

client = groq.Groq(api_key=api_key)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# CUSTOM CSS
st.markdown("""
<style>

/* Remove Streamlit top spacing */
.block-container {
    padding-top: 0.8rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* MAIN TITLE */
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

/* SIDEBAR TITLE */
.sidebar-title {
    position: relative;
    top: 0px;
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 0px;
    margin-top: -12px;
    color: white;
}

/* Sidebar padding */
section[data-testid="stSidebar"] > div {
    padding-top: 0px;
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

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚡ Pepper</div>',
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 5px 2; border-color: #333;'>", unsafe_allow_html=True)

    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("<hr style='margin: 5px 0; border-color: #333;'>", unsafe_allow_html=True)

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
        st.write(message["content"])

# CHAT INPUT
user_input = st.chat_input("Your Text here")

if user_input:

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    # Show assistant response
    with st.chat_message("assistant"):
        st.write(reply)