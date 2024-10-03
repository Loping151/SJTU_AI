import jittor as jt
from jittor import Module
from jittor import nn


class MulNet(Module):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.layer1 = nn.Linear(2, 10000)
        self.layer2 = nn.Linear(10000, 10000)
        self.layer3 = nn.Linear(10000, 10000)
        self.layer4 = nn.Linear(10000, 1)
        self.relu = nn.Relu()

    def execute(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        x = self.relu(x)
        x = self.layer3(x)
        x = self.relu(x)
        x = self.layer4(x)
        return x


