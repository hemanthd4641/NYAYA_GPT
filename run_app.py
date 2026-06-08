"""Simple launcher script to start the Streamlit app."""
import subprocess
import sys
import os

if __name__ == "__main__":
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], env=env)
