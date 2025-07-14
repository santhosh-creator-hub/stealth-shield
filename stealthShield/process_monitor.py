# surveillance_engine/process_monitor.py
import psutil
import time
from datetime import datetime

LOG_FILE = "logs/process_log.txt"
known_pids = set()

def log_process(proc):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] New process: {proc.pid} - {proc.name()}\n")

def monitor_processes():
    global known_pids
    while True:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid not in known_pids:
                known_pids.add(proc.pid)
                log_process(proc)
        time.sleep(5)  # adjustable interval

if __name__ == "__main__":
    monitor_processes()
