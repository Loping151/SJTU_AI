from jittor.dataset.cifar import CIFAR10
from PIL import Image
from typing import Union
import jittor as jt
from jittor import nn
from jittor.dataset import Dataset
from jittor import transform
import numpy as np
from itertools import permutations
from math import factorial

jt.flags.use_cuda = 1
jt.flags.use_tensorcore = 1


# %%
def jigsaw_cutter(img: Image, cuts: int, shape=None):
    if shape is None:
        shape = img.size
    assert shape[0] % cuts == 0 and shape[1] % cuts == 0
    imgs = []
    stepx, stepy = shape[0] // cuts, shape[1] // cuts
    for i in range(cuts):
        for j in range(cuts):
            imgs.append(img.crop((j * stepx, i * stepy, (j + 1) * stepx, (i + 1) * stepy)))
    return imgs, range(cuts ** 2)


def jigsaw_shuffle(imgs: list[Image], seq: list[int], order=None):
    if order is None:
        sseq = np.arange(len(seq))
        np.random.shuffle(sseq)
        sseq = sseq.tolist()
    else:
        sseq = order
    return [imgs[indice] for indice in sseq], [seq[indice] for indice in sseq]


def jigsaw_shuffle_all(dataset, cuts=2):
    shuffle_all = []
    for oda in dataset:
        cutted = jigsaw_cutter(oda, cuts)
        for per in permutations(np.arange(cuts ** 2)):
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


# %%
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


def get_dataset(cuts, batch_size=32, shuffle=True):
    original_set = CIFAR10(root='data/', train=True, download=False)
    original_set = [original_set[i][0] for i in range(len(original_set))][:1000]  # a list containing all 50000 PIL images
    original_test = CIFAR10(root='data/', train=False, download=False)
    original_test = [original_test[i][0] for i in range(len(original_test))]
    train_loader = JigsawPuzzle(original_set, jigsaw_shuffle_all(original_set, cuts=cuts), cuts, batch_size, shuffle)
    test_loader = JigsawPuzzle(original_test, jigsaw_shuffle_all(original_test, cuts=cuts), cuts, batch_size, shuffle)
    return train_loader, test_loader


# %%
# for original, shuffled, traind, labeld in get_dataset(2, batch_size=500)[0]:
#     print(original.shape, shuffled.shape, traind.shape, labeld.shape)
# print(np.array(get_dataset(2)[0][1][1]).shape)


# %%
class Discriminator(nn.Module):
    pass


class Classifier(nn.Module):
    def __init__(self, P, cut: int = 2, shape: Union[tuple, int] = (16, 16)):
        super().__init__()
        if type(shape) is int:
            shape = (shape, shape)
        self.conv1 = nn.Conv2d(64 + 3 * cut ** 2, 32, 3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding=1)
        self.linear1 = nn.Linear(64 * shape[0] * shape[1], 4096)
        self.linear2 = nn.Linear(4096, P)
        self.relu = nn.Relu()

    def execute(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view((x.shape[0], -1))
        x = self.relu(self.linear1(x))
        x = self.linear2(x)
        with open('logclass.txt', 'a') as f:
            f.writelines(str(x.view(-1)))
            f.writelines('\n')
        return x


class Encoder(nn.Module):
    def __init__(self, cut: int = 2, with_raw=True):
        super().__init__()
        self.with_raw = with_raw
        self.raw = None
        self.conv1 = nn.Conv2d(3 * cut ** 2, 32, 5, stride=1, padding=2)
        self.conv2 = nn.Conv2d(32, 32, 3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.bn3 = nn.BatchNorm2d(64)
        self.relu = nn.Relu()

    def execute(self, x):
        if self.with_raw:
            self.raw = x
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.relu(self.conv2(x))
        x = self.relu(self.bn3(self.conv3(x)))
        with open('logencode.txt', 'a') as f:
            f.writelines(str(x.view(-1)))
            f.writelines('\n')
        if self.with_raw:
            x = jt.concat([self.raw, x], dim=1)
        return x


# transfun = transform.Compose([
#     transform.Resize((224, 224)),
#     transform.ToTensor(),
#     transform.ImageNormalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
# ])
#
# backbone = resnet18(pretrained=True)
# # print(list(backbone.children()))
# modules = list(backbone.children())[:-2]
# backbone = jt.nn.Sequential(*modules)
# %%
encodel = Encoder()
data = None

# for _, _, i, j in get_dataset(2)[0]:
#     print(np.array(i).shape, np.array(j).shape)
#     data = i.reshape(i.shape[0], -1, *i.shape[-2:])
#     break
#
# features = encodel(data)
# print(features.shape)
# feature1 = features[0][0]
# print(feature1.shape)
# Image.fromarray((255 * feature1.numpy()).astype(np.uint8)).save(f'output/test_feature.png', save_all=True)
#
# cladel = Classifier(1000)
# result = cladel(features)
# print(result.shape)


# %%
class JigsawSolver(nn.Module):
    def __init__(self, cut: int = 2, shape: Union[tuple, int] = (16, 16)):
        super().__init__()
        if type(shape) is int:
            shape = (shape, shape)
        # self.conv1 = nn.Conv2d(64 + 3 * cut ** 2, 32, 3, stride=1, padding=1)
        self.conv1 = nn.Conv2d(3 * cut ** 2, 32, 5, stride=1, padding=2)
        self.conv2 = nn.Conv2d(32, 64, 3, stride=1, padding=1)
        self.linear1 = nn.Linear(64 * shape[0] * shape[1], 4096)
        self.linear2 = nn.Linear(4096, cut ** 2)
        self.relu = nn.Relu()
        self.sigmoid = nn.Sigmoid()

    def execute(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = x.view((x.shape[0], -1))
        x = self.sigmoid(self.linear1(x))
        x = self.linear2(x)
        with open('logclass.txt', 'a') as f:
            f.writelines(str(x.view(-1)))
            f.writelines('\n')
        return x


# %%
from animation import rolling_ball

model = JigsawSolver()
encoder = Encoder()
train_loader, test_loader = get_dataset(2)
criterion = nn.L1Loss()
optimizer_encoder = nn.Adam(encoder.parameters(), lr=0.1)
optimizer_model = nn.Adam(model.parameters(), lr=0.1)
lr_scheduler_model = jt.lr_scheduler.StepLR(optimizer_model, step_size=20, gamma=0.2)
num_epochs = 2
for epoch in range(num_epochs):
    for original, shuffled, train_data, train_seq in train_loader:
        print(original.shape, shuffled.shape, train_data.shape, train_seq.shape)
        pred_seq = model(train_data.view(train_data.shape[0], -1, 16, 16))
        loss = criterion(pred_seq, train_seq)
        optimizer_model.__setattr__('lr', optimizer_model.lr)
        optimizer_encoder.__setattr__('lr', optimizer_model.lr)
        optimizer_model.zero_grad()
        optimizer_model.backward(loss)
        optimizer_model.step()
        optimizer_encoder.zero_grad()
        optimizer_encoder.backward(loss)
        optimizer_encoder.step()
        rolling_ball(7, 0, f"Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}")
        lr_scheduler_model.step()
# %%
test_acc = 0
for original, shuffled, test_data, test_seq in test_loader:
    pred_seq = model(encoder(test_data.view(test_data.shape[0], -1, 16, 16)))
    print(pred_seq, test_seq)
    break
print('test accuracy: {:.4f}'.format(test_acc / len(test_loader) / test_loader.batch_size))


# %%
def simple_solver(imgs: list[Image]):
    cuts = int(len(imgs) ** 0.5)
    all_res = []
    for per in permutations(np.arange(cuts ** 2)):
        all_res.append(jigsaw_filler(imgs, per))
    return all_res
