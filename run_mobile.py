"""
AgriMate AI - Direct Mobile Device Launcher
Starts FastAPI backend, serves responsive mobile app on port 8080,
reverses ADB ports, and launches the app directly on the connected phone screen.
"""

import os
import sys
import time
import subprocess
import threading
import http.server
import socketserver

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ADB_PATH = r"C:\Users\SMART TECH\AppData\Local\Android\Sdk\platform-tools\adb.exe"
WEB_DIR = r"c:\Users\SMART TECH\Desktop\AgriMateAI\frontend\mobile_web"
BACKEND_DIR = r"c:\Users\SMART TECH\Desktop\AgriMateAI\backend"


class SilentHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)
        
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def log_message(self, format, *args):
        pass


def start_web_server():
    with socketserver.TCPServer(("", 8080), SilentHTTPHandler) as httpd:
        httpd.serve_forever()


def start_fastapi_backend():
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], cwd=BACKEND_DIR)


def main():
    print("=" * 60)
    print("LAUNCHING AGRIMATE AI DIRECTLY ON CONNECTED MOBILE DEVICE")
    print("=" * 60)

    # 1. Start FastAPI backend in background thread
    print("\n[1/4] Starting FastAPI backend on port 8000...")
    backend_thread = threading.Thread(target=start_fastapi_backend, daemon=True)
    backend_thread.start()
    time.sleep(1.5)

    # 2. Start Mobile Web Server in background thread
    print("[2/4] Starting Mobile App Server on port 8080...")
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    time.sleep(1.0)

    # 3. Configure ADB port reversal
    print("[3/4] Configuring ADB USB reverse ports (8000 & 8080)...")
    try:
        subprocess.run([ADB_PATH, "reverse", "tcp:8000", "tcp:8000"], capture_output=True, text=True, check=True)
        subprocess.run([ADB_PATH, "reverse", "tcp:8080", "tcp:8080"], capture_output=True, text=True, check=True)
        print("  [OK] Reversed tcp:8000 and tcp:8080 to mobile device via USB.")
    except Exception as e:
        print(f"  [WARN] ADB reverse warning: {e}")

    # 4. Trigger intent on mobile phone
    print("[4/4] Opening AgriMate directly on your mobile screen...")
    target_url = "http://localhost:8080"
    try:
        result = subprocess.run(
            [ADB_PATH, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", target_url],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"  [INTENT DISPATCHED]: {result.stdout.strip()}")
        print("\n" + "=" * 60)
        print("SUCCESS! LOOK AT YOUR MOBILE PHONE SCREEN NOW!")
        print("AgriMate AI is live on your device with all three screens,")
        print("interactive navigation, and connected to the FastAPI backend.")
        print("=" * 60)
    except Exception as e:
        print(f"  [ERROR] Failed to launch intent: {e}")

    # Keep server running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping mobile runner...")


if __name__ == "__main__":
    main()
