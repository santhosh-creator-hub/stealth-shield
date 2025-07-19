from multiprocessing import Process
import os
import sys
from alert_system.telegram_bot import send_alert
from usb_monitor import monitor_usb
from surveillance_engine.file_watchdog import monitor_directory
from surveillance_engine.login_tracker import track_logins
from surveillance_engine.process_monitor import monitor_processes  

def start_honeypot():
    try:
        print("[+] Starting Honeypot...")
        os.system("python honeypot/fake_admin_panel/app.py")
    except Exception as e:
        print(f"[!] Honeypot Error: {e}")

def safe_start(module_function, name):
    try:
        print(f"[+] Starting {name}...")
        module_function()
    except Exception as e:
        print(f"[!] Error in {name}: {e}")

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    print("[*] StealthShield: Initializing Modules...\n")

    try:
        p1 = Process(target=safe_start, args=(monitor_processes, "Process Monitor"))
        p2 = Process(target=safe_start, args=(monitor_directory, "File Watchdog"))
        p3 = Process(target=start_honeypot)
        p4 = Process(target=safe_start, args=(track_logins, "Login Tracker"))
        p5 = Process(target=safe_start, args=(monitor_usb, "USB Monitor"))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt detected. Shutting down.")
        sys.exit(0)

    except Exception as e:
        print(f"[!] Critical Error: {e}")
        sys.exit(1)
