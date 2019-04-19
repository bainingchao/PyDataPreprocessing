# coding:utf8

"""
Description: 利用sklearn计算tfidf值特征
Author：伏草惟存
Prompt: code in Python3 env
"""

from StopWords import readFile,seg_doc
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


# 利用sklearn计算tfidf值特征
def sklearn_tfidf_feature(corpus=None):
    # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer() # 构建词汇表
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])

if __name__=='__main__':
    corpus =[]
    # corpus参数样例数据如下：
    # corpus = ["我 来到 成都 成都 春熙路 很 开心",
              # "今天 在 宽窄巷子 耍 了 一天 ",
              # "成都 整体 来说 还是 挺 安逸 的",
              # "成都 的 美食 真 巴适 惨 了"]
    # 1 读取文本
    path1= r'../dataSet/CSCMNews/体育/0.txt'
    str_doc1 = readFile(path1)
    word_list1 =' '.join(seg_doc(str_doc1))

    path2= r'../dataSet/CSCMNews/时政/339764.txt'
    str_doc2 = readFile(path2)
    word_list2 =' '.join(seg_doc(str_doc2))

    corpus.append(word_list1)
    corpus.append(word_list2)

    sklearn_tfidf_feature(corpus)