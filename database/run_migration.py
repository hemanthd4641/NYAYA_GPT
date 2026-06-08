# database/run_migration.py

import os
import getpass
import urllib.parse
import psycopg2
from dotenv import load_dotenv

def run_migration():
    load_dotenv()
    
    supabase_url = os.getenv("SUPABASE_URL")
    if not supabase_url:
        print("❌ Error: SUPABASE_URL not found in .env file.")
        return
        
    try:
        project_ref = urllib.parse.urlparse(supabase_url).netloc.split(".")[0]
    except Exception as e:
        print(f"❌ Error parsing SUPABASE_URL: {e}")
        return

    host = f"db.{project_ref}.supabase.co"
    database = "postgres"
    user = "postgres"
    port = "5432"

    print("=" * 60)
    print("      NYAYA_GPT Supabase PostgreSQL Database Migrator")
    print("=" * 60)
    print(f"Connecting to Host : {host}")
    print(f"Database Name     : {database}")
    print(f"Database User     : {user}")
    print(f"Port              : {port}")
    print("-" * 60)
    print("Note: Your Supabase database password was set when you created the project.")
    print("It is separate from your API keys / dashboard login.")
    print("-" * 60)
    
    db_password = getpass.getpass("🔑 Enter your Supabase Database Password: ").strip()
    if not db_password:
        print("❌ Error: Password cannot be empty.")
        return

    # Load schema SQL
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if not os.path.exists(schema_path):
        print(f"❌ Error: schema.sql file not found at {schema_path}")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        sql_commands = f.read()

    print("\n⏳ Connecting to PostgreSQL database...")
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=db_password,
            port=port
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("⚡ Executing SQL schema migrations...")
        cursor.execute(sql_commands)
        
        print("🎉 Database schema, sync triggers, and RLS policies created successfully!")
        cursor.close()
        conn.close()
    except psycopg2.OperationalError as op_err:
        print(f"\n❌ Connection failed: {op_err}")
        print("Verify your password and check if connection port 5432 is allowed by your network.")
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
