import numpy as np
import os
from mycode import *  # function, self-realized


# you need to create dir \pic, \p2krange, \p2grange in the project file to run the complete code
def cluster_task_1(sample):
    """
    载入位于data/data1.npy的数据。
    对于data1.npy中给定的1000个一维且Shape为(1)的向量,将它们聚类成两类,一类的向量的ID为0,另一类的向量的ID为1。

    Args:
        sample (np.ndarray): Shape: (1000, )

    Returns:
        label (np.ndarray): Shape: (1000, ), 其中保存的是一维聚类的结果,请保证label与sample的index一致
    """
    # label = np.zeros_like(sample)

    # your code here

    label = mtd4forP1(sample)

    return label


def cluster_task_2(sample):
    """
    载入位于data/data2.npy的数据。
    对于data2.npy中给定的1000个一维且Shape为(2)的向量,将它们聚类成N类,类别ID 从0至N-1。

    Args:
        sample (np.ndarray): Shape: (M, 2)

    Returns:
        label (np.ndarray): Shape: (M, ), 其中保存的是一维聚类的结果,请保证label与sample的index一致
    """
    # label = np.zeros((sample.shape[0]))

    # your code here

    label = mtd2ForP2Short(sample)

    return label


def cluster_task_3(sample):
    """
    载入位于data/data3.npy的数据。
    对于data3.npy中给定的1000个一维且Shape为(128)的向量,将它们聚类成3类,类别ID 从0至2。

    Args:
        sample (np.ndarray): Shape: (M, 128)

    Returns:
        label (np.ndarray): Shape: (M, ), 其中保存的是一维聚类的结果,请保证label与sample的index一致
    """
    # label = np.zeros((sample.shape[0]))

    # your code here

    label = mtd3ForP3(sample)

    return label


def cluster_task_4(sample):
    """
    载入位于data/data4.npy的数据。
    对于data4.npy中给定 10000 个一维且Shape为(128)的向量,将它们聚类成N类,类别ID 从0至N-1。

    Args:
        sample (np.ndarray): Shape: (M, 128)

    Returns:
        label (np.ndarray): Shape: (M, ), 其中保存的是一维聚类的结果,请保证label与sample的index一致
    """
    # label = np.zeros((sample.shape[0]))

    # your code here

    label = mtd1ForP4Short(sample)

    return label


def main():
    data1 = np.load(os.path.join("data", "data1.npy"))
    data2 = np.load(os.path.join("data", "data2.npy"))
    data3 = np.load(os.path.join("data", "data3.npy"))
    data4 = np.load(os.path.join("data", "data4.npy"))

    label1 = cluster_task_1(data1)
    label2 = cluster_task_2(data2)
    label3 = cluster_task_3(data3)
    label4 = cluster_task_4(data4)

    np.save(os.path.join("output", "label1.npy"), label1)
    np.save(os.path.join("output", "label2.npy"), label2)
    np.save(os.path.join("output", "label3.npy"), label3)
    np.save(os.path.join("output", "label4.npy"), label4)


if __name__ == '__main__':
    main()
