# tools/history_manager.py
# Manages persistent conversation history using Supabase PostgreSQL.

import streamlit as st
import logging
import database.chat_repository as repo

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    """No-op function for backward compatibility. DB is initialized in the cloud."""
    pass

def _run_with_auth_refresh(func, *args, **kwargs):
    """Helper to run a repository function, automatically refreshing the JWT if expired."""
    client = st.session_state.get("supabase_client")
    if not client:
        raise ValueError("❌ User is not authenticated.")
    
    try:
        return func(client, *args, **kwargs)
    except Exception as e:
        if 'PGRST303' in str(e):
            logger.info("Supabase JWT expired. Re-authenticating automatically...")
            email = st.session_state.get("user_email")
            if email:
                new_client = repo.get_authenticated_client(email)
                st.session_state.supabase_client = new_client
                return func(new_client, *args, **kwargs)
        raise e

def create_session(title: str) -> str:
    """Create a new chat session in Supabase and return its UUID string."""
    user_id = st.session_state.get("user_id")
    if not user_id:
        raise ValueError("❌ User is not authenticated. Please log in first.")
    return _run_with_auth_refresh(repo.create_session, user_id, title)

def save_message(session_id: str, role: str, content: str):
    """Save a chat message to Supabase."""
    _run_with_auth_refresh(repo.save_message, session_id, role, content)

def get_all_sessions() -> list[dict]:
    """Return all sessions for the authenticated user, ordered by most recent."""
    try:
        return _run_with_auth_refresh(repo.list_sessions)
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        return []

def get_messages(session_id: str) -> list[dict]:
    """Return all messages for a given session."""
    try:
        return _run_with_auth_refresh(repo.get_session_messages, session_id)
    except Exception as e:
        logger.error(f"Error loading messages for session {session_id}: {e}")
        return []

def delete_session(session_id: str):
    """Delete a session and all its messages."""
    try:
        _run_with_auth_refresh(repo.delete_session, session_id)
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")

def update_session_title(session_id: str, title: str):
    """Update the title of a session."""
    try:
        _run_with_auth_refresh(repo.update_session_title, session_id, title)
    except Exception as e:
        logger.error(f"Error updating title for session {session_id}: {e}")

def store_uploaded_document(session_id: str, file_name: str, file_type: str):
    """Log an uploaded document under the active session."""
    try:
        _run_with_auth_refresh(repo.store_uploaded_document, session_id, file_name, file_type)
        logger.info(f"Registered uploaded file {file_name} under session {session_id}")
    except Exception as e:
        logger.error(f"Error storing uploaded document record {file_name}: {e}")
