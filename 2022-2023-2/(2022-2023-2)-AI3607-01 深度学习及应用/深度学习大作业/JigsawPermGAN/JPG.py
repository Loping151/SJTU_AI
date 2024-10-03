from typing import Union
from jittor import nn, concat


class Discriminator(nn.Module):
    def __init__(self, shape: Union[tuple, int] = (32, 32)):
        super().__init__()
        if type(shape) is int:
            shape = (shape, shape)
        self.conv1 = nn.Conv2d(3, 8, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(8, 16, 3, stride=1, padding=1)
        self.linear1 = nn.Linear(16 * shape[0] * shape[1], 4096)
        self.linear2 = nn.Linear(4096, 1)
        self.relu = nn.Relu()

    def execute(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view((x.shape[0], -1))
        x = self.relu(self.linear1(x))
        x = self.linear2(x)
        return x


class Encoder(nn.Module):
    def __init__(self, cut: int = 2, with_raw=True, shape: Union[tuple, int] = (32, 32)):
        super().__init__()
        self.with_raw = with_raw
        self.conv0 = nn.Conv2d(3, 3 * cut ** 2, 5, stride=1, padding=2)
        self.conv1 = nn.Conv2d(3 * cut ** 2, 32, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, stride=1, padding=1)
        self.linear1 = nn.Linear(64 * shape[0] * shape[1], 2048)
        self.linear2 = nn.Linear(2048, 512)
        self.classify = nn.Linear(512, 10)
        self.relu = nn.Relu()

    def execute(self, x, get_features=True):
        raw = None
        if self.with_raw:
            raw = x
        if not get_features:
            x = self.relu(self.conv0(x))
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        if get_features:
            if self.with_raw:
                x = concat([raw, x], dim=1)
            return x
        x = self.relu(self.linear1(x.view((x.shape[0], -1))))
        x = self.relu(self.linear2(x))
        x = self.classify(x)
        return x


class JigsawSolver(nn.Module):
    def __init__(self, cut: int = 2, shape: Union[tuple, int] = (16, 16), use_encoder: bool = True):
        super().__init__()
        if type(shape) is int:
            shape = (shape, shape)
        if use_encoder:
            self.conv1 = nn.Conv2d(64 + 3 * cut ** 2, 64, 3, stride=1, padding=1)
        else:
            self.conv1 = nn.Conv2d(3 * cut ** 2, 64, 5, stride=1, padding=2)
        self.conv2 = nn.Conv2d(64, 64, 3, stride=1, padding=1)
        self.linear1 = nn.Linear(64 * shape[0] * shape[1], 4096)
        self.linear2 = nn.Linear(4096, cut ** 2)
        self.relu = nn.Relu()

    def execute(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view((x.shape[0], -1))
        x = self.relu(self.linear1(x))
        x = self.linear2(x)
        return x


class Empty(nn.Module):
    def __init__(self, **kargs):
        super().__init__()
