from PIL import Image
import numpy as np
from itertools import permutations


def jigsaw_cutter(img: Image, cuts: int, shape=None, resize_shape=None):
    if shape is None:
        shape = img.size
    assert shape[0] % cuts == 0 and shape[1] % cuts == 0
    imgs = []
    stepx, stepy = shape[0] // cuts, shape[1] // cuts
    for i in range(cuts):
        for j in range(cuts):
            if resize_shape is None:
                imgs.append(img.crop((j * stepx, i * stepy, (j + 1) * stepx, (i + 1) * stepy)))
            else:
                imgs.append(img.crop((j * stepx, i * stepy, (j + 1) * stepx, (i + 1) * stepy)).resize(resize_shape))
    return imgs, range(cuts ** 2)


def jigsaw_shuffle(imgs: list[Image], seq: list[int], order=None):
    if order is None:
        sseq = np.arange(len(seq))
        np.random.shuffle(sseq)
        sseq = sseq.tolist()
    else:
        sseq = order
    return [imgs[indice] for indice in sseq], [seq[indice] for indice in sseq]


def jigsaw_shuffle_all(dataset, cuts=2, resize_shape=None, with_original=True, prob=1):
    shuffle_all = []
    for oda in dataset:
        cutted = jigsaw_cutter(oda, cuts, resize_shape=resize_shape)
        for per in permutations(np.arange(cuts ** 2)):
            if not with_original and (per == np.arange(cuts ** 2)).all():
                continue
            if np.random.rand() > prob:
                continue
            shuffle_all.append(jigsaw_shuffle(*cutted, per))

    return shuffle_all


def jigsaw_filler(imgs: list[Image], seq: list[int], padding: int = 1, shape=None, save_path: str = None, silent: bool = True):
    assert shape is not None or int(len(seq) ** 0.5) ** 2 == len(seq)  # must determine shape if not cut as square
    cuts = int(len(seq) ** 0.5)
    size = imgs[0].size
    if shape is None:
        shape = (cuts * size[0] + (cuts - 1) * padding, cuts * size[0] + (cuts - 1) * padding)
    canvas = Image.new("RGB", shape, color=(255, 255, 255))
    for i in range(len(seq)):
        canvas.paste(imgs[i], ((seq[i] % cuts) * (size[1] + padding), (seq[i] // cuts) * (size[0] + padding), (seq[i] % cuts) * (size[1] + padding) + size[1], (seq[i] // cuts) * (size[0] + padding) + size[0]))
    if not silent:
        canvas.show()
    if save_path is not None:
        save_path += 'filled' if save_path[-1] in ['/', '\\'] else ''
        save_path += '.png' if '.png' not in save_path else ''
        canvas.save(save_path)
    return canvas


def block_upsize(imgs: list[Image], cuts=2, resize_shape=None):
    if resize_shape is not None:
        for i in range(len(imgs)):
            imgs[i] = jigsaw_filler(*jigsaw_cutter(imgs[i], cuts=cuts, resize_shape=resize_shape), padding=0)
    return imgs
