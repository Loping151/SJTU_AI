import numpy as np


def get_sub_set(nums):
    sub_sets = [[]]
    for x in nums:
        sub_sets.extend([item + [x] for item in sub_sets])
    return [sum(i)for i in sub_sets][1:]


# 随机生成
n = 3
s = [np.random.randint(-100, 100) for i in range(n)]
print('Ans should be', s)
# 自定义
# s = [1, -3, 5, -7]
print('Input:', len(s), np.array(get_sub_set(s)))
