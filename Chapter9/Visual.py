# coding:utf8

from numpy import *
from pca import *
import matplotlib
import matplotlib.pyplot as plt

'''
Description:PCA降维后的数据可视化显示
Author：伏草惟存
Prompt: code in Python3 env
'''


'''降维后的数据和原始数据可视化'''
def show_picture(dataMat, reconMat):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # flatten()方法能将matrix的元素变成一维的，A能使matrix变成array,A[0]或者数组数据
    ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=50,c='green')
    ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=50, c='red')
    plt.show()






if __name__ == "__main__":
    # 1 加载数据，并转化数据类型为float
    dataMat = loadDataSet('../Files/testSet.txt')
    # print('加载原始特征数据:\n',dataMat)

    # 2 主成分分析降维特征向量设置
    lowDmat, reconMat = pca(dataMat,1)
    # print(shape(lowDmat))
    # 只需要2个特征向量，和原始数据一致，没任何变化
    # lowDmat, reconMat = pca(dataMat, 2)
    # print(shape(lowDmat))

    # 3 将降维后的数据和原始数据一起可视化
    show_picture(dataMat, reconMat)

