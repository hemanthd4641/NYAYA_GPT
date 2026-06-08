# database/supabase_client.py

import os
import logging
from dotenv import load_dotenv
from supabase import create_client, Client

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def get_supabase_client() -> Client:
    """
    Returns a standard client initialized with the anonymous key.
    Ideal for client-facing operations that respect Row Level Security (RLS).
    """
    url = os.getenv("SUPABASE_URL")
    anon_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not anon_key:
        logger.error("SUPABASE_URL or SUPABASE_ANON_KEY is missing in the environment.")
        raise EnvironmentError("❌ SUPABASE_URL and SUPABASE_ANON_KEY environment variables are required.")
    
    try:
        return create_client(url, anon_key)
    except Exception as e:
        logger.error(f"Failed to initialize standard Supabase client: {e}")
        raise e

def get_supabase_admin_client() -> Client:
    """
    Returns a system-level client initialized with the service role key.
    This client bypasses Row Level Security (RLS) and is reserved for administrative tasks
    like syncing users or global indexing.
    """
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not url or not service_key:
        logger.error("SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY is missing in the environment.")
        raise EnvironmentError("❌ SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables are required.")
    
    try:
        return create_client(url, service_key)
    except Exception as e:
        logger.error(f"Failed to initialize admin Supabase client: {e}")
        raise e
