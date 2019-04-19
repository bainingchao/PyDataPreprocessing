# coding:utf8

"""
Description:潜在语义分析：LSA
Author：伏草惟存
Prompt: code in Python3 env
"""


from mydict import *
from gensim import corpora, models
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle as pkl
# python的pickle模块实现了基本的数据序列和反序列化。
# 通过pickle模块的序列化操作我们能够将程序中运行的对象信息保存到文件中去，永久存储。
# 通过pickle模块的反序列化操作，我们能够从文件中创建上一次程序保存的对象。

'''
作者：话巴
通俗理解潜在语义分析LSA
https://www.jianshu.com/p/9fe0a7004560

通过对大量的文本集进行统计分析，从中提取出词语的上下文使用含义。技术上通过SVD分解等处理，消除了同义词、多义词的影响，提高了后续处理的精度。
流程：
（1）分析文档集合，建立词汇-文本矩阵A。
（2）对词汇-文本矩阵进行奇异值分解。
（3）对SVD分解后的矩阵进行降维
（4）使用降维后的矩阵构建潜在语义空间

'''

# LSA 潜在语义分析
def gensim_Corpus(corpus=None):
    dictionary = corpora.Dictionary(corpus)
    # 1 doc_bow转化成tfidf向量
    doc_bow_corpus = [dictionary.doc2bow(doc_cut) for doc_cut in corpus]
    tfidf_model = models.TfidfModel(dictionary=dictionary)  # 生成tfidf模型
    tfidf_corpus = [tfidf_model[doc_bow] for doc_bow in doc_bow_corpus]  # 将每doc_bow转换成对应的tfidf_doc向量
    print('doc_bow转换成对应的tfidf_doc向量:\n',tfidf_corpus)

    # 2 生成lsi model
    lsi_model = models.LsiModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=10)
    # 转换成lsi向量
    lsi_corpus = [lsi_model[tfidf_doc] for tfidf_doc in tfidf_corpus]
    print('LSA生成主题:\n',lsi_corpus)

    # 3 将lsi模型存储到磁盘上
    savepath =r'../Files/lsi_model.pkl'
    lsi_file = open(savepath, 'wb')
    pkl.dump(lsi_model, lsi_file)
    lsi_file.close()
    print('--- lsi模型已经生成 ---')


if __name__=='__main__':
    # corpus参数样例数据如下：
    corpus,classVec = loadDataSet()
    gensim_Corpus(corpus)
