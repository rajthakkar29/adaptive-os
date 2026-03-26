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
        lstm_out, _ = self.lstm(x)
        last_output = lstm_out[:, -1, :]

        context_logits = self.fc_context(last_output)
        risk_logits = self.fc_risk(last_output)

        context = self.softmax(context_logits)
        risk = self.sigmoid(risk_logits)

        return context, risk
