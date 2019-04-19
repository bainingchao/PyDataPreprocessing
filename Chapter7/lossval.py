# coding:utf8

"""
Description:处理数据缺失值
Author：伏草惟存
Prompt: code in Python3 env
"""

# 处理数据缺失值
# 使用可用特征的均值来填补缺失值
# 使用特殊值来填补缺失值如-1，0
# 忽略有缺失值的样本
# 使用相似样本的均值填补缺失值
# 使用机器学习算法预测缺失值


import numpy
from numpy import *

'''加载数据集'''
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    # print(stringArr) # 二维数组
    datArr = [list(map(float, line)) for line in stringArr]
    # print(mat(datArr))
    return mat(datArr)

"""

'''将NaN替换成平均值函数'''
def replaceNanWithMean():
    datMat = loadDataSet('../Files/dataset.data','    ')
    numFeat = shape(datMat)
    # print(numFeat[1]-1)  # 特征数3
    for i in range(numFeat[1]-1):
        # 对value不为NaN的求均值，A 返回矩阵基于的数组
        # print(datMat[nonzero(~isnan(datMat[:, i].A))[0],i]) # 列特征非nan数据
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i])
        # 将value为NaN的值赋值为均值
        datMat[nonzero(isnan(datMat[:, i].A))[0],i] = meanVal
    return datMat


if __name__=='__main__':
    # 加载数据集
    loadDataSet('../Files/dataset.data','    ')

    # 均值填补缺失值
    datMat = replaceNanWithMean()
    print(datMat)

"""

#************3 Pandas 处理丢失值*******************
# 机器学习和数据挖掘等领域由于数据缺失导致的数据质量差，
# 在模型预测的准确性上面临着严重的问题。

import pandas as pd
import numpy as np

datMat = loadDataSet('../Files/dataset.data','    ')
df = pd.DataFrame(datMat)
# df = pd.DataFrame(datMat, index=range(datMat.shape[0]),columns=['one', 'two', 'three', 'four'] )
# 使用重构索引(reindexing)，创建了一个缺少值的DataFrame。 输出中，NaN表示不是数字的值
# df = df.reindex(range(datMat.shape[0]))

# 1 重构矩阵
# print (df)    # 打印矩阵

# 2 检查是否为空
# print (df.isnull())
# print (df['one'].notnull()) # 检查第一列是否为空

# 3 均值填充法：NAN视为0.若数据是 NAN和是 NAN

lossVs = [df[col].mean() for col in range(datMat.shape[1])] # 计算特征列均值
# print(lossVs)
lists= [ list(df[i].fillna(lossVs[i])) for i in range(len(lossVs)) ]
print(mat(lists).T)

# lists.append(list(df[0].fillna(lossVs[0])))
# lists.append(list(df[1].fillna(lossVs[1])))
# lists.append(list(df[2].fillna(lossVs[2])))
# lists.append(list(df[3].fillna(lossVs[3])))


# 4 其他缺失值处理方法
# 4.1 用标量值替换NaN
# print ("NaN replaced with '0':")
# print (df.fillna(0))

# 4.2 前进和后退:pad/fill 和 bfill/backfill
# print (df.fillna(method='pad'))
# print (df.fillna(method='backfill'))

# 4.3 丢失缺少的值：axis=0在行上应用，axis=1在列上应用
# print (df.dropna(axis=0))

# 4.4 忽略无效值
# print("df.dropna():\n{}\n".format(df.dropna()))