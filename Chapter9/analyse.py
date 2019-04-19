# coding:utf8

from numpy import *
from loadnews import *

'''
Description:分析新闻数据主成分特征
Author：伏草惟存
Prompt: code in Python3 env
'''

'''分析数据'''
def analyse_data(dataMat,topNfeat = 20):
    # 去除平均值
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat-meanVals
    # 计算协方差矩阵
    covMat = cov(meanRemoved, rowvar=0)
    # 特征值和特征向量
    eigvals, eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigvals)
    # 保留前N个特征
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    # 对特征主成分分析
    cov_all_score = float(sum(eigvals))
    sum_cov_score = 0
    for i in range(0, len(eigValInd)):
        line_cov_score = float(eigvals[eigValInd[i]])
        sum_cov_score += line_cov_score
        '''
        我们发现其中有超过20%的特征值都是0。
        这就意味着这些特征都是其他特征的副本，也就是说，它们可以通过其他特征来表示，而本身并没有提供额外的信息。

        最前面15个值的数量级大于10^5，实际上那以后的值都变得非常小。
        这就相当于告诉我们只有部分重要特征，重要特征的数目也很快就会下降。

        最后，我们可能会注意到有一些小的负值，他们主要源自数值误差应该四舍五入成0.
        '''
        print('主成分：%s, 方差占比：%s%%, 累积方差占比：%s%%' % (format(i+1, '2.0f'), format(line_cov_score/cov_all_score*100, '4.2f'), format(sum_cov_score/cov_all_score*100, '4.1f')))




if __name__ == "__main__":
    # 加载新闻数据
    dataMat = replaceNanWithMean()
    # print(shape(dataMat))
    # 分析数据：要求满足99%即可
    line_cov_score=analyse_data(dataMat,20)
