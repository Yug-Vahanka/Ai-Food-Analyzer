"""
Convenience runner — starts both the FastAPI backend and Streamlit frontend.

Usage:
    python run.py
"""
import subprocess
import sys

backend  = subprocess.Popen([sys.executable, "-m", "uvicorn", "app.main:app", "--reload"])
frontend = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    backend.terminate()
    frontend.terminate()
