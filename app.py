# app.py

import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from crew import legal_assistant_crew
from tools.pdf_generator import generate_legal_pdf
from tools.voice_handler import transcribe_audio
from tools.file_processor import extract_text_from_pdf, analyze_image_with_groq
from tools.history_manager import (
    init_db, create_session, save_message,
    get_all_sessions, get_messages, delete_session, update_session_title
)
from streamlit_mic_recorder import mic_recorder

load_dotenv()
init_db()  # Initialize SQLite database on startup

st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚖️ AI Legal Assistant")
    st.divider()

    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_session_id = None
        st.session_state.messages = []
        st.session_state.legal_result = None
        st.rerun()

    st.markdown("### 📂 Chat History")

    all_sessions = get_all_sessions()
    if not all_sessions:
        st.caption("No previous conversations yet.")
    else:
        for session in all_sessions:
            col1, col2 = st.columns([5, 1])
            with col1:
                # Format the last updated timestamp nicely
                try:
                    dt = datetime.fromisoformat(session["last_updated"])
                    label = f"{session['title'][:28]}{'...' if len(session['title']) > 28 else ''}"
                    caption = dt.strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    label = session["title"]
                    caption = ""

                if st.button(label, key=f"sess_{session['id']}", use_container_width=True, help=caption):
                    st.session_state.current_session_id = session["id"]
                    st.session_state.messages = get_messages(session["id"])
                    st.session_state.legal_result = None
                    # Find last assistant message as legal result
                    for msg in reversed(st.session_state.messages):
                        if msg["role"] == "assistant":
                            st.session_state.legal_result = msg["content"]
                            break
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"del_{session['id']}", help="Delete this conversation"):
                    delete_session(session["id"])
                    if st.session_state.get("current_session_id") == session["id"]:
                        st.session_state.current_session_id = None
                        st.session_state.messages = []
                        st.session_state.legal_result = None
                    st.rerun()

    st.divider()
    st.markdown("### 📁 Documents & Evidence")
    uploaded_files = st.file_uploader(
        "Upload PDF documents or Image evidence:",
        type=["pdf", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) uploaded.")

# ─────────────────────────────────────────────────────────────────────────────
# Initialize Session State (clears fresh on every new browser session)
# ─────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "legal_result" not in st.session_state:
    st.session_state.legal_result = None
if "current_session_id" not in st.session_state:
    st.session_state.current_session_id = None  # None = fresh chat

# ─────────────────────────────────────────────────────────────────────────────
# Main Chat Area
# ─────────────────────────────────────────────────────────────────────────────
st.title("⚖️ Personal AI Legal Assistant")
st.markdown("Conversational legal aid at your fingertips. Upload documents, speak, or type your issue.")

# Display chat messages from current session
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice Input
col1, col2 = st.columns([1, 4])
with col1:
    audio = mic_recorder(
        start_prompt="🎤 Record",
        stop_prompt="🛑 Stop",
        just_once=True,
        key="recorder"
    )

if audio:
    with st.spinner("🎧 Transcribing..."):
        transcription = transcribe_audio(audio['bytes'])
        if transcription and not transcription.startswith("Error"):
            user_msg = transcription
            # Create new session if needed
            if not st.session_state.current_session_id:
                title = user_msg[:50]
                st.session_state.current_session_id = create_session(title)
            save_message(st.session_state.current_session_id, "user", user_msg)
            st.session_state.messages.append({"role": "user", "content": user_msg})
            st.rerun()

# Chat Input
if prompt := st.chat_input("Describe your legal issue..."):
    # Create a new session if this is the first message
    if not st.session_state.current_session_id:
        title = prompt[:50]  # Use first 50 chars as title
        st.session_state.current_session_id = create_session(title)

    # Save and display user message
    save_message(st.session_state.current_session_id, "user", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process uploaded files
    file_context = ""
    if uploaded_files:
        with st.status("📄 Processing uploaded files...", expanded=False) as status:
            for uploaded_file in uploaded_files:
                if uploaded_file.type == "application/pdf":
                    st.write(f"Extracting text from {uploaded_file.name}...")
                    file_context += f"\n[Document: {uploaded_file.name}]\n" + extract_text_from_pdf(uploaded_file)
                else:
                    st.write(f"Analyzing image {uploaded_file.name}...")
                    file_context += f"\n[Evidence Image: {uploaded_file.name}]\n" + analyze_image_with_groq(uploaded_file.read(), uploaded_file.type)
            status.update(label="✅ Files processed", state="complete")

    # Run Legal Crew
    with st.chat_message("assistant"):
        with st.spinner("⚖️ Analyzing your case across multiple Acts..."):
            full_input = f"{prompt}\n\n{file_context}"
            try:
                result = legal_assistant_crew.kickoff(inputs={"user_input": full_input})
                response = result if isinstance(result, str) else str(result)
            except Exception as e:
                err = str(e)
                if "rate_limit_exceeded" in err or "429" in err:
                    response = (
                        "⚠️ **Rate Limit Reached**: The AI model has hit its daily token limit on the free tier. "
                        "Please wait **10-15 minutes** and try again. "
                        "\n\nAlternatively, you can upgrade your Groq account at "
                        "https://console.groq.com/settings/billing for higher limits."
                    )
                else:
                    response = f"❌ **An error occurred**: {err}"

            st.markdown(response)
            st.session_state.legal_result = response
            st.session_state.messages.append({"role": "assistant", "content": response})
            # Save assistant response to DB
            save_message(st.session_state.current_session_id, "assistant", response)

# ─────────────────────────────────────────────────────────────────────────────
# PDF Export
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.legal_result:
    st.divider()
    pdf_bytes = generate_legal_pdf(st.session_state.legal_result)
    st.download_button(
        label="📥 Download Official Legal Report (PDF)",
        data=pdf_bytes,
        file_name=f"legal_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )
