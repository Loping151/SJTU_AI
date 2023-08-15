import cvxpy as cp

# Define the optimization variables
x1 = cp.Variable()
x2 = cp.Variable()

# Define the objective function
objective = -3*x1 - x2

# Define the constraints
constraints = [x1 + 2*x2 <= 8, x1 - x2 <= 3, x1 >= 0, x2 >= 0]

# Define the optimization problem
problem = cp.Problem(cp.Minimize(objective), constraints)

# Solve the optimization problem
problem.solve()

# Print the optimal solution
print(f"Optimal solution: x1 = {x1.value}, x2 = {x2.value}")
print(f"Optimal objective value: {problem.value}")