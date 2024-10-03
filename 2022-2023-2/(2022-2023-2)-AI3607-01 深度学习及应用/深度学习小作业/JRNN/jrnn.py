from jittor import Module, nn, zeros


class JRNN(Module):
    def __init__(self, rnn_type, input_size, hidden_size, num_layers, num_classes):
        super(JRNN, self).__init__()
        self.type = rnn_type
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        assert self.type in ['lstm', 'rnn']
        if self.type == 'lstm':
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        elif self.type == 'rnn':
            self.rnn = nn.RNN(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def execute(self, x):
        batch_size, channels, height, width = x.shape
        x = x.reshape(batch_size, height * channels, width)
        h0 = zeros((self.num_layers, x.size(0), self.hidden_size))
        if self.type == 'lstm':
            c0 = zeros((self.num_layers, x.size(0), self.hidden_size))
            out, _ = self.lstm(x, (h0, c0))
        elif self.type == 'rnn':
            out, _ = self.rnn(x, h0)
        out = self.fc(out[-1, :, :])  # strange here, but out shape is not batch first in jittor
        return out
