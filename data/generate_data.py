import numpy as np
import torch

SEQUENCE_LENGTH = 20
FEATURE_SIZE = 11  
NUM_CLASSES = 3

def generate_sequence(mode):
    sequence = []

    for _ in range(SEQUENCE_LENGTH):
        cpu = np.random.uniform(0.1, 0.3)
        hour = np.random.uniform(0.3, 0.6)

        if mode == 0:  # Dev Mode
            app = [1, 0, 0, 0, 0, 0]
            risk = 0.2
        elif mode == 1:  # Browsing Mode
            app = [0, 1, 0, 0, 0, 0]
            risk = 0.4
        else:  # Gaming Mode
            app = [0, 0, 1, 0, 0, 0]
            risk = 0.6

        network = [0, 1, 0]  # assume safe network for now

        feature_vector = [cpu, hour] + app + network
        sequence.append(feature_vector)

    return np.array(sequence), mode, risk

def generate_dataset(num_samples=500):
    X = []
    y_context = []
    y_risk = []

    for _ in range(num_samples):
        mode = np.random.randint(0, NUM_CLASSES)
        seq, context_label, risk_value = generate_sequence(mode)

        X.append(seq)
        y_context.append(context_label)
        y_risk.append(risk_value)

    return (
        torch.tensor(X, dtype=torch.float32),
        torch.tensor(y_context, dtype=torch.long),
        torch.tensor(y_risk, dtype=torch.float32).unsqueeze(1)
    )

if __name__ == "__main__":
    X, y_context, y_risk = generate_dataset()
    print("X shape:", X.shape)
    print("Context labels shape:", y_context.shape)
    print("Risk shape:", y_risk.shape)