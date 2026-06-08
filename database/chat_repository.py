# database/chat_repository.py

import logging
import hashlib
import time
from supabase import Client
from database.supabase_client import get_supabase_client, get_supabase_admin_client

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def _get_password_for_email(email: str) -> str:
    """Generate a secure, deterministic password for a given email address."""
    hashed = hashlib.sha256(email.lower().encode("utf-8")).hexdigest()[:12]
    return f"NyayaGPT_{hashed}!"

def get_or_create_user(email: str) -> dict:
    """
    Looks up a user by email, creating them via Supabase Admin Client
    if they do not exist. Automatically confirms their email to bypass OTP/verification.
    """
    email_clean = email.strip().lower()
    admin_client = get_supabase_admin_client()
    
    # Check if user already exists in public.users table
    try:
        response = admin_client.table("users").select("*").eq("email", email_clean).execute()
        if response.data:
            logger.info(f"User {email_clean} found in public.users.")
            return response.data[0]
    except Exception as e:
        logger.error(f"Error checking public.users table for email {email_clean}: {e}")

    # Create the user in auth schema using Admin auth client
    logger.info(f"User {email_clean} not found. Registering new user...")
    password = _get_password_for_email(email_clean)
    try:
        user_resp = admin_client.auth.admin.create_user({
            "email": email_clean,
            "password": password,
            "email_confirm": True
        })
        user_id = user_resp.user.id
        logger.info(f"User {email_clean} registered successfully with ID: {user_id}")
        
        # Wait up to 3 seconds for public trigger to sync user row
        for _ in range(3):
            time.sleep(1)
            response = admin_client.table("users").select("*").eq("id", user_id).execute()
            if response.data:
                logger.info("Public sync trigger completed successfully.")
                return response.data[0]
                
        # Fallback in case sync trigger didn't run or was slow
        fallback_user = {"id": user_id, "email": email_clean}
        logger.warning(f"Trigger delay. Returning fallback dictionary: {fallback_user}")
        return fallback_user
    except Exception as e:
        logger.error(f"Failed to register new user {email_clean}: {e}")
        raise e

def get_authenticated_client(email: str) -> Client:
    """
    Returns an authenticated user-level client.
    Ensures Row Level Security (RLS) is applied on all queries made by this client.
    """
    email_clean = email.strip().lower()
    client = get_supabase_client()
    password = _get_password_for_email(email_clean)
    
    try:
        client.auth.sign_in_with_password({"email": email_clean, "password": password})
        logger.info(f"Successfully authenticated client for {email_clean}.")
        return client
    except Exception as e:
        # If authentication fails, create user first and try again
        logger.warning(f"Authentication failed for {email_clean}: {e}. Creating user and retrying...")
        get_or_create_user(email_clean)
        try:
            client.auth.sign_in_with_password({"email": email_clean, "password": password})
            logger.info(f"Successfully authenticated client for {email_clean} on retry.")
            return client
        except Exception as retry_err:
            logger.error(f"Critical authentication failure for {email_clean}: {retry_err}")
            raise retry_err

def retry_operation(operation, *args, retries=3, delay=1, **kwargs):
    """Utility function to retry Supabase queries on failure."""
    last_err = None
    for attempt in range(retries):
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            last_err = e
            logger.warning(f"Supabase operation failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay)
    logger.error(f"Supabase operation permanently failed after {retries} retries.")
    raise last_err

# --- Repository CRUD Actions ---

def list_sessions(client: Client) -> list[dict]:
    """Retrieves all chat sessions for the authenticated user, ordered by date."""
    def _action():
        response = client.table("chat_sessions").select("*").order("created_at", desc=True).execute()
        return response.data
    return retry_operation(_action)

def create_session(client: Client, user_id: str, title: str) -> str:
    """Creates a new chat session and returns its UUID."""
    def _action():
        response = client.table("chat_sessions").insert({
            "user_id": user_id,
            "title": title
        }).execute()
        return response.data[0]["id"]
    return retry_operation(_action)

def delete_session(client: Client, session_id: str):
    """Deletes a chat session and all associated cascade items."""
    def _action():
        client.table("chat_sessions").delete().eq("id", session_id).execute()
    retry_operation(_action)

def update_session_title(client: Client, session_id: str, title: str):
    """Updates the title of a specific chat session."""
    def _action():
        client.table("chat_sessions").update({"title": title}).eq("id", session_id).execute()
    retry_operation(_action)

def save_message(client: Client, session_id: str, role: str, content: str):
    """Saves a message to the database."""
    def _action():
        client.table("chat_messages").insert({
            "session_id": session_id,
            "role": role,
            "content": content
        }).execute()
    retry_operation(_action)

def get_session_messages(client: Client, session_id: str) -> list[dict]:
    """Retrieves all messages for a given session sorted chronologically."""
    def _action():
        response = client.table("chat_messages").select("role, content").eq("session_id", session_id).order("timestamp", desc=False).execute()
        return response.data
    return retry_operation(_action)

def store_uploaded_document(client: Client, session_id: str, file_name: str, file_type: str):
    """Registers an uploaded document under a specific chat session."""
    def _action():
        client.table("uploaded_documents").insert({
            "session_id": session_id,
            "file_name": file_name,
            "file_type": file_type
        }).execute()
    retry_operation(_action)
