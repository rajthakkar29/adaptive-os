import torch
import torch.nn as nn
import torch.optim as optim

from models.lstm_model import ContextLSTM
from data.real_dataset import generate_real_dataset

INPUT_SIZE = 14
HIDDEN_SIZE = 32
NUM_CLASSES = 3

EPOCHS = 20
LR = 0.001

X, yc, yr = generate_real_dataset()

print("Dataset shape:", X.shape)

if len(X) == 0:
    raise ValueError("Dataset is empty. Run inference.py to collect logs first.")

model = ContextLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES)

criterion_context = nn.CrossEntropyLoss()
criterion_risk = nn.MSELoss()

optimizer = optim.Adam(model.parameters(), lr=LR)

for epoch in range(EPOCHS):

    model.train()
    optimizer.zero_grad()

    context_pred, risk_pred = model(X)

    loss_c = criterion_context(context_pred, yc)
    loss_r = criterion_risk(risk_pred, yr)

    loss = loss_c + loss_r

    loss.backward()
    optimizer.step()

    print(
        f"Epoch {epoch+1}/{EPOCHS} | "
        f"Total Loss: {loss.item():.4f} | "
        f"Context: {loss_c.item():.4f} | "
        f"Risk: {loss_r.item():.4f}"
    )

torch.save(model.state_dict(), "context_model.pth")

print("\n✅ Model trained on REAL user behavior")