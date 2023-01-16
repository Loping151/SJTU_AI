import numpy as np
import random


# author: Loping151(SJTU)(that's why Lo_clustering)
# AI homework, finished 2022.6
# email: wangkailing151@gmail.com


# basic functions


# basic distance function
# param: 'rt' means you want the sqrt or not, default False because it is used only in KMeans, used to compare
def EuclideanDistance(p1, p2, rt=True):
    dimension = len(p1)
    dis = 0.0
    for i in range(dimension):
        dis += (p1[i] - p2[i]) ** 2
    # if wo just want to compare, sqrt is not necessary
    if rt:
        dis = np.sqrt(dis)
    return dis


# default distance compare for KMeans
def default_cmp(p1, p2):
    return EuclideanDistance(p1, p2, rt=False)


# another distance function, default Manhattan distance, can be used as param in kmeans or assessment
def MinkowskiDistance(p1, p2,
                      p=1):  # p = 1 for Manhattan Distance, p = 2 for Euclidean Distance, and p->+oo for Chebyshev Distance
    dimension = len(p1)
    dis = 0.0
    for i in range(dimension):
        dis += (p1[i] - p2[i]) ** p
    dis = np.power(dis, 1 / p)
    return dis


# add vector by value, for I didn't know we are allowed to use numpy in the beginning
def VectorAdd(v1, v2):  # add vectors by value
    dimension = len(v1)
    for i in range(dimension):
        v2[i] += v1[i]
    return v2


# divide vector with const
def VectorDivide(v, d):  # vector divided by const
    dimension = len(v)
    for i in range(dimension):
        v[i] /= d
    return v


# not necessary, but I met a bug: if you use numpy to calculate x.T.dot(x), x=[1 2], you will get 5. I know it's my fault, but I should remind muself.
def VectorTVector(v):  # x.T.dot(x)
    dimension = len(v)
    m = np.zeros((dimension, dimension))
    for i in range(dimension):
        m[i][i] = v[i] ** 2
        for j in range(1, dimension):
            m[i][j] = m[j][i] = v[i] * v[[j]]
    return m


# clustering: KMeans
# param:
#   n_clusters, random_state are same as sklearn
#   centroids is optional, you can decide centroids your self, should be like [[], [], ..., []]. I used it to debug
#   dis is the distance method you use, you can write your own method: the form is f(p1, p2) return MinkowskiDistance(p1, p2, p=10)
#   tol is tolerance, when movement(defined as sum of dis(new centroid, old centroid)) is lower than tol, it means converge
#   stop is max iteration, after this number of rounds the KMeans stops and give warning
# method:
#   .init_centroids(data)
#       inner function
#       data should be shape(num_of_points, dimension), same below
#       use gaussian function to initialize value between [mu-sigma, mu+sigma) on certain dimension, no return
#   .fit_predict(data)
#       same data to init.
#       standard KMeans process, return label
#   .centroids_output()
#       output self.centroids, [[], [], ..., []]
class KMeans:  # initially used sklearn, so I decide to use exactly the same API. None of the code is copied from the Internet
    def __init__(self, n_clusters=2, random_state=-1, centroids=None, dis=default_cmp, tol=1e-5, stop=1000):
        if centroids is None:
            centroids = []
        self.centroids = centroids  # you can decide the original centroids
        self.label = []  # the result label
        self.n_clusters = n_clusters  # how many clusters
        self.random_state = random_state  # random seed
        self.dis = dis  # choose distance function
        self.tol = tol  # break tolerance
        self.stop = stop  # max iterations

    def init_centroids(self, data):
        if self.centroids:  # no need to initialize
            return
        dimension = len(data[0])
        if self.random_state != -1:  # value -1 means don't initialize seed
            random.seed(self.random_state)  # else use system time as seed
        mu = []
        sigma = []
        for i in range(dimension):  # calculate the mu and sigma of each dimension
            vector_x = data[:, i]
            mu.append(np.mean(vector_x))
            sigma.append(np.std(vector_x))
        while len(self.centroids) < self.n_clusters:
            centroid = []
            for i in range(dimension):
                centroid.append(
                    random.random() * 2 * sigma[i] - sigma[i] + mu[
                        i])  # generate an x in the range [mu-sigma, mu+sigma), used random instead of np
            if centroid not in self.centroids:  # repeated centroid is not allowed
                self.centroids.append(centroid)
        self.centroids = np.array(self.centroids)

    def fit_predict(self, data):
        self.init_centroids(data)
        size = len(data)
        for it in range(self.stop):
            print('Round', it, end=' ')
            distance = []
            for i in range(size):
                distance.append([self.dis(data[i], self.centroids[j]) for j in
                                 range(self.n_clusters)])  # calculate distance
            self.label = np.array(distance).argmin(axis=1).flatten()  # get all points labeled
            count = []
            old = np.copy(self.centroids)
            for i in range(self.n_clusters):  # reinitialize
                count.append(0)
            for i in range(size):
                count[self.label[i]] += 1
                self.centroids[self.label[i]] = self.centroids[self.label[i]] + data[i]
            movement = 0
            for i in range(self.n_clusters):
                if count[i]:  # else none of the points belongs to it
                    self.centroids[i] = self.centroids[i] / count[i]
                movement += self.dis(self.centroids[i], old[i])
            if movement < self.tol:
                print('\rFeedback from KMeans:\n\tConverged after {} rounds. Final movement: {}'.format(it, movement))
                break
            print('\r', end='')
            if it == self.stop - 1:
                print('Feedback from KMeans:\n\tWarning: did not converge! Final movement: {}'.format(movement))
        return self.label

    def centroids_output(self):
        return self.centroids


# basic functions for gaussian distribution


# standard gaussian distribution function
# param: data should be array-like, for example np.array([[], [], ..., []]), mu(a point: [], len = dimension) and sigma(dimension*dimension cov matrix) should be given
# return prob, is a list [...]
def gaussian(data, mu, sigma):  # mul-dimensional gaussian distribution
    dimension = len(data[0])
    prob = []
    x = []
    det_sigma = np.linalg.det(sigma)  # in case singular, you can add alpha(usually 1e-3)*np.eye(dimension) to sigma
    inv_sigma = np.linalg.inv(sigma)
    for point in data:
        x.append(point - mu)
    x = np.array(x)
    for i in range(len(x)):
        prob.append(1.0 / (np.sqrt(np.power(2 * np.pi, dimension) * np.abs(det_sigma))) *
                    np.exp(-0.5 * np.array(x[i]).dot(inv_sigma).dot(x[i].T)))
    return prob


# data normalize, scale all dimension into [0, 1], return data with shape
def normalize(data):
    data = np.copy(data)
    for i in range(len(data[0])):
        x_max = np.max(data[:, i])
        x_min = np.min(data[:, i])
        data[:, i] = (data[:, i] - x_min) / (x_max - x_min)
    return data


# clustering: GaussianMixture
# param:
#   n_components, random_state just like sklearn, but if you use kmeans to init, random_state becomes useless
#   KMeans_init: it's very nise to initialize by kmeans to get mu(centroids), for I didn't write very efficient initialization method for mu
#   tol and stop same as kmeans, whether to stop according to movement of gamma
# method:
#   .init_components(data)
#       inner function
#       KMeans or random norm initialization, no return
#   .expectation(data)
#       inner function
#       update gamma, which is Responsiveness Matrix shape(num_of_points, num_of_models), no return
#   .step(data)
#       inner function
#       update mu and sigma, one round iteration, no return
#   .fit_predict(data)
#       just like kmeans
#   .gaussian_output()
#       return mu and sigma of each model
class GaussianMixture:
    def __init__(self, n_components=2, random_state=-1, KMeans_init=KMeans(), tol=1e-5, stop=5000):
        self.label = []  # the result label
        self.n_components = n_components  # how many components
        self.random_state = random_state  # random seed
        self.kmeans = KMeans_init  # init with kmeans model, you can also give KMeans_init = None
        self.tol = tol  # break tolerance
        self.stop = stop  # max iterations
        self.components = []  # components=[alpha, mu, sigma]
        self.gamma = []  # response

    def init_components(self, data):
        dimension = len(data[0])
        if self.random_state != -1:  # value -1 means don't initialize seed
            np.random.seed(self.random_state)  # here I use np.random
        alpha = np.array([1.0 / self.n_components] * self.n_components)  # sum alpha = 1
        self.components.append(alpha)
        if self.kmeans:
            self.kmeans.n_clusters = self.n_components
            self.kmeans.fit_predict(data)
            self.components.append(self.kmeans.centroids_output())
        else:
            mu = np.random.rand(self.n_components, dimension)
            self.components.append(mu)
        sigma = np.array([0.01 * np.eye(dimension)] * self.n_components)  # diagonal array
        self.components.append(sigma)

    def expectation(self, data):  # calculate gamma
        size = len(data)
        self.gamma = np.zeros((size, self.n_components))
        prob = np.zeros((size, self.n_components))
        for i in range(self.n_components):
            prob[:, i] = np.array(gaussian(data, self.components[1][i], self.components[2][i]))
        for i in range(self.n_components):
            self.gamma[:, i] = self.components[0][i] * prob[:, i]
        for i in range(size):
            self.gamma[i] /= np.sum(self.gamma[i])

    def step(self, data):  # update alpha, mu and sigma
        dimension = len(data[0])
        size = len(data)
        self.components[2] = []
        for k in range(self.n_components):
            sum_gamma = np.sum(self.gamma[:, k])
            sigma = np.zeros((dimension, dimension))
            for i in range(size):
                sigma += self.gamma[i][k] * VectorTVector(data[i] - self.components[1][k])
            self.components[2].append(sigma / sum_gamma)
            self.components[0][k] = sum_gamma / size
        self.components[2] = np.array(self.components[2])

    def fit_predict(self, data):
        data = normalize(data)
        self.init_components(data)
        for it in range(self.stop):
            print('Round', it, end=' ')
            if not it:  # first round when gamma is []
                gamma = np.zeros((len(data), self.n_components))
            else:
                gamma = np.copy(self.gamma)
            self.expectation(data)
            if np.sum(np.abs(gamma - self.gamma)) < self.tol:
                print('\rFeedback from GMM:\n\tConverged after {} rounds. Final movement: {}'.format(it, np.sum(
                    np.abs(gamma - self.gamma))))
                break
            self.step(data)
            print('\r', end='')
            if it == self.stop - 1:
                print('Feedback from GMM:\n\tWarning: did not converge! Final movement: {}'.format(
                    np.sum(np.abs(gamma - self.gamma))))
        self.label = self.gamma.argmax(axis=1).flatten()
        return self.label

    def gaussian_output(self):  # return mu and sigma
        return self.components[1], self.components[2]


# Assessment functions:
# default distance for assessment
def default_dis(p1, p2):
    return MinkowskiDistance(p1, p2,
                             p=2)  # sqrt EuclideanDistance, can be replaced with EuclideanDistance(p1, p2, rt = True)


# assessment(inner)
# param:
#   data: the original data or scaled data
#   label: result from a converged model, at least two clusters, and each clusters must have at least two points to calculate in_cluster distance
#   centroids: centroids_output from kmeans or mu from GMM, be like [[], [], ..., []]
#   dis: distance method
# method:
#   avg, diam, d_min, d_cen:
#       inner function, used in formulas
#   DBI: Davies-Bouldin Index
#   DunnI: Dunn Index
class ClusteringAssessment:
    def __init__(self, data, label, centroids, distance=default_dis):
        self.label = label
        self.n_clusters = np.max(label) + 1  # label must be range(0, max)
        self.centroids = centroids
        self.data = [[data[j] for j in range(len(data)) if label[j] == i] for i in
                     range(self.n_clusters)]
        self.dis = distance

    def avg(self, c):
        num = list(self.label).count(c)
        sum_dis = 0.0
        for i in range(num):
            for j in range(i, num):
                sum_dis += self.dis(self.data[c][i], self.data[c][j])
        return 2 * sum_dis / (num * (num - 1))  # this means each label should have at least two point to be effective

    def diam(self, c):
        num = list(self.label).count(c)
        max_dis = 0.0
        for i in range(num):
            for j in range(i, num):
                d = self.dis(self.data[c][i], self.data[c][j])
                if d > max_dis:
                    max_dis = d
        return max_dis

    def d_min(self, ci, cj):
        min_dis = self.dis(self.data[ci][0],
                           self.data[cj][0])
        for i in self.data[ci]:
            for j in self.data[cj]:
                d = self.dis(i, j)
                if d < min_dis:
                    min_dis = d
        return min_dis

    def d_cen(self, ci, cj):
        return self.dis(self.centroids[ci], self.centroids[cj])

    def DBI(self):  # the lower, the better
        score = 0.0
        print('Assessment calculating: DBI ', end='')
        for i in range(self.n_clusters):
            print(str(i + 1) + '/' + str(self.n_clusters), end='')
            score += max((self.avg(i) + self.avg(j)) / self.d_cen(i, j) for j in range(self.n_clusters) if j != i)
            print('\b' * len(str(i + 1) + '/' + str(self.n_clusters)), end='')
        print('\r', end='')
        return score / self.n_clusters

    def DunnI(self):  # the higher, the better
        min_d_min = self.d_min(0, 1)  # at least 2 cluster needed
        print('Assessment calculating: DunnI ', end='')
        for i in range(self.n_clusters):
            print(str(i + 1) + '/' + str(self.n_clusters), end='')
            dm = min(self.d_min(i, j) for j in range(self.n_clusters) if j != i)
            min_d_min = min(min_d_min, dm)
            print('\b' * len(str(i + 1) + '/' + str(self.n_clusters)), end='')
        max_diam = max(self.diam(i) for i in range(self.n_clusters))
        print('\r', end='')
        return min_d_min / max_diam


# dimensionality reduction methods


# multiple dimensional scaling
# param:
#   data is the original data, n_components is the target dimension
# method:
#   fit_reduce
#   there is a strange param called _inner_mode, which is used inside Isomap only
#   return reduced data
class MDS:
    def __init__(self, n_components=2, dis=default_cmp):
        self.n_components = n_components
        self.dis = dis

    def fit_reduce(self, data, _inner_mode=False):
        size = len(data)
        dist = np.zeros((size, size))  # distance matrix D. here is actually dist_ij^2, no need to sqrt
        dist_i = np.zeros(size)  # also square dist
        dist_j = np.zeros(size)
        print('Distance calculation: total = {}   '.format(size), end='')
        if _inner_mode:
            dist = data  # _inner_mode is on means data given is also dist from Isomap
        else:
            for i in range(size):
                for _ in range(0, len(str(i - 1))):
                    print('\b', end='')
                print('.', i, sep='', end='')
                dist[i] = np.sum(np.square(data[i] - data), axis=1).T  # so written, much faster
                if not (i + 1) % 15:
                    print('\b' * 15, end='')
        dist_ij = np.mean(dist)
        print('\rMDS calculating......', end='')
        for k in range(size):
            dist_i[k] = np.mean(dist[k])
            dist_j[k] = np.mean(dist[:, k])
        B = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                B[i][j] = -0.5 * (dist[i][j] - dist_i[i] - dist_j[j] + dist_ij)
        eigenvalues, eigenvectors = np.linalg.eigh(B)
        index = np.argsort(-eigenvalues)[:self.n_components]  # sort from big to small
        diag_eigenvalues = np.sqrt(np.diag(-np.sort(-eigenvalues)[:self.n_components]))
        selected_v = eigenvectors[:, index]
        Z = selected_v.dot(diag_eigenvalues)
        print('\rFeedback from MDS:\n\tReduced from {} to {}'.format(len(data[0]), self.n_components))
        return Z


# principal component analysis
# param:
#   same as MDS, no dis
# method:
#   same as MDS
class PCA:
    def __init__(self, n_components=2):
        self.n_components = n_components

    def fit_reduce(self, data):
        centre = np.mean(data, axis=0)
        data = data - centre  # zero centred
        cov = np.cov(data.T)
        eigenvalues, eigenvectors = np.linalg.eigh(cov)
        index = np.argsort(eigenvalues)[-self.n_components:]  # sort from big to small
        selected_v = eigenvectors[:, index]
        W = data.dot(selected_v)
        print('\rFeedback from PCA:\n\tReduced from {} to {}'.format(len(data[0]), self.n_components))
        return np.fliplr(W)  # flip to look better


# Isometric Mapping
# param:
#   n_components: same as MDS, distance is EuclideanDistance squared
#   k: for KNN used inside
#   method: PCA or MDS here
# method:
#   fit_reduce(data):
#       same as MDS
#   dijkstra(data, start):
#       inner static method
#       used for KNN, update dist
class Isomap:
    def __init__(self, n_components, dis=default_dis, k=5):
        self.n_components = n_components
        self.dis = dis
        self.k = k

    @staticmethod  # I just want to write it inside, this function changes input!
    def dijkstra(dist, start):
        if np.max(dist) < np.inf:  # skip
            return dist
        size = len(dist)
        current = np.copy(dist[start])
        for i in range(len(current)):
            if current[i] == np.inf:
                current[i] = size * 2  # any route must be lower than size * 2
        current[start] = np.inf
        for _ in range(size - 1):
            i = np.argmin(current)  # second lowest(lowest is itself)
            to_dis = dist[start][i]  # distance to target i
            for j in range(size):
                if dist[start][j] > to_dis + dist[i][j]:  # if shorter route, update
                    current[j] = dist[start][j] = to_dis + dist[i][j]
                    dist[j][start] = dist[start][j]
            current[i] = np.inf
        return dist

    def fit_reduce(self, data):
        data = normalize(data)  # I have to normalize to process better dij
        size = len(data)
        dist = np.zeros((size, size))
        print('Distance calculation: total = {}   '.format(size), end='')
        for i in range(size):
            for _ in range(0, len(str(i - 1))):
                print('\b', end='')
            print('.', i, sep='', end='')
            dist[i] = np.sum(np.square(data[i] - data), axis=1).T  # so written, much faster
            if not (i + 1) % 15:
                print('\b' * 15, end='')
        knn = np.ones((size, size)) * np.inf
        for i in range(size):
            selected = np.argpartition(dist[i], self.k)[:self.k + 1]  # k+1 lowest including itself
            knn[i][selected] = dist[i][selected]
        for i in range(size):  # undirected graph
            for j in range(i + 1, size):
                if knn[i][j] < np.inf:
                    knn[j][i] = knn[i][j]
                elif knn[j][i] < np.inf:
                    knn[i][j] = knn[j][i]
        print('Calculating path: total = {}   '.format(size), end='')
        for i in range(size):  # dij takes really long time, but I have no time to realize KD-tree
            for _ in range(0, len(str(i - 1))):
                print('\b', end='')
            print('.', i, sep='', end='')
            knn = self.dijkstra(knn, i)
            if np.max(knn[i]) == np.inf:
                print(
                    '\rFeedback from Isomap:\n\tWarning: unconnected graph! should raise k(current: {})'.format(self.k))
                return np.zeros((size, self.n_components))
            if not (i + 1) % 15:
                print('\b' * 15, end='')
        print('\rFeedback from Isomap:\n\tStarting MDS, please wait!')
        return MDS(n_components=self.n_components).fit_reduce(knn, _inner_mode=True)
