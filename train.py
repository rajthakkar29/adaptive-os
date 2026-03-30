import torch
import torch.nn as nn
import torch.optim as optim

from models.lstm_model import ContextLSTM
from data.real_dataset import generate_real_dataset

INPUT_SIZE = 14
HIDDEN = 32
CLASSES = 3

X, yc, yr = generate_real_dataset()

model = ContextLSTM(INPUT_SIZE, HIDDEN, CLASSES)

opt = optim.Adam(model.parameters(), lr=0.001)

for e in range(30):
    opt.zero_grad()

    cp, rp = model(X)

    loss = nn.CrossEntropyLoss()(cp, yc) + nn.MSELoss()(rp, yr)

    loss.backward()
    opt.step()

    print(e, loss.item())

torch.save(model.state_dict(), "context_model.pth")