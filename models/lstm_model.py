import torch
import torch.nn as nn


class ContextLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(ContextLSTM, self).__init__()

        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)

        self.fc_context = nn.Linear(hidden_size, num_classes)
        self.fc_risk = nn.Linear(hidden_size, 1)

        self.softmax = nn.Softmax(dim=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        out, _ = self.lstm(x)
        last = out[:, -1, :]

        context = self.softmax(self.fc_context(last))
        risk = self.sigmoid(self.fc_risk(last))

        return context, risk