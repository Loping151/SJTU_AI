import numpy as np


def newton_eq(f, fp, fpp, x0, A, b, initial_stepsize=1.0, alpha=0.5, beta=0.5, tol=1e-8, maxiter=100000):
    """
    f: function that takes an input x an returns the value of f at x
    fp: function that takes an input x and returns the gradient of f at x
    fpp: function that takes an input x and returns the Hessian of f at x
    A, b: constraint A x = b
    x0: initial feasible point
    initial_stepsize: initial stepsize used in backtracking line search
    alpha: parameter in Armijo's rule
                f(x + t * d) > f(x) + t * alpha * f(x) @ d
    beta: constant factor used in stepsize reduction
    tol: toleracne parameter in the stopping crieterion. Gradient descent stops
         when the 2-norm of the Newton direction is smaller than tol
    maxiter: maximum number of iterations in outer loop of damped Newton's method.

    This function should return a list of the iterates x_k
    """
    x_traces = [np.array(x0)]

    m = len(b)
    x = np.array(x0)

    for it in range(maxiter):
        #   START OF YOUR CODE

        # Compute Newton direction
        tmpH = fpp(x)
        H = np.zeros((tmpH.shape[0] + A.shape[0], tmpH.shape[1] + A.shape[0]))
        H[:tmpH.shape[0], :tmpH.shape[1]] = tmpH
        H[-1, :-1] = A
        H[:-1, -1] = A.T.reshape((tmpH.shape[1],))

        tmpg = fp(x)
        g = np.zeros((len(tmpg) + A.shape[0], 1))
        g[:-1] = tmpg.reshape((len(tmpg), 1))
        g[-1] = 0
        d = -np.linalg.solve(H, g)[:-1]
        d = d.reshape((3,))
        # print(d.shape)

        # Test for convergence
        if np.linalg.norm(d) < tol:
            break

        # Perform backtracking line search to find a suitable stepsize
        stepsize = initial_stepsize
        while True:
            x_new = x + stepsize * d
            if f(x_new) <= f(x) + stepsize * alpha * tmpg @ d:
                break
            stepsize *= beta
        x = x_new
        x_traces.append(x)

    #	END OF YOUR CODE

    return x_traces
