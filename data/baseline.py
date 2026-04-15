import json
import numpy as np
import os

LOG_FILE = "telemetry_logs.json"
BASELINE_FILE = "data/baseline.json"


def load_logs():
    if not os.path.exists(LOG_FILE):
        raise FileNotFoundError("Run inference first to generate logs")

    with open(LOG_FILE, "r") as f:
        return json.load(f)


def remove_outliers(values):
    values = np.array(values)

    q1 = np.percentile(values, 25)
    q3 = np.percentile(values, 75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    filtered = values[(values >= lower) & (values <= upper)]

    return filtered.tolist()


def compute_stats(values):
    # Reduce sensitivity to extreme spikes before computing baseline stats.
    values = remove_outliers(values)

    return {
        "mean": float(np.mean(values)),
        "std": float(np.std(values) + 1e-6)
    }


def generate_baseline():

    logs = load_logs()

    typing = [x.get("typing_speed", 0) for x in logs]
    clicks = [x.get("click_rate", 0) for x in logs]

    # Count cumulative app switches to capture context-changing behavior.
    switches = []
    prev = None
    count = 0

    for x in logs:
        if prev and x["active_app"] != prev:
            count += 1
        switches.append(count)
        prev = x["active_app"]

    baseline = {
        "typing": compute_stats(typing),
        "clicks": compute_stats(clicks),
        "switches": compute_stats(switches)
    }

    os.makedirs("data", exist_ok=True)

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print("\nRobust baseline created:")
    print(json.dumps(baseline, indent=4))


if __name__ == "__main__":
    generate_baseline()