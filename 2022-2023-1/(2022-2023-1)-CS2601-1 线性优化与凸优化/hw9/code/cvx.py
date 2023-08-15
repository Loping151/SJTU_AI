import cvxpy as cp
import numpy as np

x = cp.Variable(3)

f = cp.exp(2*x[0]) + cp.exp(x[1]) + cp.exp(x[2])

constraints = [x[0] + x[1] + x[2] == 1]

problem = cp.Problem(cp.Minimize(f), constraints)
problem.solve()

print('optimal value:', problem.value)
print('optimal solution:', x.value)