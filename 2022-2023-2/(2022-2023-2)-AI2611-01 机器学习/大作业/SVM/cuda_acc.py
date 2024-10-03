import torch
import cupy as cp
import numpy as np


# to make my code easier to understand, rename and modified some functions from cupy
# the core is to accelerate matrix calculation
# I tried to write in direct C++ cuda, cut the workload is too high

def has_cuda():
    return torch.cuda.is_available()


def cuda(matrix):
    return cp.array(matrix)


def to_cpu(matrix: cp.ndarray):
    return matrix.get()


def cpu(matrix):
    return np.array(matrix)


def is_cuda(matrix):
    return type(matrix) is cp.ndarray


def normalize(matrix, device):
    if device is cuda:
        return (matrix - cp.min(matrix)) / (cp.max(matrix) - cp.min(matrix))
    elif device is cpu:
        return (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
    else:
        raise NotImplementedError
