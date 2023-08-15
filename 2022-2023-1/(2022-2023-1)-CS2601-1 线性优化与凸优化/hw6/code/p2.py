import numpy as np
import gd
import utils

X = (4, 1, 0, 4, 2, 0,
     2, 4, 1, 1, 0, 2,
     4, 4, 0, 4, 1, 4,
     1, 0, 2, 3, 1, 2,
     4, 4, 2, 2, 0, 1,
     2, 2, 0, 1, 2, 4,
     0, 1, 2, 1, 4, 2,
     0, 0, 1, 0, 1, 3)
X = np.array(X).reshape(8, 6)
y = [5, 0, 5, 0, 4, 2, 5, 3]
y = np.array(y).reshape(-1, 1)

omega = np.linalg.solve(X.T.dot(X), X.T.dot(y))
print(omega)


def f(w):
    return np.linalg.norm(X.dot(w) - y)


def fp(w):
    return 2 * (X.T.dot(X.dot(w) - y))


stp = 0.001
w0 = np.array([0] * 6).reshape(-1, 1)
x_traces = gd.gd_const_ss(fp, w0, stepsize=stp)
print(f'stepsize={stp}, number of iterations={len(x_traces) - 1}')
# utils.plot_traces_2d(f_2d, x_traces, f'../figures/p2_ss{stp}.png')
utils.plot(f, x_traces, f'../figures/p2_ss{stp}.png')
print(x_traces[-1])
