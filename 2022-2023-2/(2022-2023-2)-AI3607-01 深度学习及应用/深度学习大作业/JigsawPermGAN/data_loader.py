import jittor as jt
from cifar import CIFAR10
from jittor.dataset import Dataset
from jittor import transform
from math import factorial
from jigsaw_utils import jigsaw_shuffle_all, block_upsize, jigsaw_filler


class JigsawPuzzle(Dataset):
    def __init__(self, raw, data, cuts=2, batch_size=32, shuffle=True):
        super().__init__(batch_size=batch_size, shuffle=shuffle)
        self.raw = raw
        self.data = data
        self.repeat = factorial(cuts ** 2)
        self.total = len(self.raw)
        self.cuts = int(len(data[0][0]) ** 0.5)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        original_images = jt.array(transform.to_tensor(self.raw[idx // self.repeat]))
        shuffled_images = jt.array(transform.to_tensor(jigsaw_filler(*self.data[idx // self.repeat], padding=0)))
        image_pieces = jt.array([transform.to_tensor(self.data[idx][0][i]) for i in range(self.cuts ** 2)])
        label_sequence = jt.array(self.data[idx][1])
        return original_images, shuffled_images, image_pieces, label_sequence  # original image, shuffled image, pieces, label sequence


def get_dataset(cuts, data_root='./data', batch_size=32, shuffle=True, resize_shape=None, resize_piece=None, prob=1, with_original=True, download=False):
    original_set = CIFAR10(root=data_root, train=True, download=download, resize=resize_shape)
    original_set = [original_set[i][0] for i in range(len(original_set))]
    original_test = CIFAR10(root=data_root, train=False, download=download, resize=resize_shape)
    original_test = [original_test[i][0] for i in range(len(original_test))]
    train_loader = JigsawPuzzle(block_upsize(original_set, cuts=cuts, resize_shape=resize_piece), jigsaw_shuffle_all(original_set, cuts=cuts, resize_shape=resize_piece, with_original=with_original, prob=prob), cuts, batch_size, shuffle)
    test_loader = JigsawPuzzle(block_upsize(original_test, cuts=cuts, resize_shape=resize_piece), jigsaw_shuffle_all(original_test, cuts=cuts, resize_shape=resize_piece, with_original=with_original, prob=prob), cuts, 200, shuffle)
    return train_loader, test_loader
