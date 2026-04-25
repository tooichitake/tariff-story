"""Launch the Streamlit app from project root."""
import subprocess
import sys
import os

app_path = os.path.join(os.path.dirname(__file__), "app", "app.py")
subprocess.run([sys.executable, "-m", "streamlit", "run", app_path])
