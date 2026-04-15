import json
import numpy as np
import torch

from telemetry.preprocess import preprocess

SEQ = 20


def load_logs():
    with open("telemetry_logs.json", "r") as f:
        return json.load(f)


def load_baseline():
    with open("data/baseline.json", "r") as f:
        return json.load(f)


def z_score(value, mean, std):
    std = max(std, 1.0)
    return (value - mean) / std


def generate_real_dataset():

    logs = load_logs()
    BASELINE = load_baseline()

    X = []
    y_context = []
    y_risk = []

    sequence = []

    for i in range(len(logs)):

        data = logs[i]

        vec = preprocess(data)
        sequence.append(vec)

        if len(sequence) > SEQ:
            sequence.pop(0)

        if len(sequence) == SEQ:

            X.append(sequence.copy())

            # -------- CONTEXT --------
            app = data["active_app"]

            if app == "Code.exe":
                y_context.append(0)
            elif app == "chrome.exe":
                y_context.append(1)
            elif app in ["steam.exe", "steamwebhelper.exe"]:
                y_context.append(2)
            else:
                y_context.append(0)

            # -------- ADAPTIVE RISK LABEL --------
            t = data.get("typing_speed", 0)
            c = data.get("click_rate", 0)

            t_z = z_score(t, BASELINE["typing"]["mean"], BASELINE["typing"]["std"])

            click_std = BASELINE["clicks"]["std"]
            if click_std < 0.01:
                c_z = 0
            else:
                c_z = z_score(c, BASELINE["clicks"]["mean"], click_std)

            anomaly = abs(t_z) * 1.5 + abs(c_z)

            if anomaly > 4:
                y_risk.append([1.0])
            elif anomaly > 2.5:
                y_risk.append([0.7])
            elif anomaly > 1.5:
                y_risk.append([0.5])
            else:
                y_risk.append([0.2])

    X = torch.tensor(np.array(X), dtype=torch.float32)
    y_context = torch.tensor(y_context, dtype=torch.long)
    y_risk = torch.tensor(y_risk, dtype=torch.float32)

    return X, y_context, y_risk