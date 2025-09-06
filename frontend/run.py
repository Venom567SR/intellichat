#!/usr/bin/env python3
"""
IntelliSupport Streamlit Runner
Main entry point for the Streamlit application
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit application"""
    
    # Change to the frontend directory
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    # Run Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "localhost",
        "--theme.primaryColor", "#3b82f6",
        "--theme.backgroundColor", "#ffffff",
        "--theme.secondaryBackgroundColor", "#f3f4f6"
    ]
    
    print("🚀 Starting IntelliSupport Streamlit Frontend...")
    print("📍 URL: http://localhost:8501")
    print("🔧 Use Ctrl+C to stop the server")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("
👋 IntelliSupport stopped.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
