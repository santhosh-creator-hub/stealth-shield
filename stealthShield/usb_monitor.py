import wmi
import time
from datetime import datetime
from alert_system.telegram_bot import send_alert
import tkinter as tk
from tkinter import messagebox
import pythoncom
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

log_file = "logs/usb_log.txt"
logged_devices = set()
denied_devices = set()

def log_event(message):
    with open(log_file, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def ask_permission_gui(device_name):
    root = tk.Tk()
    root.withdraw()  # Hide main window
    result = messagebox.askquestion(
        "⚠️ USB Device Detected",
        f"A new USB device was detected:\n\n{device_name}\n\nAllow access?",
        icon='warning'
    )
    root.destroy()
    return result

def get_usb_device_name(usb_entry):
    try:
        pnp_id = usb_entry.Dependent.split("DeviceID=")[-1].strip('"').replace('\\\\', '\\')
        c = wmi.WMI()
        for device in c.Win32_PnPEntity():
            if device.DeviceID == pnp_id:
                return device.Name or pnp_id
    except Exception:
        return usb_entry.Dependent
    return usb_entry.Dependent

def monitor_usb():
    pythoncom.CoInitialize()
    c = wmi.WMI()

    insert_watcher = c.watch_for(notification_type="Creation", wmi_class="Win32_USBControllerDevice")
    remove_watcher = c.watch_for(notification_type="Deletion", wmi_class="Win32_USBControllerDevice")

    print("[*] USB Monitor Started...")

    while True:
        try:
            inserted = removed = None

            try:
                inserted = insert_watcher(timeout_ms=500)
            except:
                pass

            try:
                removed = remove_watcher(timeout_ms=500)
            except:
                pass

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if inserted:
                device_name = get_usb_device_name(inserted)

                if device_name in logged_devices or device_name in denied_devices:
                    continue

                user_choice = ask_permission_gui(device_name)

                if user_choice == 'yes':
                    logged_devices.add(device_name)
                    log_msg = f"[USB ALLOWED] {device_name} at {timestamp}"
                    send_alert(f"✅ USB Allowed:\n{device_name}\n🕒 {timestamp}")
                else:
                    denied_devices.add(device_name)
                    log_msg = f"[USB DENIED] {device_name} at {timestamp}"
                    send_alert(f"🚫 USB Denied:\n{device_name}\n🕒 {timestamp}")

                print(log_msg)
                log_event(log_msg)

            if removed:
                device_name = get_usb_device_name(removed)

                if device_name in logged_devices:
                    logged_devices.remove(device_name)
                    log_msg = f"[USB REMOVED] {device_name} at {timestamp}"
                    print(log_msg)
                    log_event(log_msg)
                    send_alert(f"❌ USB Removed:\n{device_name}\n🕒 {timestamp}")

                elif device_name in denied_devices:
                    denied_devices.remove(device_name)
                    log_event(f"[DENIED USB REMOVED] {device_name} at {timestamp}")

        except Exception as e:
            log_event(f"[ERROR] {str(e)}")
            time.sleep(2)

if __name__ == "__main__":
    monitor_usb()
