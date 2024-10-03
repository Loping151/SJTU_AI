# ~/anaconda3/env/yourEnvName python3.9
# _*_ coding:utf-8 _*_
#
# @Version : 1.0
# @Time    : 2022.8.7
# @Author  : Kailing Wang
# @File    : user_example.py
#
# DTMC userExample

from DTMC import DTMC
import numpy as np
from random import shuffle

# 模型使用方法简介


def sampleDTMC():
    mc = DTMC(4)

    mc.predict()
    print('\n')

    trans = [[0, 0.1, 0.4, 0.5], [0.3, 0, 0, 0.7],
             [0, 0, 0, 1], [0, 0.4, 0.6, 0]]
    mc.fit(trans)
    mc.predict()
    print('\n')

    mc.reset_state([0.1, 0.2, 0.3, 0.4])
    mc.fit(trans)
    mc.predict()
    print('\n')

    mc.eps = 1e-10
    mc.fit(trans)
    mc.predict()
    print('\n')

    mc.state_names = ['sunny', 'rainy', 'foggy', 'cloudy']
    mc.predict(2)
    print('\n')

    mc.eps = -1  # not allow break
    mc.fit(trans)
    mc.predict()
    print('\n')

    mc.eps = 0.001
    mc.max_iter = 10
    mc.fit(trans)
    mc.predict()
    print('\n')


# 下方函数给出了预测未来大学生毕业去向的样例


def predict_graduate():
    model = DTMC(3, eps=0.1)  # 建立模型
    graduate_data = [[0.85, 0.12, 0.03],
                     [0.02, 0.95, 0.03],
                     [0.01, 0.32, 0.67]]
    graduate_data = np.array(graduate_data)
    model.state_names = ['就业', '升学', '留学']
    model.fit(graduate_data)
    model.predict()
    model.eps = 0.001
    model.fit(graduate_data)
    model.predict()
    model.eps = -1
    model.max_iter = 30000
    model.fit(graduate_data)
    model.predict()


predict_graduate()
