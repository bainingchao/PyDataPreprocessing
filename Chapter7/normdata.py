# coding:utf8

"""
Description:不均衡的数据归一化处理方法
Author：伏草惟存
Prompt: code in Python3 env
"""

from numpy import *
from lossval import replaceNanWithMean


'''数值归一化：特征值转化为0-1之间：newValue = (oldValue-min)/(max-min)'''
def norm_dataset(dataset):
    minVals = dataset.min(0)  # 参数0是取得列表中的最小值，而不是行中最小值
    maxVals = dataset.max(0)
    ranges = maxVals - minVals

    normdataset = zeros(shape(dataset)) # 生成原矩阵一样大小的0矩阵
    m = dataset.shape[0]

    # tile:复制同样大小的矩阵
    molecular = dataset - tile(minVals,(m,1))  # 分子： (oldValue-min)
    Denominator = tile(ranges,(m,1))           # 分母：(max-min)
    normdataset = molecular / Denominator     # 归一化结果。

    print('归一化的数据结果：\n'+str(normdataset))
    return normdataset,ranges,minVals



if __name__=='__main__':
    dataset = replaceNanWithMean()
    print('归一化前数据结果：\n',dataset)
    normdataset,ranges,minVals = norm_dataset(dataset[:,:-1])
    # print(normdataset[:100])


