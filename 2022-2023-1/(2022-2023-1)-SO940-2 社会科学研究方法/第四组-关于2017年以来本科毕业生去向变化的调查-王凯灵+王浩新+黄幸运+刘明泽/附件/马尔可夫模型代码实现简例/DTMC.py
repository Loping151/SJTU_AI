# ~/anaconda3/env/yourEnvName python3.9
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2022.8.7
# @Author  : Kailing Wang
# @File    : DTMC.py
#
# Markov Chain

from numpy import zeros, sum, array, ones


class DTMC:
    def __init__(self, size, state_names=None, init_state=None, eps=0.001, max_iter=1e5):
        if state_names is not None:
            self.state_names = state_names
        else:
            self.state_names = []
            for _ in range(size):
                self.state_names.append('state_' + str(_))
        self.size = size
        if init_state is not None:
            self.p_i = array(init_state)
        else:
            self.p_i = ones((1, self.size)) / size
        self.trans = zeros((self.size, self.size))
        self.max_iter = max_iter
        self.eps = eps
        self.result = None

    def reset_state(self, s):
        self.p_i = array(s).reshape((1, self.size))

    def fit(self, trans):
        trans = array(trans)
        res = self.p_i.copy()
        for _ in range(int(self.max_iter)):
            print('\riter', _, end='')
            rec = res.copy()
            res = res.dot(trans)
            if sum(abs(res - rec)) < self.eps:
                print('\rDTMC: Converge after', _, 'iteration(s).')
                break
            if _ == self.max_iter - 1:
                if self.eps > 0:
                    print('\rWarning: Did not converge! Epsilon too small or max_iter not enough. Final change:', sum(abs(res - rec)))
                else:
                    print('\rYou\'ve disabled Epsilon. Final change:', sum(abs(res - rec)))
        self.result = res

    def predict(self, index=None):
        if self.result is None:
            print('Fit the model first.')
            return
        if index is not None:
            if index >= self.size:
                raise IndexError
            print('\rDTMC: predict', self.state_names[index], 100 * self.result[0, index], '%')
            return self.result[0, index]
        else:
            print('\rDTMC:\n', '\b' + self.state_names[0], 100 * self.result[0, 0], '%')
            for _ in range(1, self.size):
                print(self.state_names[_], 100 * self.result[0, _], '%')
            return self.result
