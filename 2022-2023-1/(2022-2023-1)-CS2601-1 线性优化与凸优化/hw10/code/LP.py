import newton as nt
import numpy as np


def centering_step(c, A, b, x0, t):
    """
    c, A, b: parameters in LP

            min   c^T x
            s.t.  Ax = b
                  x >= 0

    x0: feasible initial point for constrained Newton's method
    t:  penalty parameter in barrier method

    This function returns the central point x^*(t) 
    """

    #   START OF YOUR CODE

    def f(x):
        return c.T @ x - np.sum(np.log(x)) / t

    def fp(x):
        return c.T - 1 / x / t

    def fpp(x):
        return 1 / t * np.diag(1 / x / x)

    x_star = nt.newton_eq(f, fp, fpp, x0, A, b, maxiter=100)[-1]

    return x_star

    #	END OF YOUR CODE


def barrier(c, A, b, x0, tol=1e-8, t0=1, rho=10):
    """
    c, A, b: parameters in LP

            min   c^T x
            s.t.  Ax = b
                  x >= 0

    x0:  feasible initial point for the barrier method
    tol: tolerance parameter for the suboptimality gap. The algorithm stops when

             f(x) - f^* <= tol

    t0:  initial penalty parameter in barrier method
    rho: factor by which the penalty parameter is increased in each centering step

    This function should return a list of the iterates
    """
    t = t0
    x = np.array(x0)
    x_traces = [np.array(x0)]

    #   START OF YOUR CODE

    while True:
        x_star = centering_step(c, A, b, x, t)
        if t >= len(x0) / tol:
            break
        x = x_star
        t *= rho
        x_traces.append(x)

    #	END OF YOUR CODE

    return x_traces
