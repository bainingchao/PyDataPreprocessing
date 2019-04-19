# coding:utf8

from numpy import *
import matplotlib
import matplotlib.pyplot as plt

'''
Description:PCA新闻数据降维并可视化分析
Author：伏草惟存
Prompt: code in Python3 env
'''

'''加载数据集'''
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [list(map(float, line)) for line in stringArr]
    return mat(datArr)


# 将NaN替换成平均值函数：secom.data 为1567篇文章，每篇文章590个单词
def replaceNanWithMean():
    datMat = loadDataSet('../Files/news.data', ' ')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i])
        datMat[nonzero(isnan(datMat[:, i].A))[0],i] = meanVal
    return datMat


# 主成分降维
def pca(dataMat, topNfeat=9999999):
    # 1 计算每一列的均值
    meanVals = mean(dataMat, axis=0) # axis=0表示列，axis=1表示行

    # 2 去平均值，每个向量同时都减去均值
    meanRemoved = dataMat - meanVals

    # 3 计算协方差矩阵的特征值与特征向量
    covMat = cov(meanRemoved, rowvar=0)
    eigVals, eigVects = linalg.eig(mat(covMat))
    print('特征值:\n', eigVals,'\n特征向量:\n', eigVects) # 很多特征值为0

    # 4 将特征值排序
    eigValInd = argsort(eigVals)

    # 5 保留前N个特征
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:, eigValInd]
    # print('重组n特征向量最大到最小:\n', redEigVects.T)

    # 6 将数据转换到新空间
    lowDDataMat = meanRemoved * redEigVects
    reconMat = (lowDDataMat * redEigVects.T) + meanVals
    return lowDDataMat, reconMat




'''降维后的数据和原始数据可视化'''
def show_picture(dataMat, reconMat):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0], marker='^', s=5,c='green')
    ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0], marker='o', s=5, c='red')
    plt.show()




if __name__ == "__main__":
    dataMat = replaceNanWithMean()
    # 分析数据
    lowDmat, reconMat = pca(dataMat,17)
    print(shape(lowDmat)) # 1567篇文章，提取前20个单词
    show_picture(dataMat, reconMat)
