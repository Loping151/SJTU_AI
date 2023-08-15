import numpy as np
import gd
import utils
import matplotlib.pyplot as plt

# X: m x 2 matrix, X[i,:] is the 2D feature vector of the i-th sample
X = np.array([[3, 1.5],
              [3.2, 2.5],
              [3, 3.5],
              [2, 2.25],
              [3.8, 3],
              [1.5, 4],
              [1, 1.9],
              [4.5, .5],
              [3.5, .8],
              [3.8, .3],
              [4.2, .3],
              [1, .8],
              [3.8, 1],
              [4, 2],
              [5.8, 1.8]])
# y: m-D vector, y[i] is the label of the i-th sample
y = np.append(np.ones((7,)), -np.ones((8,)))

# append a constant 1 to each feature vector, so X is now a m x 3 matrix
X = np.append(X, np.ones((15, 1)), axis=1)

# Xy[i,:] = X[i,:] * y[i]
Xy = X * y.reshape((-1, 1))

# X.shape = (15,3), Xy.shape = (15, 3), y.shape = (15,)
print(X.shape, Xy.shape, y.shape)


# sigmoid function
def sigmoid(z):
    #   START OF YOUR CODE
    if type(z) == 'numpy.ndarray':
        return np.array([1 / (1 + np.exp(-i)) for i in z])
    else:
        # print(z)
        # print(1 / (1 + np.exp(-z)))
        return 1 / (1 + np.exp(-z))


#   END OF YOUR CODE

def fp(w):
    # START OF YOUR CODE
    sum = 0
    for i in range(len(y)):
        tmp = y[i] * X[i].T.dot(w)
        sum = sum - y[i] * X[i].T * (1 - sigmoid(tmp))
    return sum


#   END OF YOUR CODE

# minimize f by gradient descent
#   START OF YOUR CODE
w_traces = gd.gd_const_ss(fp, [1, 1, 1], stepsize=0.01)

print(f'number of iterations={len(w_traces) - 1}')
#   END OF YOUR CODE

# compute the accuracy on the training set
w = w_traces[-1]
y_hat = 2 * (X @ w > 0) - 1

accuracy = sum(y_hat == y) / float(len(y))
print(f"accuracy = {accuracy}")

# visualization
plt.figure(figsize=(4, 4))

plt.scatter(*zip(*X[y > 0, 0:2]), c='r', marker='x')
plt.scatter(*zip(*X[y < 0, 0:2]), c='g', marker='o')

# plot the decision boundary w[0] * x1 + w[1] * x2 + w[0] = 0
x1 = np.array([min(X[:, 0]), max(X[:, 0])])
x2 = -(w[0] * x1 + w[2]) / w[1]
plt.plot(x1, x2, 'b-')

plt.xlabel('x1')
plt.ylabel('x2')

plt.tight_layout()
plt.show()
plt.savefig('../figures/p3.png')
