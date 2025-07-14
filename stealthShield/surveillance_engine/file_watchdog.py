# surveillance_engine/file_watchdog.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os
from alert_system.telegram_bot import send_alert

LOG_FILE = "logs/file_log.txt"
WATCH_DIR = "C:\\Users\\santh\\Downloads"  # Now monitoring Downloads folder

class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        message = f"🛠️ File modified: {event.src_path}"
        send_alert(message)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] Modified: {event.src_path}\n")

    def on_created(self, event):
        message = f"📁 File created: {event.src_path}"
        send_alert(message)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] Created: {event.src_path}\n")

def monitor_directory():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_directory()
