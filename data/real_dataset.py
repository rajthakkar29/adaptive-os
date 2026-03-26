import json
import torch
import numpy as np
from telemetry.preprocess import preprocess

LOG_FILE = "telemetry_logs.json"
SEQUENCE_LENGTH = 10


def load_logs():
    with open(LOG_FILE, "r") as f:
        return json.load(f)


def create_sequences(logs):

    sequences = []

    for i in range(len(logs) - SEQUENCE_LENGTH):

        seq = []

        for j in range(SEQUENCE_LENGTH):

            data = logs[i + j]

            telemetry = {
                "cpu": data["cpu"],
                "hour": data["hour"],
                "active_app": data["active_app"],
                "network": data["network"]
            }

            vector = preprocess(telemetry)
            seq.append(vector)

        sequences.append(seq)

    return np.array(sequences)


def assign_labels(sequences):

    y_context = []
    y_risk = []

    for seq in sequences:

        avg_cpu = np.mean(seq[:, 0])

        if avg_cpu < 0.2:
            context = 0
            risk = 0.2

        elif avg_cpu < 0.4:
            context = 1
            risk = 0.4

        else:
            context = 2
            risk = 0.6

        y_context.append(context)
        y_risk.append(risk)

    return (
        torch.tensor(y_context, dtype=torch.long),
        torch.tensor(y_risk, dtype=torch.float32).unsqueeze(1)
    )


def generate_real_dataset():

    logs = load_logs()

    sequences = create_sequences(logs)

    y_context, y_risk = assign_labels(sequences)

    X = torch.tensor(sequences, dtype=torch.float32)

    return X, y_context, y_risk


if __name__ == "__main__":

    X, y_context, y_risk = generate_real_dataset()

    print("X shape:", X.shape)
    print("Context shape:", y_context.shape)
    print("Risk shape:", y_risk.shape)