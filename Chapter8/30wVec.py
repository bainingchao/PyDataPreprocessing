# coding:utf8

"""
Description:gensim实现30万条新闻文本特征向量化
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,time,sys
from gensim import corpora, models
from StopWords import *


#******************** 高效读取文件***********************************
class loadFolders(object):   # 迭代器
    def __init__(self, par_path):
        self.par_path = par_path
    def __iter__(self):
        for file in os.listdir(self.par_path):
            file_abspath = os.path.join(self.par_path, file)
            if os.path.isdir(file_abspath): # if file is a folder
                yield file_abspath

class loadFiles(object):
    def __init__(self, par_path):
        self.par_path = par_path
    def __iter__(self):
        folders = loadFolders(self.par_path)
        for folder in folders:              # level directory
            catg = folder.split(os.sep)[-1]
            for file in os.listdir(folder):     # secondary directory
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    this_file = open(file_path, 'rb') #rb读取方式更快
                    content = this_file.read().decode('utf8')
                    yield catg, content
                    this_file.close()



if __name__=='__main__':
    start = time.time()

    n = 5  # n 表示抽样率
    path_doc_root = '../Corpus/CSCMNews'  # 根目录 即存放按类分类好的文本数据集
    path_tmp = '../Corpus/CSCMNews_model'  # 存放中间结果的位置
    path_dictionary = os.path.join(path_tmp, 'CSCMNews.dict')
    path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus')


    if not os.path.exists(path_tmp):
        os.makedirs(path_tmp)
    # # ===================================================================
    # #  第一阶段，遍历文档，生成词典,并去掉频率较少的项
    #       如果指定的位置没有词典，则重新生成一个。如果有，则跳过该阶段
    if not os.path.exists(path_dictionary):
        print('=== 未检测到有词典存在，开始遍历生成词典 ===')
        dictionary = corpora.Dictionary()
        files = loadFiles(path_doc_root)
        for i, msg in enumerate(files):
            if i % n == 0:
                catg = msg[0]
                content = msg[1]
                content = seg_doc(content)
                dictionary.add_documents([content])
                if int(i/n) % 1000 == 0:
                    print('{t} *** {i} \t docs has been dealed'
                          .format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
        # 去掉词典中出现次数过少的
        small_freq_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq < 5 ]
        dictionary.filter_tokens(small_freq_ids)
        dictionary.compactify() # 从新产生连续的编号
        dictionary.save(path_dictionary)
        print('=== 词典已经生成 ===')
    else:
        print('=== 检测到词典已经存在，跳过该阶段 ===')

    # # ===================================================================
    # # # 第二阶段，  开始将文档转化成tfidf
    dictionary = None
    if not os.path.exists(path_tmp_tfidf):
        print('=== 未检测到有tfidf文件夹存在，开始生成tfidf向量 ===')
        # 如果指定的位置没有tfidf文档，则生成一个。如果有，则跳过该阶段
        if not dictionary:  # 如果跳过了第一阶段，则从指定位置读取词典
            dictionary = corpora.Dictionary.load(path_dictionary)
        os.makedirs(path_tmp_tfidf)
        files = loadFiles(path_doc_root)
        tfidf_model = models.TfidfModel(dictionary=dictionary)
        corpus_tfidf = {}
        for i, msg in enumerate(files):
            if i % n == 0:
                catg = msg[0]
                content = msg[1]
                word_list = seg_doc(content)
                file_bow = dictionary.doc2bow(word_list)
                file_tfidf = tfidf_model[file_bow]
                tmp = corpus_tfidf.get(catg, [])
                tmp.append(file_tfidf)
                if tmp.__len__() == 1:
                    corpus_tfidf[catg] = tmp
            if i % 10000 == 0:
                print('{i} files is dealed'.format(i=i))
        # 将tfidf中间结果储存起来
        catgs = list(corpus_tfidf.keys())
        for catg in catgs:
            corpora.MmCorpus.serialize('{f}{s}{c}.mm'.format(f=path_tmp_tfidf, s=os.sep, c=catg),corpus_tfidf.get(catg),id2word=dictionary)
            print('catg {c} has been transformed into tfidf vector'.format(c=catg))
        print('=== tfidf向量已经生成 ===')
    else:
        print('=== 检测到tfidf向量已经生成，跳过该阶段 ===')

    end = time.time()
    print('total spent times:%.2f' % (end-start)+ ' s')






