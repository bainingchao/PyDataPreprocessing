# coding:utf8

"""
Description:相似度计算
Author：伏草惟存
Prompt: code in Python3 env
"""

from numpy import linalg as la
from numpy import *

'''原矩阵
列向量为商品的类别
行向量为用户对商品的评分
可以根据相似度推荐商品
'''
def loadExData():
    return [[1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [1, 1, 1, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1]]


'''基于欧氏距离相似度计算，假定inA和inB 都是列向量
相似度=1/(1+距离),相似度介于0-1之间
norm：范式计算，默认是2范数，即:sqrt(a^2+b^2+...)
'''
def ecludSim(inA, inB):
    return 1.0/(1.0 + la.norm(inA - inB))


'''皮尔逊相关系数
范围[-1, 1]，归一化后[0, 1]即0.5 + 0.5 *
相对于欧式距离，不敏感皮尔逊相关系数
'''
def pearsSim(inA, inB):
    return 0.5 + 0.5 * corrcoef(inA, inB, rowvar=0)[0][1]


'''计算余弦相似度
如果夹角为90度相似度为0；两个向量的方向相同，相似度为1.0
余弦取值-1到1之间，归一化到0与1之间即：相似度=0.5 + 0.5*cosθ
余弦相似度cosθ=(A*B/|A|*|B|)
'''
def cosSim(inA, inB):
    num = float(inA.T*inB) # 矩阵相乘
    denom = la.norm(inA)*la.norm(inB) # 默认是2范数
    return 0.5 + 0.5*(num/denom)



if __name__=='__main__':
    # 3 相似度计算
    # 3.1 计算欧氏距离,比较第一列商品A和第四列商品D的相似率
    myMat = mat(loadExData())
    # print(myMat[:, 3])
    print('欧氏距离\n',ecludSim(myMat[:, 0], myMat[:, 3]))
    # 3.2 计算余弦相似度
    print('余弦相似度距离\n',cosSim(myMat[:, 0], myMat[:, 3]))
    # 3.3 计算皮尔逊相关系数
    print('皮尔逊距离\n',pearsSim(myMat[:, 0], myMat[:, 3]))

