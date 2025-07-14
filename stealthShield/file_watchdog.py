# surveillance_engine/file_watchdog.py
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

LOG_FILE = "logs/file_log.txt"
WATCH_DIR = "/home/youruser/Documents"  # Change this to a test dir

class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] Modified: {event.src_path}\n")

    def on_created(self, event):
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] Created: {event.src_path}\n")

def monitor_directory():
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
