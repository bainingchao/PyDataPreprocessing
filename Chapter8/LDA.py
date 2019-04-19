# coding:utf8

"""
Description:生成lda特征(主题模型)
Author：伏草惟存
Prompt: code in Python3 env
"""

from mydict import *
from gensim import corpora, models
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pickle as pkl
import umap


'''
作者：-柚子皮-
主题模型TopicModel：隐含狄利克雷分布LDA
https://blog.csdn.net/pipisorry/article/details/42649657

什么是LDA？
它是一种无监督的贝叶斯模型。
是一种主题模型，它可以将文档集中的每篇文档按照概率分布的形式给出。
是一种无监督学习，在训练时不需要手工标注的训练集，需要的是文档集和指定主题的个数。
是一种典型的词袋模型，它认为一篇文档是由一组词组成的集合，词与词之间没有顺序和先后关系。

隐含狄利克雷分布简称LDA(Latent Dirichlet allocation)，首先由吴恩达等人于2003年提出，目前在文本挖掘领域包括文本主题识别、文本分类以及文本相似度计算方面都有应用。

LDA是一种典型的词袋模型，即它认为一篇文档是由一组词构成的一个集合，词与词之间没有顺序以及先后的关系。一篇文档可以包含多个主题，文档中每一个词都由其中的一个主题生成。
它是一种主题模型，它可以将文档集中每篇文档的主题按照概率分布的形式给出；
同时是一种无监督学习算法，在训练时不需要手工标注的训练集，需要的仅仅是文档集以及指定主题的数量k即可；
此外LDA的另一个优点则是，对于每一个主题均可找出一些词语来描述它；

LDA可以被认为是一种聚类算法：
主题对应聚类中心，文档对应数据集中的例子。
主题和文档在特征空间中都存在，且特征向量是词频向量。
LDA不是用传统的距离来衡量一个类簇，它使用的是基于文本文档生成的统计模型的函数。


'''


# 生成lda特征(主题模型)
def gensim_Corpus(corpus=None):
    dictionary = corpora.Dictionary(corpus)
    # 1 doc_bow转化为tfidf向量
    doc_bow_corpus = [dictionary.doc2bow(doc_cut) for doc_cut in corpus]
    tfidf_model = models.TfidfModel(dictionary=dictionary)  # 生成tfidf模型
    # 将每doc_bow转换成对应的tfidf_doc向量
    tfidf_corpus = [tfidf_model[doc_bow] for doc_bow in doc_bow_corpus]
    print('doc_bow转换成对应的tfidf_doc向量:\n',tfidf_corpus)

    lda_model = models.LdaModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=10)  # 生成lda model
    # 2 生成corpus of LDA
    lda_corpus = [lda_model[tfidf_doc] for tfidf_doc in tfidf_corpus]  # 转换成lda向量
    print('LDA生成主题:\n',lda_corpus)

    # 3 将LDA模型存储到磁盘上
    savepath =r'../Files/lda_model.pkl'
    lda_file = open(savepath, 'wb')
    pkl.dump(lda_model, lda_file)
    lda_file.close()
    print('--- lda模型已经生成 ---')















if __name__=='__main__':
    # corpus参数样例数据如下：
    corpus,classVec = loadDataSet()
    gensim_Corpus(corpus)




