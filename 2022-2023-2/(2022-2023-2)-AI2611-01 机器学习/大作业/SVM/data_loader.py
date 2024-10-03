import torch
from torchvision.datasets import MNIST, CIFAR10
from cuda_acc import cpu, cuda, has_cuda
import numpy as np
import cupy as cp
from utils import data_filter


def load_data(data_type, data_path='./data', device=cuda):
    X_train, y_train, X_test, y_test = None, None, None, None
    lib = np if device is cpu else cp
    if data_type == 'mnist':
        train_dataset = MNIST(root=data_path, train=True, download=True)
        X_train = train_dataset.data.reshape(train_dataset.data.shape[0], -1)
        y_train = train_dataset.targets.reshape(train_dataset.targets.shape[0], -1)

        test_dataset = MNIST(root=data_path, train=False)
        X_test = test_dataset.data.reshape(test_dataset.data.shape[0], -1)
        y_test = test_dataset.targets.reshape(test_dataset.targets.shape[0], -1)

    elif data_type == 'cifar10':
        train_dataset = CIFAR10(root=data_path, train=True, download=True)
        X_train = torch.tensor(train_dataset.data).reshape(len(train_dataset), -1)
        y_train = torch.tensor(train_dataset.targets).reshape(len(train_dataset), -1)

        test_dataset = CIFAR10(root=data_path, train=False)
        X_test = torch.tensor(test_dataset.data).reshape(len(test_dataset), -1)
        y_test = torch.tensor(test_dataset.targets).reshape(len(test_dataset), -1)

    X_train, y_train, X_test, y_test = device(X_train), device(y_train), device(X_test), device(y_test)

    X_train, y_train = data_filter(X_train, y_train, lib, 500)
    X_test, y_test = data_filter(X_test, y_test, lib, 100)

    print('Data Loaded.')

    m = X_train.mean(0)
    if data_type == 'mnist':
        return (X_train - m) / 255 * 6, y_train, (X_test - m) / 255 * 6, y_test
    else:
        return (X_train - m) / 255, y_train, (X_test - m) / 255, y_test


if __name__ == '__main__':
    dev = cuda if has_cuda() else cpu
    print('MNIST dataset:')
    for item in load_data('mnist', device=dev):
        print(item.shape, type(item))
    print()
    print('CIFAR10 dataset:')
    for item in load_data('cifar10', device=dev):
        print(item.shape, type(item))
    print('data load OK!')
