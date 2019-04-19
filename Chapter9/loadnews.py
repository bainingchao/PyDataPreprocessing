# coding:utf8

from numpy import *
from loadData import *

'''
Description:处理带有缺少值的新闻数据
Author：伏草惟存
Prompt: code in Python3 env
'''



'''将NaN替换成平均值函数
secom.data 为1567篇文章，每篇文章590个单词
'''
def replaceNanWithMean():
    datMat = loadDataSet('../Files/news.data', ' ')
    # print('缺少值的新闻数据:\n',datMat)
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        # 对value不为NaN的求均值
        # .A 返回矩阵基于的数组
        meanVal = mean(datMat[nonzero(~isnan(datMat[:, i].A))[0], i])
        # 将value为NaN的值赋值为均值
        datMat[nonzero(isnan(datMat[:, i].A))[0],i] = meanVal
    return datMat



if __name__ == "__main__":
    # 加载新闻数据
    dataMat = replaceNanWithMean()
    print('处理缺少值的新闻数据:\n',dataMat)
    print('新闻矩阵数据规模:\n',shape(dataMat))

