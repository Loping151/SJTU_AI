import os
import numpy as np
from PIL import Image
from jittor import rand
from jittor.dataset import Dataset
from jittor.dataset.mnist import MNIST
import gzip
import jittor.transform as trans


def get_dataset(train_path, test_path, download=False, batch_size=128, shuffle=True, data_seg=False):
    test_loader = MNIST(data_root=test_path, train=False, download=download, batch_size=batch_size, shuffle=shuffle)

    if data_seg:
        with gzip.open(train_path + "train-images-idx3-ubyte.gz", 'rb') as f:
            data = np.frombuffer(f.read(), np.uint8, offset=16).reshape((-1, 28, 28))
        with gzip.open(train_path + "train-labels-idx1-ubyte.gz", 'rb') as f:
            labels = np.frombuffer(f.read(), np.uint8, offset=8)
        part = [[] for _ in range(10)]
        for i in range(len(labels)):
            part[labels[i]].append(i)
        train_indices = []
        for i in range(10):
            if i < 5:
                selected = np.random.choice(part[i], size=int(len(part[i]) * 0.1), replace=False)
                train_indices = np.concatenate((train_indices, selected, selected, selected, selected, selected, selected, selected, selected, selected))
                # train_indices = np.concatenate((train_indices, selected))
            else:
                train_indices = np.concatenate((train_indices, np.array(part[i])))
        np.random.shuffle(train_indices)
        train_indices = np.array(train_indices, dtype=int)

        class DataFilter(Dataset):
            def __init__(self, data, label, indices, batch_size):
                super().__init__(batch_size=batch_size)
                self.data = data
                self.label = label
                self.indices = indices

            def __len__(self):
                return len(self.indices)

            def __getitem__(self, idx):
                if self.label[self.indices[idx]]<5:
                    return trans.to_tensor(Image.fromarray((self.data[self.indices[idx]])).rotate(rand(1)*40-20).convert('RGB')), self.label[self.indices[idx]]
                return trans.to_tensor(Image.fromarray(self.data[self.indices[idx]]).convert('RGB')), self.label[self.indices[idx]]

        train_loader = DataFilter(data, labels, train_indices, batch_size=batch_size)
    else:
        train_loader = MNIST(data_root=train_path, train=True, download=download, batch_size=batch_size, shuffle=shuffle)

    return train_loader, test_loader


if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
    x, y = get_dataset('data/', 'data/', download=True, data_seg=True)
