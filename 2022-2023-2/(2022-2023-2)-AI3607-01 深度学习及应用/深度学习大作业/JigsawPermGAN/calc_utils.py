from itertools import permutations

import jittor as jt
import numpy as np
from PIL.Image import Image

from jigsaw_utils import jigsaw_filler


def zero_or_one(arr):
    zoo = []
    for _i in range(len(arr)):
        zoo.append(1 if arr[_i][0] > 0.5 else 0)
    return jt.array(zoo, dtype=jt.int32)


def max_to_one(arr):
    max_value = jt.max(arr)
    arr[arr != max_value] = 0
    arr[arr == max_value] = 1
    return jt.int32(arr)


def rank(lst: jt.array):
    arr = lst.numpy()
    sorted_indices = np.argsort(arr, axis=1)
    ranks = np.empty_like(sorted_indices)
    ranks[np.arange(len(lst))[:, np.newaxis], sorted_indices] = np.arange(arr.shape[1])
    return ranks


def transrank(lst: jt.array):
    return 1 / (lst + 1)


def remap(imgs, transarray, with_gradient=False):
    assert imgs[0].shape[-1] == imgs[0].shape[-2]  # should be square
    batch, cuts, _, shape, _ = imgs.shape  # batch, cuts**2, 3, H, W
    cuts = int(np.sqrt(cuts))
    canvas = jt.zeros((batch, 3, shape * cuts, shape * cuts))
    trans = rank(transarray)
    for i in range(batch):
        for j in range(cuts ** 2):
            _x = trans[i][j] % cuts
            _y = trans[i][j] // cuts
            if with_gradient:
                canvas[i, :, _x * shape:(_x + 1) * shape, _y * shape:(_y + 1) * shape] = imgs[i, j, :, :, :] * 1e5 * transarray[i][j] / (1e5 + transarray[i][j].detach())
            else:
                canvas[i, :, _x * shape:(_x + 1) * shape, _y * shape:(_y + 1) * shape] = imgs[i, j, :, :, :]
    return canvas


def edge_loss(maps: jt.array, cuts):
    assert cuts in [2, 4]  # No implementation
    _loss = jt.array(0, dtype=jt.float32)
    _, _, shape, _ = maps.shape
    if cuts == 2:
        assert shape % 2 == 0
        mid = shape // 2
        for i in maps:
            _loss += jt.mean(jt.abs(i[:, mid - 1, :] - i[:, mid, :])) + jt.mean(jt.abs(i[:, :, mid - 1] - i[:, :, mid]))
    elif cuts == 4:
        assert shape % 4 == 0
        mid = [shape // 4, shape // 2, 3 * shape // 4]
        for i in maps:
            for j in range(3):
                _loss += jt.mean(jt.abs(i[:, mid[i] - 1, :] - i[:, mid[i], :])) + jt.mean(jt.abs(i[:, :, mid[i] - 1] - i[:, :, mid[i]]))
    return _loss


def tv_loss2(img):
    img = np.array(img, dtype=np.float32)
    half = int(img.shape[0] / 2), int(img.shape[1] / 2)
    tv_h = np.sum(np.abs(img[half[0] - 1, :, :] - img[half[0], :, :]))
    tv_w = np.sum(np.abs(img[:, half[1] - 1, :] - img[:, half[1], :]))
    return tv_h + tv_w


def simple_solver(imgs: list[Image]):
    cuts = int(len(imgs) ** 0.5)
    all_res = []
    for per in permutations(np.arange(cuts ** 2)):
        all_res.append(tv_loss2(jigsaw_filler(imgs, per, padding=0)))
    return jt.array(list(permutations(np.arange(cuts ** 2)))[all_res.index(min(all_res))])
