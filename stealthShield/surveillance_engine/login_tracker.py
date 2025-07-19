# surveillance_engine/login_tracker.py
import subprocess
from datetime import datetime
import os
from alert_system.telegram_bot import send_alert

LOG_FILE = "logs/login_log.txt"

def track_logins():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    result = subprocess.run(['last', '-n', '5'], capture_output=True, text=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] Last 5 logins:\n{result.stdout}\n")
    send_alert(f"Last 5 logins:\n{result.stdout}")

if __name__ == "__main__":
    track_logins()
