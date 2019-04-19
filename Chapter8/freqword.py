# coding:utf8

"""
Description:gensim统计词频特征
Author：伏草惟存
Prompt: code in Python3 env
"""

from gensim import corpora
from mydict import *


# 2 统计词频特征
def gensim_Corpus(corpus=None):
    dictionary = corpora.Dictionary(corpus)
    dfs = dictionary.dfs  # 词频词典
    print('统计词频特征:')
    for key_id, c in dfs.items():
        print(dictionary[key_id], c)
    return dictionary[key_id], c



if __name__=='__main__':
    # corpus参数样例数据如下：
    corpus,classVec = loadDataSet()
    gensim_Corpus(corpus)
