import json
import numpy as np

LOG_FILE = "telemetry_logs.json"
BASELINE_FILE = "data/baseline.json"


def load_logs():
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def compute_stats(values):
    if len(values) == 0:
        return {"mean": 0.0, "std": 1.0}

    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values) + 1e-6)
    }


def generate_baseline():

    logs = load_logs()

    typing = []
    clicks = []

    for x in logs:
        typing.append(x.get("typing_speed", 0.0))
        clicks.append(x.get("click_rate", 0.0))

    # app switches
    switches = []
    prev = None
    count = 0

    for x in logs:
        app = x.get("active_app", "Unknown")

        if prev and app != prev:
            count += 1

        switches.append(count)
        prev = app

    baseline = {
        "typing": compute_stats(typing),
        "clicks": compute_stats(clicks),
        "switches": compute_stats(switches)
    }

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("Baseline created:", baseline)


if __name__ == "__main__":
    generate_baseline()