import numpy as np
import matplotlib.pyplot as plt


# 函数
def f_1(x):
    return np.exp(x ** 2)


# 积分区间
def xr(n=1e6, l=-3, h=3):
    return np.arange(l, h, 6 / n)


# plt.figure()
# plt.plot(xr(), f_1(xr()))
# plt.xlabel('x')
# plt.ylabel('f(x)')
# plt.show()


# 数值积分
def numer_int(f, a, b, dx=1e-6):
    res = 0
    for i in range(int((b - a) / dx)):
        res = res + f(a + i * dx) * dx
    return res


# 样本产生
def cdf(pdf, x, dx=1e-6):
    x = sorted(x)
    head = 0
    res = []
    c = 0.5 - numer_int(pdf, -3, 0)
    while head < len(x) and x[head] <= c:
        head = head + 1
    for i in range(int(6 / dx)):
        c = c + pdf(-3 + i * dx) * dx
        while head < len(x) and x[head] <= c:
            head = head + 1
            res.append(-3 + i * dx)
    return res


def f_u(x):
    if -3 <= x <= 3:
        return 1 / 6
    else:
        return 0


def f_n(x):
    return np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi)


def f_0(x):
    if -3 <= x < -2.5 or -2 <= x < -1.5 or -1 <= x < -0.5 or 0 <= x < 0.5 or 1 <= x < 1.5 or 2 <= x < 2.5:
        return 1 / 3
    else:
        return 0


f_sint = numer_int(lambda l: abs(np.sin(1 / l)), -3, 0 - 1e-6) * 2


def f_s(x):
    if x != 0 and -3 <= x <= 3:
        return abs(np.sin(1 / x)) / f_sint
    else:
        return 0


# plt.figure()
# _, bins, _ = plt.hist(cdf(f_n, np.random.random(100000)), bins=75, density=1)
# plt.plot(bins, f_n(bins), 'r--')
# plt.show()


def MC_int(f, pdf, n):
    us = np.random.random(int(n * 1.2))
    ns = cdf(pdf, us)
    np.random.shuffle(ns)
    ns = ns[:n]
    res = 0
    for i in range(n):
        res = res + f(ns[i]) / pdf(ns[i])
    return res / n


# fu = []
# fn = []
# f0 = []
# fs = []
# iters = ["10", "100", "1000", "10000", "100000", "1000000", "5000000", "10000000"]
# for n in [10, 100, 1000, 10000, 100000, 1000000, 5000000, 10000000]:
#     print(n)
#     fu.append(MC_int(f_1, f_u, n)), print("f_u", fu[-1])
#     fn.append(MC_int(f_1, f_n, n)), print("f_n", fn[-1])
#     f0.append(MC_int(f_1, f_0, n)), print("f_0", f0[-1])
#     fs.append(MC_int(f_1, f_s, n)), print("f_s", fs[-1])
#
# realint = numer_int(f_1, -3, 3)
# plt.figure()
# plt.plot(iters, fu, marker='o', markersize=3)
# plt.plot(iters, fn, marker='o', markersize=3)
# plt.plot(iters, f0, marker='o', markersize=3)
# plt.plot(iters, fs, marker='o', markersize=3)
# plt.plot(iters, realint * np.ones((len(fu),)), marker='o', markersize=3)
# plt.legend(['f_u', 'f_n', 'f_0', 'f_s', 'I(f)'])
# plt.show()
#
# print(fu, np.array(fu) - realint)
# print(fn, np.array(fn) - realint)
# print(f0, np.array(f0) - realint)
# print(fs, np.array(fs) - realint)

def cdf2(pdf, x, dx=1e-4):
    x = sorted(x)
    head = 0
    res = []
    c = 0.5 - numer_int(pdf, -10, 0)
    while head < len(x) and x[head] <= c:
        head = head + 1
    for i in range(int(20 / dx)):
        c = c + pdf(-10 + i * dx) * dx
        while head < len(x) and x[head] <= c:
            head = head + 1
            res.append(-10 + i * dx)
    return res

def pi(n=100000):
    nsx = cdf2(f_n, np.random.random(int(n * 1.2)))
    nsy = cdf2(f_n, np.random.random(int(n * 1.2)))
    np.random.shuffle(nsx)
    nsx = nsx[:n]
    np.random.shuffle(nsy)
    nsy = nsy[:n]
    res = 0
    inner = []
    outer = []
    for i in range(n):
        if nsx[i] ** 2 + nsy[i] ** 2 <= 1:
            inner.append([nsx[i], nsy[i]])
            res = res + 1 / f_n(nsx[i]) / f_n(nsy[i])
        else:
            outer.append([nsx[i], nsy[i]])
    plt.figure(figsize=(5,5))
    inner = np.array(inner)
    outer = np.array(outer)
    plt.scatter(inner[:, 0], inner[:, 1])
    plt.scatter(outer[:, 0], outer[:, 1])
    plt.title("n={}, pi={}".format(n, res / n))
    plt.show()
    return res / n


for n in [1000, 10000, 100000, 1000000]:
    print(n, pi(n))
