#coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


# 绘制3D梯度下降图
def d3_hookface():
    fig = plt.figure()  # 得到画面
    ax = fig.gca(projection='3d')  # 得到3d坐标的图
    X = np.arange(-5, 5, 0.1)
    Y = np.arange(-5, 5, 0.1)
    X,Y = np.meshgrid(X, Y)  # 将坐标向量变为坐标矩阵，列为x的长度，行为y的长度
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    # 曲面，x,y,z坐标，横向步长，纵向步长，颜色，线宽，是否渐变
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.set_xlabel("x-label", color='r')
    ax.set_ylabel("y-label", color='g')
    ax.set_zlabel("z-label", color='b')

    ax.zaxis.set_major_locator(LinearLocator(10))  # 设置z轴标度
    ax.zaxis.set_major_formatter(FormatStrFormatter('%0.02f'))  # 设置z轴精度
    # shrink颜色条伸缩比例0-1, aspect颜色条宽度（反比例，数值越大宽度越窄）
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.savefig("d3_hookface.png")
    plt.show()





def d3_scatter():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = 50

    # For each set of style and range settings, plot n random points in the box
    # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
    for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('g', '+', -20, 15),('b', '^', -30, -5)]:
        xs = randrange(n, 23, 32)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zlow, zhigh)
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()




def randrange(n, vmin, vmax):
    return (vmax - vmin) * np.random.rand(n) + vmin


if __name__ =='__main__':
    # 绘制3D梯度下降图
    # d3_hookface()
    # 绘制3D散点图
    d3_scatter()