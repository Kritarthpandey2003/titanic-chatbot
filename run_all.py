import subprocess
import os
import sys
import time

def main():
    print("🚢 Starting Titanic Chatbot Full Stack...")
    
    # Check if .env has the API key
    if not os.path.exists(".env"):
        print("Creating default .env file...")
        with open(".env", "w") as f:
            f.write('GEMINI_API_KEY="your_api_key_here"\n')
        print("⚠️ PLEASE EDIT .env AND ADD YOUR GEMINI API KEY BEFORE RUNNING!")
        return

    # Start FastAPI Backend
    print("Starting FastAPI Backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"]
    )
    
    time.sleep(3) # Wait for backend to initialize
    
    # Start Streamlit Frontend
    print("Starting Streamlit Frontend...")
    frontend_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py", 
         "--server.enableCORS=false", 
         "--server.enableXsrfProtection=false", 
         "--browser.gatherUsageStats=false",
         "--server.address=0.0.0.0",
         "--server.headless=true"],
    )

    try:
        print("\n✅ Both servers are running! Press Ctrl+C to stop.")
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
