import os

from cuda_acc import cpu, cp, cuda, to_cpu
import numpy as np
from scipy.ndimage import convolve


# this lib includes img_process and dim reduction. the latter is a previous homework, modified for use

# Lo_dim_reduction version 1.1
# author: Loping151(SJTU)
# AI homework, finished 2022.6
# Reconstructed 2023.5
# email: wangkailing151@gmail.com


# dimensionality reduction methods


# multiple dimensional scaling
# param:
#   data is the original data, n_components is the target dimension
# method:
#   fit_reduce
#   there is a strange param called _inner_mode, which is used inside Isomap only
#   return reduced data
class MDS:
    def __init__(self, n_components=2):
        self.n_components = n_components

    def fit_reduce(self, data, dev=cuda):
        lib = np if dev == cuda else cp
        dist = lib.square(data[:, None] - data).sum(axis=2)
        dist_i = lib.mean(dist, axis=1)
        dist_j = lib.mean(dist, axis=0)
        dist_ij = lib.mean(dist)
        B = -0.5 * (dist - dist_i[:, None] - dist_j + dist_ij)
        eigenvalues, eigenvectors = lib.linalg.eigh(B)
        index = lib.argsort(-eigenvalues)[:self.n_components]
        diag_eigenvalues = lib.sqrt(-np.sort(-eigenvalues)[:self.n_components])
        selected_v = eigenvectors[:, index]
        Z = selected_v.dot(lib.diag(diag_eigenvalues))
        return Z


# principal component analysis
# param:
#   same as MDS, no dis
# method:
#   same as MDS
class PCA:
    def __init__(self, n_components=2):
        self.n_components = n_components
        self.centre = None
        self.selected_v = None

    def fit_reduce(self, data, dev='cpu'):
        lib = np if dev == 'cpu' else cp
        self.centre = lib.mean(data, axis=0)
        data = data - self.centre  # zero centred
        cov = lib.cov(data.T)
        eigenvalues, eigenvectors = lib.linalg.eigh(cov)
        index = lib.argsort(eigenvalues)[-self.n_components:]  # sort from big to small
        self.selected_v = eigenvectors[:, index]
        W = data.dot(self.selected_v)
        return W

    def reduce(self, data):
        data = data - self.centre  # zero centred
        W = data.dot(self.selected_v)
        return W


# img process functions
def histo_gram(images, nbins=256, dev=cuda):
    lib = np if dev is cpu else cp
    batch_size = len(images)
    hists = []
    for i in range(batch_size):
        hist, _ = lib.histogram(images[i], bins=nbins, range=(0, 1 + 1e-5))
        hists.append(hist / lib.sum(hist) - 0.5)
    hists = lib.array(hists)
    return hists


def rgb_vector(images, dev=cuda):
    lib = np if dev is cpu else cp
    v = lib.sum(images.reshape((images.shape[0], -1, 3)), axis=1)
    return v / lib.linalg.norm(v) * 100


def mathcal_fetures(images, dev=cuda):
    lib = np if dev is cpu else cp
    mean = lib.mean(images, axis=1)[:, lib.newaxis]
    variance = lib.var(images, axis=1)[:, lib.newaxis]
    min_value = lib.min(images, axis=1)[:, lib.newaxis]
    max_value = lib.max(images, axis=1)[:, lib.newaxis]
    median = lib.median(images, axis=1)[:, lib.newaxis]
    features = lib.concatenate((mean, variance, min_value, max_value, max_value, median), axis=1)
    return features


def calculate_hog(image, lib):
    gray = lib.dot(image[..., :3], lib.array([0.2989, 0.5870, 0.1140]))
    gray = gray.get() if lib is cp else gray
    dx = lib.array(convolve(gray, np.array([[-1, 0, 1]])))
    dy = lib.array(convolve(gray, np.array([[-1], [0], [1]])))
    magnitude = lib.sqrt(dx ** 2 + dy ** 2)
    angle = lib.arctan2(dy, dx)
    angle = lib.rad2deg(angle) % 180
    block_size = 8
    cell_size = 4
    num_bins = 9
    hog_feature = []
    for i in range(0, gray.shape[0] - block_size + 1, cell_size):
        for j in range(0, gray.shape[1] - block_size + 1, cell_size):
            block = magnitude[i:i + block_size, j:j + block_size]
            block_angle = angle[i:i + block_size, j:j + block_size]
            hist, _ = lib.histogram(block_angle, bins=num_bins, range=(0, 180), weights=block)
            hog_feature.append(hist)
    hog_vector = lib.array(hog_feature).flatten()
    return hog_vector


def hog_features(images, shape=(32, 32, 3), dev=cuda, fast_laod=False):
    lib = np if dev is cpu else cp
    if fast_laod and os.path.exists('hog_features.npy'):
        return lib.load('hog_features.npy')
    images = images.reshape(-1, *shape)
    hog_batch = []
    for image in images:
        hog_vector = calculate_hog(image, lib)
        hog_batch.append(hog_vector)
    hog_batch = lib.array(hog_batch)
    if fast_laod:
        cp.save('hog_features', hog_batch)
    return hog_batch
