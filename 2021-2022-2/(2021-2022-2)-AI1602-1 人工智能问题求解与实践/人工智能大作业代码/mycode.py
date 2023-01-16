from Lo_clustering_with_dr import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

_data1 = np.load(os.path.join("data", "data1.npy"))
_data2 = np.load(os.path.join("data", "data2.npy"))
_data3 = np.load(os.path.join("data", "data3.npy"))
_data4 = np.load(os.path.join("data", "data4.npy"))


def plotP1():
    plt.figure(figsize=(10, 2))
    plt.scatter(_data1, np.zeros(_data1.shape), cmap='Spectral')
    plt.savefig('pics/p1raw.png')
    plt.show()


def mtd1ForP1(data=_data1):  # simple average
    total = 0
    label = []
    for i in data:
        total = total + i
    average = total / len(data)
    for i in range(1000):
        if data[i] < average:
            label.append(0)
        else:
            label.append(1)
    plt.figure(figsize=(10, 2))
    plt.scatter(data, np.zeros(data.shape), c=label, cmap='Spectral')
    plt.savefig('pics/m1p1.png')
    plt.show()
    return label


def mtd2ForP1(data=_data1):  # Kmeans
    label = KMeans(n_clusters=2, random_state=11).fit_predict(data.reshape(-1, 1))
    plt.figure(figsize=(10, 2))
    plt.scatter(data, np.zeros(data.shape), c=label, cmap='Spectral')
    plt.savefig('pics/m2p1.png')
    plt.show()
    return label


def plotP1Dis():
    sort_data1 = np.sort(_data1)
    dis1 = [sort_data1[1] - sort_data1[0]]
    for i in range(1, 999):
        dis1.append((sort_data1[i + 1] - sort_data1[i - 1]) / 2)
    dis1.append(sort_data1[999] - sort_data1[998])
    plt.figure(figsize=(10, 2))
    plt.ylabel('distance')
    plt.scatter(sort_data1, np.array(dis1), cmap='Spectral')
    plt.savefig('pics/distance1.png')
    plt.show()


def mtd3ForP1(data=_data1):  # Kernel + Kmeans
    y = []
    for i in range(data.shape[0]):
        mid = (np.max(data) + np.min(data)) / 2
        y.append(-(data[i] - mid) ** 4)
    data = np.stack((data, y), axis=1)
    label = KMeans(n_clusters=2).fit_predict(data)
    plt.figure(figsize=(10, 5))
    plt.scatter(data[:, 0], data[:, 1], c=label, cmap='Spectral')
    plt.savefig('pics/m3p1.png')
    plt.show()
    return label


def plotP1H():
    plt.figure(figsize=(6, 3))
    plt.hist(_data1, bins=45, edgecolor="black")
    plt.ylabel("frequency")
    plt.savefig('pics/his.png')
    plt.show()


def mtd4forP1(data=_data1):  # GMM
    gmm = GaussianMixture(n_components=2, KMeans_init=KMeans(random_state=11))
    label = gmm.fit_predict(data.reshape(-1, 1))
    # plt.figure(figsize=(10, 2))
    # plt.scatter(data, np.zeros(data.shape), c=label, cmap='Spectral')
    # plt.savefig('pics/m4p1.png')
    # plt.show()
    x = []
    for i in range(1000):
        x.append([i / 1000])
    mu, sigma = gmm.gaussian_output()
    y0 = gaussian(x, mu[0], sigma[0])
    y0 = np.array(y0).flatten()
    y1 = gaussian(x, mu[1], sigma[1])
    y1 = np.array(y1).flatten()
    x = np.array(x).flatten()
    data = normalize(data.reshape(-1, 1))
    plt.figure(figsize=(10, 3))
    plt.plot(x, y0, color='r')
    plt.plot(x, y1, color='b')
    plt.scatter(data, np.zeros(data.shape), c=label, cmap='Spectral')
    plt.savefig('pics/m4p1gaussian.png')
    plt.show()
    return label


def plotP2():
    plt.figure(figsize=(6, 4))
    plt.scatter(_data2[:, 0], _data2[:, 1], cmap='Spectral')
    plt.savefig('pics/p2raw.png')
    plt.show()


def mtd1ForP2(data=_data2):  # KMeans with Index
    nk = []
    DBI = []
    DunnI = []
    for k in range(2, 11):
        nk.append(k)
        kmeans = KMeans(n_clusters=k, random_state=1)
        label = kmeans.fit_predict(data)
        centroids = kmeans.centroids_output()
        plt.figure(figsize=(6, 4))
        plt.scatter(data[:, 0], data[:, 1], c=label, cmap='Spectral')
        plt.scatter(centroids[:, 0], centroids[:, 1], cmap='Spectral')
        plt.title('K=' + str(k), size=25)
        plt.savefig('p2krange/k=' + str(k) + '.png')
        plt.show()
        assess = ClusteringAssessment(data=data, label=label, centroids=kmeans.centroids_output())
        DBI.append(assess.DBI())
        DunnI.append(assess.DunnI())
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(111)
    ax1.plot(nk, DBI, 'r', label='DBI')
    ax1.set_ylabel('DBI')
    ax2 = ax1.twinx()
    ax2.plot(nk, DunnI, 'b', label='DunnI')
    ax2.set_xlabel('K')
    ax2.set_ylabel('DunnI')
    ax1.legend(loc='upper left', fontsize=15)
    ax2.legend(loc='upper right', fontsize=15)
    plt.title('KMeans', size=25)
    plt.savefig('pics/KM_DDI.png')
    plt.show()
    if DBI.index(min(DBI)) == DunnI.index(max(DunnI)):
        k = DBI.index(min(DBI)) + 2  # note that k start from 2
        print('According to DBI and DunnI, {} clusters is the best choice'.format(k))
        kmeans = KMeans(n_clusters=k, random_state=1)
        label = kmeans.fit_predict(data)
        centroids = kmeans.centroids_output()
        plt.figure(figsize=(6, 4))
        plt.scatter(data[:, 0], data[:, 1], c=label, cmap='Spectral')
        plt.scatter(centroids[:, 0], centroids[:, 1], cmap='Spectral')
        plt.title('KMeans', size=25)
        plt.savefig('pics/m1p2.png')
        plt.show()
        return label
    print('Unable to decide k!')
    return np.zeros(len(data))


def mtd2ForP2(data=_data2):  # GMM with index
    nk = []
    DBI = []
    DunnI = []
    for k in range(2, 11):
        nk.append(k)
        gmm = GaussianMixture(n_components=k, KMeans_init=KMeans(random_state=1))
        label = gmm.fit_predict(data)
        mu, _ = gmm.gaussian_output()
        plt.figure(figsize=(6, 4))
        plt.scatter(data[:, 0], data[:, 1], c=label, cmap='Spectral')
        plt.scatter(mu[:, 0], mu[:, 1], cmap='Spectral')
        plt.title('C=' + str(k), size=25)
        plt.savefig('p2grange/g=' + str(k) + '.png')
        plt.show()
        assess = ClusteringAssessment(data=data, label=label, centroids=gmm.gaussian_output()[0])
        DBI.append(assess.DBI())
        DunnI.append(assess.DunnI())
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(111)
    ax1.plot(nk, DBI, 'r', label='DBI')
    ax1.set_ylabel('DBI')
    ax2 = ax1.twinx()
    ax2.plot(nk, DunnI, 'b', label='DunnI')
    ax2.set_xlabel('K')
    ax2.set_ylabel('DunnI')
    ax1.legend(loc='upper left', fontsize=15)
    ax2.legend(loc='upper right', fontsize=15)
    plt.title('GMM', size=25)
    plt.savefig('pics/GM_DDI.png')
    plt.show()
    if DBI.index(min(DBI)) == DunnI.index(max(DunnI)):
        k = DBI.index(min(DBI)) + 2  # note that k start from 2
        print('According to DBI and DunnI, {} clusters is the best choice'.format(k))
        gmm = GaussianMixture(n_components=k, KMeans_init=KMeans(random_state=1))
        label = gmm.fit_predict(data)
        mu, _ = gmm.gaussian_output()
        plt.figure(figsize=(6, 4))
        plt.scatter(data[:, 0], data[:, 1], c=label, cmap='Spectral')
        plt.scatter(mu[:, 0], mu[:, 1], cmap='Spectral')
        plt.title('GMM', size=25)
        plt.savefig('pics/m2p2.png')
        plt.show()
        return label
    print('Unable to decide k!')
    return np.zeros(len(data))


def mtd2ForP2Short(data=_data2):
    gmm = GaussianMixture(n_components=4, KMeans_init=KMeans(random_state=1))
    label = gmm.fit_predict(data)
    mu, _ = gmm.gaussian_output()
    plt.figure(figsize=(6, 4))
    plt.scatter(normalize(data)[:, 0], normalize(data)[:, 1], c=label, cmap='Spectral')
    plt.scatter(mu[:, 0], mu[:, 1], cmap='Spectral')
    plt.title('GMM', size=25)
    plt.savefig('pics/m2p2.png')
    plt.show()
    return label


def plot(data, label=None, save=None, title=None):  # 3D plot
    if not len(label):
        label = np.zeros(len(data))
    fig = plt.figure()
    ax = Axes3D(fig, auto_add_to_figure=False)
    fig.add_axes(ax)
    ax.scatter3D(data[:, 0], data[:, 1], data[:, 2], c=label, cmap='Spectral')
    if save:
        plt.savefig(save)
    if title:
        plt.savefig(title, size=25)
    plt.show()
    return fig


def mtd1ForP3(data=_data3):  # DR first and Clustering
    plt.figure(figsize=(6, 4))
    _data = MDS(n_components=2).fit_reduce(data)
    plt.scatter(_data[:, 0], _data[:, 1], cmap='Spectral')
    plt.title('MDS', size=25)
    # plt.savefig('pics/p3MDS.png')
    # plt.show()
    plt.figure(figsize=(6, 4))
    kmeans = KMeans(n_clusters=3, random_state=1)
    label1 = kmeans.fit_predict(_data)
    plt.scatter(_data[:, 0], _data[:, 1], c=label1, cmap='Spectral')
    plt.title('MDS+KMeans', size=25)
    # plt.savefig('pics/p3MK2.png')
    # plt.show()
    plt.figure(figsize=(6, 4))
    gmm = GaussianMixture(n_components=3, KMeans_init=KMeans(random_state=1))
    label2 = gmm.fit_predict(_data)
    plt.scatter(_data[:, 0], _data[:, 1], c=label2, cmap='Spectral')
    # plt.title('MDS(reduced to 5)+GMM')
    # plt.savefig('pics/p3MG5.png')
    plt.show()
    plt.figure(figsize=(6, 4))
    _data = PCA(n_components=2).fit_reduce(data)
    plt.scatter(_data[:, 0], _data[:, 1], cmap='Spectral')
    plt.title('PCA', size=25)
    plt.savefig('pics/p3PCA.png')
    # plt.show()
    plt.figure(figsize=(6, 4))
    kmeans = KMeans(n_clusters=3, random_state=1)
    label3 = kmeans.fit_predict(_data)
    plt.scatter(_data[:, 0], _data[:, 1], c=label3, cmap='Spectral')
    plt.title('PCA+KMeans')
    # plt.show()
    plt.figure(figsize=(6, 4))
    gmm = GaussianMixture(n_components=3, KMeans_init=KMeans(random_state=1))
    label4 = gmm.fit_predict(_data)
    plt.scatter(_data[:, 0], _data[:, 1], c=label4, cmap='Spectral')
    plt.title('PCA+GMM')
    # plt.show()
    return label1


def mtd2ForP3(data=_data3):  # directly KMenas
    plot_data = MDS(n_components=2).fit_reduce(data)
    kmeans = KMeans(n_clusters=3, random_state=9)
    label1 = kmeans.fit_predict(data)
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_data[:, 0], plot_data[:, 1], c=label1, cmap='Spectral')
    plt.title('KMeans only', size=25)
    # plt.savefig('pics/P3K.png')
    # plt.show()
    plot_data = MDS(n_components=5).fit_reduce(data)
    kmeans = GaussianMixture(n_components=3, KMeans_init=KMeans(random_state=1))
    label2 = kmeans.fit_predict(data)
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_data[:, 0], plot_data[:, 1], c=label2, cmap='Spectral')
    plt.title('KMeans only')
    plt.show()
    return label1


def mtd3ForP3(data=_data3):  # PCA-Isomap and KMeans
    r2_data = MDS(n_components=2).fit_reduce(data)
    index = np.array([i for i in range(len(r2_data)) if r2_data[i][0] < 1])  # used simpler ways
    # i_data = Isomap(n_components=2, k=5).fit_reduce(data[index])
    # plt.figure(figsize=(6, 4))
    # plt.scatter(i_data[:, 0], i_data[:, 1], cmap='Spectral')
    # plt.savefig('pics/p3IsoR.png')
    # plt.show()
    r5_data = PCA(n_components=5).fit_reduce(data)
    i_data = Isomap(n_components=2, k=5).fit_reduce(r5_data[index])
    kmeans = KMeans(n_clusters=2)
    label = kmeans.fit_predict(i_data)
    plt.figure(figsize=(6, 4))
    plt.scatter(i_data[:, 0], i_data[:, 1], c=label, cmap='Spectral')
    plt.savefig('pics/p3IsoK.png')
    plt.show()
    label += 1
    final_label = np.zeros(len(data))
    final_label[index] = label
    plt.figure(figsize=(6, 4))
    plt.scatter(r2_data[:, 0], r2_data[:, 1], c=final_label, cmap='Spectral')
    plt.savefig('pics/p3Fin.png')
    plt.show()
    r3_data = MDS(n_components=3).fit_reduce(data)
    plot(data=r3_data, label=final_label, save='pics/p3Fin3.png')
    return final_label


def plotP4():
    plot_mds = MDS(n_components=2).fit_reduce(_data4)
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_mds[:, 0], plot_mds[:, 1], cmap='Spectral')
    plt.title('MDS', size=25)
    plt.savefig('pics/P4RM_full.png')
    plt.show()
    plot_pca = PCA(n_components=2).fit_reduce(_data4)
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_pca[:, 0], plot_pca[:, 1], cmap='Spectral')
    plt.title('PCA', size=25)
    plt.savefig('pics/P4RP_full.png')
    plt.show()
    plot_mds = MDS(n_components=2).fit_reduce(_data4[::5])
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_mds[:, 0], plot_mds[:, 1], cmap='Spectral')
    plt.title('MDS', size=25)
    plt.savefig('pics/P4RM.png')
    plt.show()
    plot_pca = PCA(n_components=2).fit_reduce(_data4[::5])
    plt.figure(figsize=(6, 4))
    plt.scatter(plot_pca[:, 0], plot_pca[:, 1], cmap='Spectral')
    plt.title('PCA', size=25)
    plt.savefig('pics/P4RP.png')
    plt.show()


def mtd1ForP4(data=_data4[::10]):  # reduced and KMeans
    data_pca = PCA(n_components=3).fit_reduce(data)
    nk = []
    DBI = []
    DunnI = []
    for k in range(2, 11):
        nk.append(k)
        kmeans = KMeans(n_clusters=k, random_state=10)
        label = kmeans.fit_predict(data_pca)
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('K=' + str(k), size=25)
        plt.savefig('p2krange/4k=' + str(k) + '.png')
        plt.show()
        assess = ClusteringAssessment(data=data_pca, label=label, centroids=kmeans.centroids_output())
        DBI.append(assess.DBI())
        DunnI.append(assess.DunnI())
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(111)
    ax1.plot(nk, DBI, 'r', label='DBI')
    ax1.set_ylabel('DBI')
    ax2 = ax1.twinx()
    ax2.plot(nk, DunnI, 'b', label='DunnI')
    ax2.set_xlabel('K')
    ax2.set_ylabel('DunnI')
    ax1.legend(loc='upper left', fontsize=15)
    ax2.legend(loc='upper right', fontsize=15)
    plt.title('KMeans', size=25)
    plt.savefig('pics/KM_DDI4.png')
    plt.show()
    if DBI.index(min(DBI)) == DunnI.index(max(DunnI)):
        k = DBI.index(min(DBI)) + 2  # note that k start from 3
        print('According to DBI and DunnI, {} clusters is the best choice'.format(k))
        kmeans = KMeans(n_clusters=k, random_state=2)
        label = kmeans.fit_predict(data_pca)
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('KMeans', size=25)
        plt.savefig('pics/m1p4.png')
        plt.show()
        return label
    print('Unable to decide k!')
    return np.zeros(len(data))


def mtd2ForP4(data=_data4[::10]):  # reduced and GMM
    data_pca = PCA(n_components=3).fit_reduce(data)
    nk = []
    DBI = []
    DunnI = []
    for k in range(2, 11):
        nk.append(k)
        gmm = GaussianMixture(n_components=k, KMeans_init=KMeans(random_state=10))
        label = gmm.fit_predict(data_pca)
        mu, _ = gmm.gaussian_output()
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('C=' + str(k), size=25)
        plt.savefig('p2grange/4g=' + str(k) + '.png')
        plt.show()
        assess = ClusteringAssessment(data=data_pca, label=label, centroids=gmm.gaussian_output()[0])
        DBI.append(assess.DBI())
        DunnI.append(assess.DunnI())
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(111)
    ax1.plot(nk, DBI, 'r', label='DBI')
    ax1.set_ylabel('DBI')
    ax2 = ax1.twinx()
    ax2.plot(nk, DunnI, 'b', label='DunnI')
    ax2.set_xlabel('K')
    ax2.set_ylabel('DunnI')
    ax1.legend(loc='upper left', fontsize=15)
    ax2.legend(loc='upper right', fontsize=15)
    plt.title('GMM', size=25)
    plt.savefig('pics/GM_DDI4.png')
    plt.show()
    if DBI.index(min(DBI)) == DunnI.index(max(DunnI)):
        k = DBI.index(min(DBI)) + 2  # note that k start from 2
        print('According to DBI and DunnI, {} clusters is the best choice'.format(k))
        gmm = GaussianMixture(n_components=k, KMeans_init=KMeans(random_state=1))
        label = gmm.fit_predict(data_pca)
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('GMM', size=25)
        plt.savefig('pics/m2p4.png')
        plt.show()
        return label
    print('Unable to decide k!')
    return np.zeros(len(data))


def mtd3ForP4(data=_data4[::10]):  # directly KMeans
    data_pca = PCA(n_components=3).fit_reduce(data)
    nk = []
    DBI = []
    DunnI = []
    for k in range(2, 11):
        nk.append(k)
        kmeans = KMeans(n_clusters=k, random_state=2)
        label = kmeans.fit_predict(data)
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('K=' + str(k), size=25)
        plt.savefig('p2krange/4dk=' + str(k) + '.png')
        plt.show()
        assess = ClusteringAssessment(data=data, label=label, centroids=kmeans.centroids_output())
        DBI.append(assess.DBI())
        DunnI.append(assess.DunnI())
    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(111)
    ax1.plot(nk, DBI, 'r', label='DBI')
    ax1.set_ylabel('DBI')
    ax2 = ax1.twinx()
    ax2.plot(nk, DunnI, 'b', label='DunnI')
    ax2.set_xlabel('K')
    ax2.set_ylabel('DunnI')
    ax1.legend(loc='upper left', fontsize=15)
    ax2.legend(loc='upper right', fontsize=15)
    plt.title('KMeans', size=25)
    plt.savefig('pics/KM_DDI4D.png')
    plt.show()
    if DBI.index(min(DBI)) == DunnI.index(max(DunnI)):
        k = DBI.index(min(DBI)) + 2  # note that k start from 3
        print('According to DBI and DunnI, {} clusters is the best choice'.format(k))
        kmeans = KMeans(n_clusters=k, random_state=2)
        label = kmeans.fit_predict(data)
        plt.figure(figsize=(6, 4))
        plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
        plt.title('KMeans', size=25)
        plt.savefig('pics/m3p4.png')
        plt.show()
        return label
    print('Unable to decide k!')
    return np.zeros(len(data))


def mtd1ForP4Short(data=_data4):
    data_pca = PCA(n_components=3).fit_reduce(data)
    kmeans = KMeans(n_clusters=5, random_state=10)
    label = kmeans.fit_predict(data_pca)
    plt.figure(figsize=(6, 4))
    plt.scatter(data_pca[:, 0], data_pca[:, 1], c=label, cmap='Spectral')
    plt.savefig('pics/p4Fin.png')
    plt.show()
    return label
