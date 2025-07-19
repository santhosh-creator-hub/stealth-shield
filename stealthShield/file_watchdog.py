import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
from alert_system.telegram_bot import send_alert # Ensur

# Auto-detect user's home Documents folder
WATCH_DIR = os.path.expanduser("~/Documents")
LOG_FILE = "logs/file_log.txt"

class WatcherHandler(FileSystemEventHandler):
    def log_event(self, event_type, path):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{timestamp}] {event_type.upper()}: {path}"
        print(message)

        # Log locally
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")

        # Send Telegram alert
        emoji = {
            "CREATED": "🆕",
            "MODIFIED": "✏️",
            "DELETED": "❌"
        }.get(event_type.upper(), "📁")
        send_alert(f"{emoji} *{event_type.title()}*:\n`{path}`")

    def on_created(self, event):
        self.log_event("CREATED", event.src_path)

    def on_modified(self, event):
        self.log_event("MODIFIED", event.src_path)

    def on_deleted(self, event):
        self.log_event("DELETED", event.src_path)

def monitor_directory():
    print(f"[i] File Monitor Started — Watching: {WATCH_DIR}")
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
