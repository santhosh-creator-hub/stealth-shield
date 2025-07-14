# run.py
from multiprocessing import Process
import os
from multiprocessing import Process
from surveillance_engine import process_monitor, file_watchdog

def start_honeypot():
    os.system("python honeypot/fake_admin_panel/app.py")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    p1 = Process(target=process_monitor.monitor_processes)
    p2 = Process(target=file_watchdog.monitor_directory)
    p3 = Process(target=start_honeypot)

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
