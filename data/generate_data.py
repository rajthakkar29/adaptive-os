import torch
import numpy as np


def generate_dataset(num_samples=1000, seq_length=10):

    X = []
    y_context = []
    y_risk = []

    for _ in range(num_samples):

        sequence = []

        for _ in range(seq_length):

            cpu = np.random.rand()
            hour = np.random.rand()

            typing = np.random.uniform(0, 1)
            click = np.random.uniform(0, 1)

            app = np.random.randint(0, 6)
            app_onehot = [0]*6
            app_onehot[app] = 1

            net = np.random.randint(0, 3)
            net_onehot = [0]*3
            net_onehot[net] = 1

            feature = [cpu, hour, typing, click] + app_onehot + net_onehot
            sequence.append(feature)

        X.append(sequence)

        y_context.append(np.random.randint(0, 3))
        y_risk.append(np.random.rand())

    return (
        torch.tensor(X, dtype=torch.float32),
        torch.tensor(y_context, dtype=torch.long),
        torch.tensor(y_risk, dtype=torch.float32).unsqueeze(1)
    )