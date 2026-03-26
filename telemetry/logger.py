import json
import os
from datetime import datetime

LOG_FILE = "telemetry_logs.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)


def log_telemetry(data):
    logs = load_logs()

    entry = {
        "timestamp": datetime.now().isoformat(),

        # existing fields
        "cpu": data.get("cpu", 0),
        "hour": data.get("hour", 0),
        "active_app": data.get("active_app", "Unknown"),
        "network": data.get("network", "Unknown"),

        # NEW behavioral fields
        "keystrokes": data.get("keystrokes", 0),
        "mouse_clicks": data.get("mouse_clicks", 0),
        "mouse_distance": data.get("mouse_distance", 0)
    }

    logs.append(entry)

    # keep file size controlled
    if len(logs) > 5000:
        logs = logs[-5000:]

    save_logs(logs)