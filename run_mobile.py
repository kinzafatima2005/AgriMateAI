"""
AgriMate AI - Persistent Mobile & Backend Runner with Auto-Reconnecting Watchdog
Runs FastAPI backend on 0.0.0.0:8000, detects Wi-Fi LAN IP, serves mobile web,
and maintains an active USB Watchdog that re-applies ADB reverse automatically
whenever the mobile phone is plugged in or wakes up.
"""

import os
import sys
import time
import socket
import subprocess
import threading
import http.server
import socketserver

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ADB_PATH = r"C:\Users\SMART TECH\AppData\Local\Android\Sdk\platform-tools\adb.exe"
WEB_DIR = r"c:\Users\SMART TECH\Desktop\AgriMateAI\frontend\mobile_web"
BACKEND_DIR = r"c:\Users\SMART TECH\Desktop\AgriMateAI\backend"


def get_local_lan_ip():
    """Detects active Wi-Fi / Ethernet LAN IP of the host computer."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '192.168.1.14'


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
    """Serves mobile web application on port 8080."""
    try:
        with socketserver.TCPServer(("0.0.0.0", 8080), SilentHTTPHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"[Web Server Note] {e}")


def start_fastapi_backend():
    """Runs FastAPI backend with uvicorn on 0.0.0.0:8000."""
    while True:
        try:
            print("\n[FastAPI] Starting Uvicorn on 0.0.0.0:8000...")
            subprocess.run(
                [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
                cwd=BACKEND_DIR
            )
        except Exception as e:
            print(f"[FastAPI Crash Guard] Uvicorn exited: {e}. Restarting in 2s...")
            time.sleep(2)


def adb_watchdog_loop():
    """
    Continuous watchdog that monitors USB connected devices every 3 seconds.
    If device is connected and port reverse is lost (due to disconnect or phone sleep),
    it immediately re-applies adb reverse tcp:8000 and tcp:8080!
    """
    last_state = False
    while True:
        try:
            res = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True)
            devices = [line.split()[0] for line in res.stdout.strip().splitlines() if "\tdevice" in line]
            if devices:
                rev = subprocess.run([ADB_PATH, "reverse", "--list"], capture_output=True, text=True)
                if "tcp:8000" not in rev.stdout:
                    subprocess.run([ADB_PATH, "reverse", "tcp:8000", "tcp:8000"], capture_output=True)
                    subprocess.run([ADB_PATH, "reverse", "tcp:8080", "tcp:8080"], capture_output=True)
                    print(f"\n[USB WATCHDOG] Phone detected ({devices[0]})! Restored ADB reverse ports 8000 & 8080.")
                    last_state = True
            else:
                if last_state:
                    print("\n[USB WATCHDOG] Phone disconnected. Waiting for reconnection...")
                    last_state = False
        except Exception:
            pass
        time.sleep(3)


def main():
    lan_ip = get_local_lan_ip()

    print("=" * 65)
    print("      AGRIMATE AI - PERSISTENT MULTI-CHANNEL SERVER")
    print("=" * 65)
    print(f"  [1] Wi-Fi LAN Address:   http://{lan_ip}:8000")
    print(f"  [2] USB / ADB Loopback:  http://127.0.0.1:8000")
    print(f"  [3] Mobile Web Portal:   http://{lan_ip}:8080")
    print("=" * 65)

    # 1. Start FastAPI backend
    backend_thread = threading.Thread(target=start_fastapi_backend, daemon=True)
    backend_thread.start()
    time.sleep(1.5)

    # 2. Start Mobile Web Server
    web_thread = threading.Thread(target=start_web_server, daemon=True)
    web_thread.start()
    time.sleep(1.0)

    # 3. Start ADB Watchdog Thread
    watchdog_thread = threading.Thread(target=adb_watchdog_loop, daemon=True)
    watchdog_thread.start()

    # 4. Initial port reverse and app launch
    try:
        subprocess.run([ADB_PATH, "reverse", "tcp:8000", "tcp:8000"], capture_output=True)
        subprocess.run([ADB_PATH, "reverse", "tcp:8080", "tcp:8080"], capture_output=True)
        # Bring native APK to front
        subprocess.run([ADB_PATH, "shell", "am", "start", "-n", "pk.agrimate.ai/.MainActivity"], capture_output=True)
        print("  [OK] Initialized USB reverse and launched AgriMate AI native app on phone.")
    except Exception as e:
        print(f"  [Note] ADB initial launch: {e}")

    print("\n[SERVER ACTIVE] Server is running permanently. Press CTRL+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping AgriMate AI runner...")


if __name__ == "__main__":
    main()
