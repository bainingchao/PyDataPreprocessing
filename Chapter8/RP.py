# coding:utf8

"""
Description:生成随机映射（Random Projections，RP)
Author：伏草惟存
Prompt: code in Python3 env
"""


from mydict import *
from gensim import corpora, models
import pickle as pkl



'''
随机映射（Random Projections，RP）
目的在于减小空维度。这是一个非常高效（对CPU和内存都很友好）方法，通过抛出一点点随机性，来近似得到两个文档之间的Tfidf距离。推荐目标维度也是成百上千，具体数值要视你的数据集大小而定。

优点：减小空维度、CPU和内存都很友好
'''


 # 生成随机映射（Random Projections，RP)
def gensim_Corpus(corpus=None):
    dictionary = corpora.Dictionary(corpus)
    # 1 doc_bow转化为tfidf向量
    doc_bow_corpus = [dictionary.doc2bow(doc_cut) for doc_cut in corpus]
    tfidf_model = models.TfidfModel(dictionary=dictionary)  # 生成tfidf模型
    tfidf_corpus = [tfidf_model[doc_bow] for doc_bow in doc_bow_corpus]
    print('doc_bow转换成对应的tfidf_doc向量:\n',tfidf_corpus)

    # 2 生成corpus of RP
    rp_model = models.RpModel(tfidf_corpus, num_topics=10)
    rp_corpus = [rp_model[tfidf_doc] for tfidf_doc in tfidf_corpus]  # 转换成随机映射tfidf向量
    print('RP:\n',rp_corpus)

    # 3 将RP模型存储到磁盘上
    savepath =r'../Files/rp_model.pkl'
    rp_file = open(savepath, 'wb')
    pkl.dump(rp_model, rp_file)
    rp_file.close()
    print('--- RP模型已经生成 ---')



if __name__=='__main__':
    # corpus参数样例数据如下：
    corpus,classVec = loadDataSet()
    gensim_Corpus(corpus)

