import cvxpy as cp
import numpy as np

x1 = cp.Variable()
x2 = cp.Variable()

cons = [x1 + 2 * x2 >= 1,
        3 * x1 + x2 >= 1,
        x1 >= 0, x2 >= 0]

f1 = cp.Minimize(x1 + x2)
f2 = cp.Minimize(-x1 - x2)
f3 = cp.Minimize(x1)
f4 = cp.Minimize(cp.maximum(x1, x2))
f5 = cp.Minimize(x1 ** 2 + 9 * x2 ** 2)


def solve(name, f):
    prob = cp.Problem(f, cons)
    prob.solve()
    print("Problem(", name, "\b): status:", prob.status, "\noptimal value", prob.value, "\noptimal var: x1 =", x1.value,
          'x2 =', x2.value)


solve('\ba', f1)
solve('\bb', f2)
solve('\bc', f3)
solve('\bd', f4)
solve('\be', f5)
