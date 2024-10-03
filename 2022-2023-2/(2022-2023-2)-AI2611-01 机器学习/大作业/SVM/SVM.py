import numpy as np
from typing import Union, Callable
from cuda_acc import cpu, cp
from utils import data_shuffle, batchify, label_wash, data_filter, time_str
import pickle
from animation import rolling_ball, spinning_stick
import time


def error_loss(w, b, x, y, lib, kernel):
    svm_output = kernel(x, w) + b
    error = lib.abs(svm_output - y)
    return lib.sum(error)


def hinge_loss(w, b, x, y, lib, kernel):
    out = kernel(x, w) + b
    loss = 1 - y * out
    loss = (loss + lib.abs(loss)) / 2  # max(0, 1-y*out)
    return lib.mean(loss)


dict_loss = {'error_loss': error_loss, 'hinge_loss': hinge_loss}


def kernel_rbf(A, B, gamma, lib):  # also called gaussian function
    diff = A - B.T
    dist_sq = lib.sum(diff ** 2, axis=1)
    K = lib.exp(-gamma * dist_sq)
    return 10 * K[:, lib.newaxis]


def kernel_gaussian(A, B, sigma, lib):
    return kernel_rbf(A, B, -0.5 / sigma ** 2, lib) / sigma / lib.sqrt(lib.pi * 2)


def kernel_linear(A, B):
    return A.dot(B)


def kernel_poly(A, B, c, d):
    return (A.dot(B) + c) ** d


dict_kernel = {'rbf': kernel_rbf, 'gaussian': kernel_gaussian, 'linear': kernel_linear, 'poly': kernel_poly}


def kernels(A, B, idx, args):
    return list(dict_kernel.values())[idx](A, B, *args)


def fprintf(silence, msg):
    if not silence:
        print(msg)


class SVMbase:
    def __init__(self, dev):
        self.lib = np if dev is cpu else cp  # use numpy if you use cpu else use cupy
        self.kernel = None

    def kernel_gradient(self, A, B, func, args, lib):
        if func[1] is kernel_linear:
            return A / (lib.linalg.norm(A) + 1)
        if func[1] is kernel_rbf or func[1] is kernel_gaussian:
            grad = func[0](A, B) * (A - B.T) * 2 * args[0]
            return grad / (lib.linalg.norm(grad) + 1)
        if func[1] is kernel_poly:
            c, d = args
            grad = d * (A.dot(B) + c) ** (d - 1) * A
            return grad / (lib.linalg.norm(grad) + 1)
        raise NotImplementedError

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['lib']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def save(self, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load(filename: str):
        with open(filename, 'rb') as file:
            return pickle.load(file)


class SVM151(SVMbase):  # 151 is my identity code
    def __init__(self, dev,  # the current device
                 C=1.0,  # In sklearn_tests.ipynb I showed that we'd better set a default C
                 inner=False
                 ):
        super(SVM151, self).__init__(dev)
        self.C = C
        self.w = None  # I name my variavble the same as what I write in my report
        self.b = None
        self.inner = inner  # whether the SVM is wrapped inside SVC

    def __getstate__(self):
        state = self.__dict__.copy()
        paras = ['w', 'b']
        state = {k: state[k] for k in paras if k in state.keys()}
        return state

    def fit(self,
            X,
            y,
            cache_size: int = 1024,  # batch size, but sklearn call it cache size
            epochs: int = 1000,  # or max_iter, but I may have no time to consider stopping conditon
            step_lambda: float = 0.01,  # or learning rate lambda, to normalize lr
            kernel: str = 'linear',  # rbf, gaussian, linear, poly
            kernel_args=None,  # touple of your kernel arguments
            loss_fun: Union[
                'error_loss', 'hinge_loss', Callable] = 'error_loss'  # will make no difference to optimizing, legacy!
            ):
        assert len(X.shape) == 2 and len(y.shape) == 2
        assert X.shape[0] == y.shape[0]

        feature_dim = X.shape[1]
        dict_args = {'rbf': (0.001, self.lib),
                     'gaussian': (1, self.lib),
                     'linear': (),
                     'poly': (1, 3)}
        if loss_fun in dict_loss.keys():
            loss_fun = dict_loss[loss_fun]
        else:
            raise NotImplementedError
        if kernel in dict_kernel.keys():
            if kernel_args is None:
                kernel_args = dict_args[kernel]
            kernel = dict_kernel[kernel]
        else:
            raise NotImplementedError

        def inner_kernel(A, B):
            return kernel(A, B, *kernel_args)

        self.kernel = inner_kernel

        C = self.C
        w = self.lib.zeros((feature_dim, 1))
        b = self.lib.array(0)
        losses = []

        X, y = data_shuffle(X, y, self.lib)
        y = label_wash(y, self.lib)
        X, y = batchify(X, y, cache_size, self.lib)
        start_time = time.time()
        for _iter in range(epochs):
            for data, label in zip(X, y):
                losses.append(loss_fun(w, b, data, label, self.lib, self.kernel))
                time_diff = time.time() - start_time
                rolling_ball(7, 0,
                             f"[{time_str(time_diff)}<{time_str(time_diff * (epochs - _iter - 1) / (_iter + 1))}]Epoch [{_iter + 1}/{epochs}], Loss: {losses[-1]:.4f} ")
                margin = (self.kernel(data, w) + b) * label
                mask = margin < 1
                g_w = -C * self.lib.sum(
                    self.kernel_gradient(data, w, (self.kernel, kernel), kernel_args, self.lib) * label * mask,
                    axis=0)[:, self.lib.newaxis] + self.kernel_gradient(w.T, w, (self.kernel, kernel), kernel_args,
                                                                        self.lib).T
                g_b = -C * self.lib.sum(label * mask)
                eta = 1 / step_lambda / (_iter + 1)
                w = (1 - 1 / (_iter + 1)) * w - eta * g_w / cache_size
                b = b - eta * g_b / cache_size
                w = min(1, 1 / (self.lib.sqrt(step_lambda) * self.lib.linalg.norm(w))) * w
        if not self.inner:
            print()
        self.b = b
        self.w = w
        return losses

    def predict(self, X):
        return self.kernel(X, self.w) + self.b

    def test(self, X, y, cache_size=512):
        total = len(X)
        y = label_wash(y, self.lib)
        X, y = batchify(X, y, cache_size, self.lib)
        test_acc = 0
        for data, label in zip(X, y):
            out = self.predict(data)
            predictions = self.lib.sign(out)
            test_acc += self.lib.sum(predictions.flatten() == label.flatten())
        return test_acc / total


class MKLSVM151(SVMbase):
    def __init__(self, dev,  # the current device
                 C=1.0,  # In sklearn_tests.ipynb I showed that we'd better set a default C
                 inner=False
                 ):
        super(MKLSVM151, self).__init__(dev)
        self.C = C
        self.w = None  # I name my variavble the same as what I write in my report
        self.b = None
        self.theta = None
        self.inner = inner  # whether the SVM is wrapped inside SVC
        self.dict_args = None

        self.kernel_weights = [0, 0, 2, 2]
        self.optimize = False  # used in debug mode

    def multi_kernel(self, A, B, args):
        mk = []
        for _i in range(len(dict_kernel)):
            if self.kernel_weights[_i] == 0:
                mk.append(self.lib.zeros((A.shape[0], 1)))
            else:
                mk.append(kernels(A, B, _i, list(args.values())[_i]) * self.kernel_weights[_i])
        return self.lib.array(mk)

    def multi_gradient(self, data, w, kernel_args):
        mg = []
        args = list(kernel_args.values())
        for _i in range(len(dict_kernel)):
            if self.kernel_weights[_i] == 0:
                mg.append(self.lib.zeros(data.shape))
            else:
                mg.append(
                    self.kernel_gradient(data, w,
                                         (lambda A, B: kernels(A, B, _i, args[_i]), list(dict_kernel.values())[_i]),
                                         args[_i], self.lib) * self.kernel_weights[_i])
        return self.lib.sum(self.lib.array(mg), axis=0)

    def __getstate__(self):
        state = self.__dict__.copy()
        paras = ['w', 'b', 'theta']
        state = {k: state[k] for k in paras if k in state.keys()}
        return state

    def fit(self,
            X,
            y,
            cache_size: int = 1024,  # batch size, but sklearn call it cache size
            epochs: int = 1000,  # or max_iter, but I may have no time to consider stopping conditon
            step_lambda: float = 0.01,  # or learning rate lambda, to normalize lr
            kernel_args: dict = None,  # touple of your kernel arguments
            ):
        assert len(X.shape) == 2 and len(y.shape) == 2
        assert X.shape[0] == y.shape[0]

        feature_dim = X.shape[1]
        dict_args = {'rbf': (0.001, self.lib),
                     'gaussian': (1, self.lib),
                     'linear': (),
                     'poly': (1, 3)}
        if kernel_args is not None:
            for k, v in zip(kernel_args.keys(), kernel_args.values()):
                dict_args[k] = v
        self.dict_args = dict_args

        C = self.C
        w = self.lib.zeros((feature_dim, 1))
        b = self.lib.array(0)
        theta = self.lib.ones((len(dict_kernel), 1)) / len(dict_kernel)

        X, y = data_shuffle(X, y, self.lib)
        y = label_wash(y, self.lib)
        X, y = batchify(X, y, cache_size, self.lib)
        start_time = time.time()
        for _iter in range(epochs):
            for data, label in zip(X, y):
                time_diff = time.time() - start_time
                rolling_ball(7, 0,
                             f"[{time_str(time_diff)}<{time_str(time_diff * (epochs - _iter - 1) / (_iter + 1))}]Epoch [{_iter + 1}/{epochs}]")
                mk = self.multi_kernel(data, w, dict_args)
                mk_theta = mk * theta[:, self.lib.newaxis, :]
                margin = (self.lib.sum(mk_theta, axis=0) + b) * label
                mask = margin < 1
                g_w = -C * self.lib.sum(
                    self.multi_gradient(data, w, dict_args) * label * mask,
                    axis=0) + self.lib.sum(self.multi_gradient(w.T, w, dict_args), axis=0).T
                g_w = g_w[:, self.lib.newaxis]
                g_b = -C * self.lib.sum(label * mask)
                g_theta = -C * self.lib.sum(mk * label * mask, axis=1)
                g_theta = 100 * g_theta / (self.lib.linalg.norm(g_theta) + 100)
                eta = 1 / step_lambda / (_iter + 1)
                w = (1 - 1 / (_iter + 1)) * w - eta * g_w / cache_size
                b = b - eta * g_b / cache_size
                if self.optimize:
                    theta = theta - eta * g_theta / cache_size
                theta = theta / self.lib.sum(theta)
                w = min(1, 1 / (self.lib.sqrt(step_lambda) * self.lib.linalg.norm(w))) * w
        if not self.inner:
            print()
        self.b = b
        self.w = w
        self.theta = theta

    def predict(self, X):
        return self.lib.sum(
            self.multi_kernel(X, self.w, self.dict_args) * self.theta[:, self.lib.newaxis, :],
            axis=0) + self.b

    def test(self, X, y, cache_size=512):
        total = len(X)
        y = label_wash(y, self.lib)
        X, y = batchify(X, y, cache_size, self.lib)
        test_acc = 0
        for data, label in zip(X, y):
            out = self.predict(data)
            predictions = self.lib.sign(out)
            test_acc += self.lib.sum(predictions.flatten() == label.flatten())
        return test_acc / total


class SVC151(SVMbase):
    def __init__(self, dev,
                 multi_kernel=False,
                 C=1.0,
                 num_classes=10,
                 mode: Union[int, str] = 'one_to_rest'
                 ):
        super(SVC151, self).__init__(dev)
        allowed = ['one_to_rest', 'one_to_one']
        assert mode in allowed or mode in [0, 1]
        if type(mode) is str:
            mode = 0 if mode == 'one_to_rest' else 1
        self.multi_kernel = multi_kernel
        self.num_classes = num_classes
        if not multi_kernel:
            self.SVM = [SVM151(dev, C=C, inner=True) for _ in
                        range(num_classes if mode == 0 else (num_classes - 1) * (num_classes - 2))]
        else:
            self.SVM = [MKLSVM151(dev, C=C, inner=True) for _ in
                        range(num_classes if mode == 0 else (num_classes - 1) * (num_classes - 2))]
        self.lib = np if dev is cpu else cp
        self.mode = mode

    def __setstate__(self, state):
        pass

    def fit(self,
            X,
            y,
            cache_size: int = 1024,  # batch size, but sklearn call it cache size
            epochs: int = 1000,  # or max_iter, but I may have no time to consider stopping conditon
            step_lambda: float = 0.01,  # or learning rate lambda, to normalize lr
            kernel: str = 'linear',  # rbf, gaussian, linear, poly
            kernel_args=None,  # touple of your kernel arguments
            loss_fun: Union[
                'error_loss', 'hinge_loss', Callable] = 'error_loss',  # will make no difference to optimizing, legacy!
            silence: bool = True
            ):
        args = None
        if self.multi_kernel:
            args = (cache_size, epochs, step_lambda, kernel_args)
        else:
            args = (cache_size, epochs, step_lambda, kernel, kernel_args, loss_fun)

        def _fit_one_to_rest():
            n_losses = []
            for n_c in range(self.num_classes):
                fprintf(silence, ("Class", n_c))
                n_losses.append(self.SVM[n_c].fit(*data_filter(X, y, self.lib, filter=[n_c]), *args))
                fprintf(silence, '')
            return n_losses

        def _fit_one_to_one():
            n_losses = []
            p_s = 0
            for c1 in range(self.num_classes - 1):
                for c2 in range(c1 + 1, self.num_classes - 1):
                    fprintf(silence, f'c1: {c1}, c2: {c2}')
                    n_losses.append(self.SVM[p_s].fit(*data_filter(X, y, self.lib, filter=[c1, c2]), *args))
                    p_s += 1
                    fprintf(silence, '')
            return n_losses

        t = time.time()
        _fit = [_fit_one_to_rest, _fit_one_to_one]
        return _fit[self.mode](), time.time() - t

    def predict(self, X):
        def _predict_one_to_rest():
            out = self.lib.array([self.SVM[i].predict(X) for i in range(self.num_classes)])
            out = out.reshape(out.shape[:-1])
            return self.lib.argmax(out, axis=0)

        def _predict_one_to_one():
            assert len(X.shape) == 2
            out = self.lib.zeros((X.shape[0], self.num_classes))
            p_s = 0
            for c1 in range(self.num_classes - 1):
                for c2 in range(c1 + 1, self.num_classes - 1):
                    pred = self.SVM[p_s].predict(X)
                    out[:, c1] += self.lib.where(pred < 0, 1, 0).flatten()
                    out[:, c2] += self.lib.where(pred > 0, 1, 0).flatten()
                    p_s += 1
            return self.lib.argmax(out, axis=1)

        _predict = [_predict_one_to_rest, _predict_one_to_one]
        return _predict[self.mode]()

    def test(self, X, y, cache_size=512):
        total = len(X)
        X, y = batchify(X, y, cache_size, self.lib)
        test_acc = 0
        for data, label in zip(X, y):
            prediction = self.predict(data)
            test_acc += self.lib.sum(prediction.flatten() == label.flatten())
        return test_acc / total
