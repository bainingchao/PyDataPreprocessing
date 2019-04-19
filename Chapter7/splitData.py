# coding:utf8

"""
Description:解析数据文件，返回特征集和标签
Author：伏草惟存
Prompt: code in Python3 env
"""

'''
特征数据集：
特征1：年均投入时间（min）
特征2：玩游戏占时间百分比
特征3：每天看综艺的时间（h）

标签集：
1：学习专注
2：学习正常
3：比较贪玩
'''

import os
from numpy import *


def file_matrix(filename):
    f = open(filename)
    arrayLines = f.readlines()

    returnMat = zeros((len(arrayLines),3))    # 特征数据集
    classLabelVactor = []                     # 标签集
    index = 0
    for line in arrayLines:
        listFromLine = line.strip().split('\t')    # 分析数据，空格处理
        returnMat[index,:] = listFromLine[0:3]
        classLabelVactor.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVactor



if __name__=='__main__':
    path = os.path.abspath(r'../Files/dataset.txt')
    returnMat,classLabelVactor=file_matrix(path)
    print('数据集:\n',returnMat,'\n标签集:\n',classLabelVactor)