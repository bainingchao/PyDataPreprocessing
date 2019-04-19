# coding:utf8

"""
Description:词袋模型
Author：伏草惟存
Prompt: code in Python3 env
"""

from numpy import *
import numpy as np


'''创建数据集：单词列表postingList, 所属类别classVec'''
def loadDataSet():
    # corpus参数样例数据如下：
    corpus =[]
    tiyu = ['姚明', '我来', '承担', '连败', '巨人', '宣言', '酷似', '当年', '麦蒂', '新浪', '体育讯', '北京', '时间', '消息', '休斯敦', '纪事报', '专栏', '记者', '乔纳森', '费根', '报道', '姚明', '渴望', '一场', '胜利', '当年', '队友', '麦蒂', '惯用', '句式']
    yule = ['谢婷婷', '模特', '酬劳', '仅够', '生活', '风光', '背后', '惨遭', '拖薪', '新浪', '娱乐', '金融', '海啸', 'blog', '席卷', '全球', '模特儿', '酬劳', '被迫', '打折', '全职', 'Model', '谢婷婷', '业界', '工作量', '有增无减', '收入', '仅够', '糊口', '拖薪']
    jioayu = ['名师', '解读', '四六级', '阅读', '真题', '技巧', '考前', '复习', '重点', '历年', '真题', '阅读', '听力', '完形', '提升', '空间', '天中', '题为', '主导', '考过', '六级', '四级', '题为', '主导', '真题', '告诉', '方向', '会考', '题材', '包括']
    shizheng = ['美国', '军舰', '抵达', '越南', '联合', '军演', '中新社', '北京', '日电', '杨刚', '美国', '海军', '第七', '舰队', '三艘', '军舰', '抵达', '越南', '岘港', '为期', '七天', '美越', '南海', '联合', '军事训练', '拉开序幕', '美国', '海军', '官方网站', '消息']

    corpus.append(tiyu)
    corpus.append(yule)
    corpus.append(jioayu)
    corpus.append(shizheng)

    classVec = ['体育','娱乐','教育','时政']
    return  corpus,classVec


'''获取所有单词的集合:返回不含重复元素的单词列表'''
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # 操作符 | 用于求两个集合的并集
    # print(vocabSet)
    return list(vocabSet)



'''文档词袋模型构建数据矩阵'''
def bagOfWords2VecMN(vocabList, DataSet):
    # 1 所有文档的词向量
    VecList = []
    for inputSet in DataSet:
        # print('-->',inputSet)
        returnVec = [0] * len(vocabList)
        for word in inputSet:
            if word in vocabList:
                returnVec[vocabList.index(word)] += 1
        VecList.append(returnVec)
    return VecList



'''词袋模型转化为tf-idf计算
实现自动摘要
https://www.cnblogs.com/cppb/p/5976266.html
'''
def TFIDF(bagvec):
    # 词频 = 某个词在文章中出现的总次数/文章中出现次数最多的词的个数
    tf = [ doc/sum(doc) for doc in bagvec]
    # 逆文档频率（IDF） = log（词料库的文档总数/包含该词的文档数+1）
    m = len(bagvec) # 词料库的文档总数
    ndw =sum(mat(bagvec).T!=0,axis=1).T  # 包含该词的文档数
    idf =  [ log(m/(t+1)) for t in ndw]
    tfidf = tf * np.array(idf)
    # 设置保留小数位
    np.set_printoptions(precision=2)
    # print('tf:\n',mat(tf),'\nndw:\n',ndw,'\nidf:\n',idf,'\ntfidf:\n',tfidf)
    return tfidf



if __name__=='__main__':
    # 1 打印数据集和标签
    dataSet,classlab = loadDataSet()
    print('数据集:\n',mat(dataSet),'\n标签集:\n',mat(classlab))

    # 2 获取所有单词的集合
    vocabList=createVocabList(dataSet)
    print('\n词汇列表：\n',vocabList)

    #***********特征词转向量*********************
    # 3 词袋模型:文本向量转化
    bagvec = bagOfWords2VecMN(vocabList, dataSet)
    print('词袋模型:\n',mat(bagvec))

    # 4 tf-idf计算
    tfidf = TFIDF(bagvec)
    print('tf-idf:\n ',tfidf)

