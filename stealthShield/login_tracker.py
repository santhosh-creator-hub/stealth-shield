# surveillance_engine/login_tracker.py
import subprocess
from datetime import datetime

LOG_FILE = "logs/login_log.txt"

def track_logins():
    result = subprocess.run(['last', '-n', '5'], capture_output=True, text=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] Last 5 logins:\n{result.stdout}\n")

if __name__ == "__main__":
    track_logins()
