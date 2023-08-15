import numpy as np
import gd
import utils

gamma = 0.001
Q = np.diag([gamma, 1])


def f(x):
    return 0.5 * x.T @ Q @ x


def fp(x):
    return Q @ x


def f_2d(x1, x2):
    return 0.5 * gamma * x1 ** 2 + 0.5 * x2 ** 2


x0 = np.array([1.0, 1.0])

stepsize = 1

x_traces = gd.gd_const_ss(fp, x0, stepsize=stepsize)

print(f'gamma={gamma}, stepsize={stepsize}, number of iterations={len(x_traces) - 1}')

utils.plot_traces_2d(f_2d, x_traces, f'../figures/gd_traces_gamma{gamma}_ss{stepsize}.png')
utils.plot(f, x_traces, f'../figures/gd_f_gamma{gamma}_ss{stepsize}.png')
