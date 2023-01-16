# coding utf-8 by Kailing Wang
# if you ask why not matlab: I forgot it
from numpy import *


# 常数表
G = 6.67384e-11
Ms = 1.98855e30
Me = 5.9722e24
Mm = 7.3477e22
D = 1.496e11
d = 3.84401e8
Re = 6.371e6
r = 4.672e6


# 旋转周期
omiga = sqrt(G*Mm/d**2/r)
# print("omiga = {:.4} s^-1".format(omiga))
# omiga = 2.665e-06


# 重要角度正弦余弦
def sinalpha(theta):
    return Re*sin(theta)/sqrt(Re**2+r**2-2*Re*r*cos(theta))


def cosalpha(theta):
    return (Re*cos(theta)-r)/sqrt(Re**2+r**2-2*Re*r*cos(theta))


def sinbeta(theta):
    return Re*sin(theta)/sqrt(Re**2+d**2-2*Re*d*cos(theta))


def cosbeta(theta):
    return (d-Re*cos(theta))/sqrt(Re**2+d**2-2*Re*d*cos(theta))


# 我的惯性力
def myFine(m, theta):
    return m*omiga**2*sqrt(Re**2+r**2-2*Re*r*cos(theta))


# 我的潮汐力(月引力)
def myFgra(m, theta):
    return G*Mm*m/(Re**2+d**2-2*Re*d*cos(theta))


# 我的引潮力表达式
def myF(m, theta):
    Fx = myFine(m, theta)*cosalpha(theta) + myFgra(m, theta)*cosbeta(theta)
    Fy = myFine(m, theta)*sinalpha(theta) - myFgra(m, theta)*sinbeta(theta)
    return Fx, Fy


# 方法一
def method1(m, theta):
    Fx = m*omiga**2*Re*cos(theta) + myFgra(m, theta)*cosbeta(theta)
    Fy = m*omiga**2*Re*sin(theta) + myFgra(m, theta)*sinbeta(theta)
    return Fx, Fy


# 方法二
def method2(m, theta):
    Fx = 2*G*Mm*m*Re*cos(theta)/d**3
    Fy = G*Mm*m*Re*sin(theta)/d**3
    return Fx, Fy


p = []  # Mass, theta of point. Example:[2(kg), pi/2(rad)]


# 计算并显示三个方法的合力与方向分力
def calculate():
    print("\tmass = {} kg, theta = {} pi rad".format(p[0], p[1]/pi))
    myFx, myFy = myF(p[0], p[1])
    print("\tmyF = {:.4} N, myFx = {:.4} N, myFy = {:.4} N".format(
        sqrt(myFx**2+myFy**2), myFx, myFy))
    m1Fx, m1Fy = method1(p[0], p[1])
    print("\tm1F = {:.4} N, m1Fx = {:.4} N, m1Fy = {:.4} N".format(
        sqrt(m1Fx**2+m1Fy**2), m1Fx, m1Fy))
    m2Fx, m2Fy = method2(p[0], p[1])
    print("\tm2F = {:.4} N, m2Fx = {:.4} N, m2Fy = {:.4} N".format(
        sqrt(m2Fx**2+m2Fy**2), m2Fx, m2Fy), end='\n\n')


# 计算表2中的三个分力大小
def decomposition():
    print("\tmass = {} kg, theta = {} pi rad".format(p[0], p[1]/pi))
    myFi, Fg = myFine(p[0], p[1]), myFgra(p[0], p[1])
    m1Fi = p[0]*omiga**2*Re
    print(
        "\tmy inertial force = {:.4} N\n\tm1 inertial force = {:.4} N\n\tmy gravity = {:.4} N".format(myFi, m1Fi, Fg), end='\n\n')


# 输出表1中数据
for i in range(5):
    p = [1, i*pi/4]
    print("For point ", i+1, ":", sep='')
    calculate()


# 输出表2中数据
for i in range(5):
    p = [1, i*pi/4]
    print("For point ", i+1, ":", sep='')
    decomposition()


# 计算公式19
print("tidal force (sun):", 3*G*1*Ms*Re/D**3, end='\n\n')


# 缺陷分析建立的模型3
def method3(m, theta):
    Fx = myFgra(m, theta)*cosbeta(theta)-G*Mm*m/d**2
    Fy = -myFgra(m, theta)*sinbeta(theta)
    return Fx, Fy


# 模型2和3数据比较
def compare():
    print("\tmass = {} kg, theta = {} pi rad".format(p[0], p[1]/pi))
    m2Fx, m2Fy = method2(p[0], p[1])
    m3Fx, m3Fy = method3(p[0], p[1])
    m2F = sqrt(m2Fx**2+m2Fy**2)
    m3F = sqrt(m3Fx**2+m3Fy**2)
    print("\tm2F = {:.4} N, m3F = {:.4} N, error rate = {:.4}%".format(
        m2F, m3F, abs(100*(m2F - m3F)/m3F)), end='\n\n')


# 检验数据
for i in range(5):
    p = [1, i*pi/4]
    print("For point ", i+1, ":", sep='')
    compare()


# 计算公式21
print("tidal height:{:.4}".format(3*Mm*Re**4/2/Me/d**3))
