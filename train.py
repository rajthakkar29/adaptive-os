import torch
import torch.nn as nn
import torch.optim as optim

from models.lstm_model import ContextLSTM
from data.real_dataset import generate_real_dataset   # CHANGED

# Model parameters
INPUT_SIZE = 11
HIDDEN_SIZE = 32
NUM_CLASSES = 3

EPOCHS = 30
LEARNING_RATE = 0.001

# Generate dataset (REAL DATA NOW)
X, y_context, y_risk = generate_real_dataset()   # CHANGED

# Initialize model
model = ContextLSTM(INPUT_SIZE, HIDDEN_SIZE, NUM_CLASSES)

# Loss functions
criterion_context = nn.CrossEntropyLoss()
criterion_risk = nn.MSELoss()

optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Training loop
for epoch in range(EPOCHS):

    model.train()
    optimizer.zero_grad()

    context_pred, risk_pred = model(X)

    loss_context = criterion_context(context_pred, y_context)
    loss_risk = criterion_risk(risk_pred, y_risk)

    loss = loss_context + loss_risk

    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}/{EPOCHS} | "
          f"Total Loss: {loss.item():.4f} | "
          f"Context Loss: {loss_context.item():.4f} | "
          f"Risk Loss: {loss_risk.item():.4f}")

# Save trained model
torch.save(model.state_dict(), "context_model.pth")

print("Training complete. Model saved as context_model.pth")