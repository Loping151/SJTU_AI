from PIL import Image
import jittor as jt
import numpy as np
from calc_utils import simple_solver
from data_loader import get_dataset

acc = 0
data1, data2 = get_dataset(2, shuffle=False, resize_piece=(64, 64))
for i in range(len(data1) // 24):
    x = data1[24 * i]
    y = x[3]
    z = [Image.fromarray((255 * x[2][j].transpose((1, 2, 0)).numpy()).astype(np.uint8)) for j in range(4)]
    a = simple_solver(z)
    if jt.max(jt.abs(a - y)) == 0:
        acc = acc + 1
print('if upsize to 64 as a whole:')
print('acc on train data:', acc / len(data1) * 24)

acc = 0
for i in range(len(data2) // 24):
    x = data2[24 * i]
    y = x[3]
    z = [Image.fromarray((255 * x[2][j].transpose((1, 2, 0)).numpy()).astype(np.uint8)) for j in range(4)]
    a = simple_solver(z)
    if jt.max(jt.abs(a - y)) == 0 == 0:
        acc = acc + 1
print('acc on test data:', acc / len(data2) * 24)
