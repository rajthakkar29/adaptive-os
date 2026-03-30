import json
import numpy as np
import torch
from telemetry.preprocess import preprocess

SEQ = 10


def load():
    with open("telemetry_logs.json") as f:
        return json.load(f)


def sequences(data):
    return [data[i:i+SEQ] for i in range(len(data)-SEQ)]


def label(seq):
    t = np.mean([x.get("typing_speed", 0) for x in seq])
    c = np.mean([x.get("click_rate", 0) for x in seq])

    if t > 7 or c > 10:
        return 2, 0.9
    elif t >4 or c > 6:
        return 1, 0.6
    elif t>1 or c>2:
        return 0, 0.3
    else:
        return 0, 0.1


def generate_real_dataset():
    raw = load()
    seqs = sequences(raw)

    X, yc, yr = [], [], []

    for s in seqs:
        X.append([preprocess(x) for x in s])
        c, r = label(s)
        yc.append(c)
        yr.append([r])

    return (
        torch.tensor(np.array(X), dtype=torch.float32),
        torch.tensor(yc, dtype=torch.long),
        torch.tensor(yr, dtype=torch.float32)
    )