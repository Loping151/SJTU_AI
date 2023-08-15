import cvxpy as cp
import numpy as np

A = np.array([2, 1, 1, 3, 1, 2]).reshape(3, 2)
x = cp.Variable((2, 1))
b = np.array([5, 6, -5]).reshape(3, 1)

cons = [cp.norm_inf(x) <= 1]

obj = cp.Minimize(cp.norm_inf(A @ x - b))

prob = cp.Problem(obj, cons)
prob.solve()

print("Problem(", '\bb', "\b): status:", prob.status, "\noptimal value", prob.value, "\noptimal var: x =", x.value,
      "\noptimal")

t = cp.Variable()

cons = [A[i, :] @ x - b[i, :] <= t for i in range(3)] + \
       [A[i, :] @ x - b[i, :] >= -t for i in range(3)] + \
       [x[0] <= 1, x[1] <= 1] + [x[0] >= - 1, x[1] >= - 1]
obj = cp.Minimize(t)

prob = cp.Problem(obj, cons)
prob.solve()

print("Problem(", '\bc', "\b): status:", prob.status, "\noptimal value", prob.value, "\noptimal var: x =", x.value,
      "\noptimal")
