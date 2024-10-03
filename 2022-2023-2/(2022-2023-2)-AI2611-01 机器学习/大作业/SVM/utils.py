import numpy as np
from cuda_acc import to_cpu
import time

time_str = lambda t: time.strftime("%H:%M:%S", time.gmtime(t))


def data_shuffle(X, y, lib):
    assert len(X.shape) == 2 and len(y.shape) == 2
    assert X.shape[0] == y.shape[0]
    rperm = lib.random.permutation(X.shape[0])
    return X[rperm], y[rperm]


def data_filter(X, y, lib, amount=None, filter=range(10)):
    if amount is None:
        amount = len(X)
    selected_data = []
    selected_labels = []
    for label in filter:
        label_indices = lib.where(y == label)[0]
        selected_indices = label_indices[:amount]
        selected_data.append(X[selected_indices])
        selected_labels.append(y[selected_indices])
        if len(filter) == 1:
            selected_data.append(X[~selected_indices])
            selected_labels.append(-1 * lib.ones((selected_data[-1].shape[0], 1)))
    X = lib.concatenate(selected_data, axis=0)
    y = lib.concatenate(selected_labels, axis=0)
    rperm = lib.random.permutation(X.shape[0])
    X = X[rperm]
    y = y[rperm]
    return X, y


def batchify(X, y, batch_size, lib):
    batch_X = []
    batch_y = []
    num_batch = len(X) // batch_size
    for i in range(num_batch):
        batch_X.append(X[i * batch_size:(i + 1) * batch_size])
        batch_y.append(y[i * batch_size:(i + 1) * batch_size])
    if len(X) > num_batch * batch_size:
        batch_X.append(X[num_batch * batch_size:])
        batch_y.append(y[num_batch * batch_size:])
    return batch_X, batch_y


def label_wash(label, lib):
    unique_labels = lib.unique(label if lib is np else to_cpu(label))  # 查找唯一的标签
    if len(unique_labels) != 2:
        raise ValueError('Include more than one classes or only one class.')
    l_converted = lib.where(label == max(unique_labels), 1, -1)
    return l_converted
