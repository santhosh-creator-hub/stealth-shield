import sys
import os
import json
from collections import defaultdict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from flask import Flask, request, render_template
from datetime import datetime
from alert_system.telegram_bot import send_alert

app = Flask(__name__)

LOG_DIR = "honeypot/fake_admin_panel/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "honeypot_log.txt")

login_attempts = defaultdict(list)
THRESHOLD = 3  # Attempts per IP

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_agent = request.headers.get('User-Agent', 'Unknown')
        # Track attempts
        login_attempts[ip].append(timestamp)
        attempt_count = len(login_attempts[ip])
        log_data = {
            "timestamp": timestamp,
            "ip": ip,
            "username": username,
            "password": password,
            "user_agent": user_agent,
            "attempt_count": attempt_count
        }
        # Save JSON log
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_data) + "\n")
        alert_msg = f"\ud83d\udea8 Honeypot Alert!\nIP: {ip}\nUser: {username}\nPassword: {password}\nAgent: {user_agent}"
        if attempt_count >= THRESHOLD:
            alert_msg += f"\n\u26a0\ufe0f Multiple attempts from same IP ({attempt_count}x)"
        send_alert(alert_msg)
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
