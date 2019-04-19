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
    # 构建词汇表
    vectorizer = CountVectorizer()
    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()
     # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    # 元素a[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    # 第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    for i in range(len(weight)):
        print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
        for j in range(len(word)):
            print(word[j], weight[i][j])




if __name__=='__main__':
    # corpus参数样例数据如下：
    corpus = ["我 来到 成都 成都 春熙路 很 开心",
              "今天 在 宽窄巷子 耍 了 一天 ",
              "成都 整体 来说 还是 挺 安逸 的",
              "成都 的 美食 真 巴适 惨 了"]

    sklearn_tfidf_feature(corpus)