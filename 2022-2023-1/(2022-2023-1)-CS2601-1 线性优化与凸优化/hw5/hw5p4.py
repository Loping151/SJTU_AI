import cvxpy as cp
import numpy as np

X = np.array([
    4, 1, 0, 4, 2, 0, 2, 4, 1, 1, 0, 2, 4, 4, 0, 4, 1, 4, 1, 0, 2, 3, 1, 2, 4, 4, 2, 2, 0, 1, 2, 2, 0, 1, 2, 4, 0, 1, 2,
    1, 4, 2, 0, 0, 1, 0, 1, 3]).reshape((8, 6))
y = np.array([5, 0, 5, 0, 4, 2, 5, 3]).reshape((8, 1))

print(np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y))

w = cp.Variable((6, 1))

cons = []
obj = cp.Minimize(cp.norm2(X @ w - y) ** 2)
prob = cp.Problem(obj, cons)
prob.solve()
print("Problem(", '\ba', "\b): status:", prob.status, "\noptimal value", prob.value, "\noptimal var: w =", w.value,
      "\no1ptimal")

cons = [cp.norm1(w) <= 1]
obj = cp.Minimize(cp.norm2(X @ w - y) ** 2)
prob = cp.Problem(obj, cons)
prob.solve()
print("Problem(", '\bb', "\b) when t = 1: status:", prob.status, "\noptimal value", prob.value, "\noptimal var: w =",
      w.value,
      "\noptimal")

cons = [cp.norm1(w) <= 10]
obj = cp.Minimize(cp.norm2(X @ w - y) ** 2)
prob = cp.Problem(obj, cons)
prob.solve()
print("Problem(", '\bb', "\b) when t = 10: status:", prob.status, "\noptimal value", prob.value, "\noptimal var: w =",
      w.value,
      "\noptimal")

cons = [cp.norm2(w) <= 1]
obj = cp.Minimize(cp.norm2(X @ w - y) ** 2)
prob = cp.Problem(obj, cons)
prob.solve()
print("Problem(", '\bc', "\b) when t = 1: status:", prob.status, "\noptimal value", prob.value, "\noptimal var: w =",
      w.value,
      "\noptimal")

cons = [cp.norm2(w) <= 100]
obj = cp.Minimize(cp.norm2(X @ w - y) ** 2)
prob = cp.Problem(obj, cons)
prob.solve()
print("Problem(", '\bc', "\b) when t = 100: status:", prob.status, "\noptimal value", prob.value, "\noptimal var: w =",
      w.value,
      "\noptimal")
