import json
import os
from datetime import datetime

LOG_FILE = "telemetry_logs.json"

def log_telemetry(data):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "cpu": data["cpu"],
        "hour": data["hour"],
        "active_app": data["active_app"],
        "network": data["network"]
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)