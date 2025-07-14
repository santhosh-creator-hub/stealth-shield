# StealthShield Surveillance Suite

## Overview
This project monitors file changes, user logins, and new processes on your system, logging all events for later review. All monitors run in parallel.

## Directory Structure
```
stealthShield/
├── surveillance_engine/
│   ├── __init__.py
│   ├── file_watchdog.py
│   ├── login_tracker.py
│   └── process_monitor.py
├── logs/
├── run.py
├── requirements.txt
└── README.md
```

## Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Ensure you are running on a Unix-like OS (the login tracker uses the `last` command).

## Usage
Run all monitors in parallel with:
```
python run.py
```

Log files will be created in the `logs/` directory.

---

**Note:**
- If you are on Windows, the login tracker will not work as expected.
- You can change the monitored directory in `file_watchdog.py` (`WATCH_DIR`).
