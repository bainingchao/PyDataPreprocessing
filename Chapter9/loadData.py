# coding:utf8

from numpy import *

'''
Description:加载坐标系数据
Author：伏草惟存
Prompt: code in Python3 env
'''

'''加载数据集'''
def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr = [list(map(float, line)) for line in stringArr]
    #注意这里和python2的区别，需要在map函数外加一个list（），否则显示结果为 map at 0x3fed1d0
    return mat(datArr)



if __name__ == "__main__":
    # 1 加载数据，并转化数据类型为float
    dataMat = loadDataSet('../Files/testSet.txt')
    print('坐标系原始数据:\n',dataMat)

