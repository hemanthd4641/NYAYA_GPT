# app.py

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from crew import legal_assistant_crew
from tools.utils.pdf_generator import generate_legal_pdf
from tools.utils.voice_handler import transcribe_audio
from tools.utils.file_processor import extract_text_from_pdf, analyze_image_with_groq
from tools.utils.history_manager import (
    init_db, create_session, save_message,
    get_all_sessions, get_messages, delete_session, update_session_title,
    store_uploaded_document
)
import database.chat_repository as repo
from streamlit_mic_recorder import mic_recorder

load_dotenv()
init_db()  # Initialize database mapping (no-op on Supabase)

st.set_page_config(page_title="AI Legal Assistant", page_icon="⚖️", layout="wide")

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar & Authentication
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚖️ AI Legal Assistant")
    st.divider()

    st.markdown("### 👤 User Account")
    email_input = st.text_input("Enter Email to Login/Register:", value="guest@example.com")
    
    # Trigger authentication if email changes or not set yet
    if "user_email" not in st.session_state or st.session_state.user_email != email_input:
        st.session_state.user_email = email_input
        with st.spinner("Authenticating user..."):
            try:
                st.session_state.supabase_client = repo.get_authenticated_client(email_input)
                st.session_state.user_id = repo.get_or_create_user(email_input)["id"]
                st.session_state.current_session_id = None
                st.session_state.messages = []
                st.session_state.legal_result = None
                st.toast(f"Logged in as {email_input}", icon="👤")
            except Exception as e:
                st.error(f"Authentication failed: {e}")
                st.stop()

    st.divider()

    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        st.session_state.current_session_id = None
        st.session_state.messages = []
        st.session_state.legal_result = None
        st.rerun()

    st.markdown("### 📂 Chat History")

    # Load sessions from Supabase
    all_sessions = get_all_sessions()
    if not all_sessions:
        st.caption("No previous conversations yet.")
    else:
        for session in all_sessions:
            col1, col2 = st.columns([5, 1])
            with col1:
                # Format timestamps
                try:
                    dt = datetime.fromisoformat(session["created_at"].replace("Z", "+00:00"))
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


# ─────────────────────────────────────────────────────────────────────────────
# Initialize Session State
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
st.markdown(f"Conversational legal aid at your fingertips. Active User: **{st.session_state.user_email}**")

# Display chat messages from current session
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Voice and Document Input
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    audio = mic_recorder(
        start_prompt="🎤 Voice Record",
        stop_prompt="🛑 Stop Recording",
        just_once=True,
        key="recorder"
    )

with col2:
    with st.popover("📎 Attach Files"):
        uploaded_files = st.file_uploader(
            "Upload PDF documents or Image evidence:",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True
        )
        if uploaded_files:
            st.success(f"{len(uploaded_files)} file(s) uploaded.")
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
                # Log upload to database under active session
                store_uploaded_document(
                    session_id=st.session_state.current_session_id,
                    file_name=uploaded_file.name,
                    file_type=uploaded_file.type
                )
                
                if uploaded_file.type == "application/pdf":
                    st.write(f"Extracting text from {uploaded_file.name}...")
                    file_context += f"\n[Document: {uploaded_file.name}]\n" + extract_text_from_pdf(uploaded_file)
                else:
                    st.write(f"Analyzing image {uploaded_file.name}...")
                    file_context += f"\n[Evidence Image: {uploaded_file.name}]\n" + analyze_image_with_groq(uploaded_file.read(), uploaded_file.type)
            status.update(label="✅ Files processed", state="complete")

    # Run Legal Crew
    with st.chat_message("assistant"):
        with st.status("⚖️ Analyzing your case across multiple Acts...", expanded=True) as status:
            def task_completed_callback(output):
                agent_name = output.agent if output.agent else "Legal Agent"
                st.markdown(f"---")
                st.markdown(f"### 🤖 {agent_name}")
                st.markdown(output.raw)

            # Register callback dynamically
            legal_assistant_crew.task_callback = task_completed_callback

            full_input = f"{prompt}\n\n{file_context}"
            try:
                result = legal_assistant_crew.kickoff(inputs={"user_input": full_input})
                response = result if isinstance(result, str) else str(result)
                status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
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
                status.update(label="❌ Analysis Failed", state="error", expanded=True)

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
