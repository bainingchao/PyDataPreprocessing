# coding:utf8

"""
Description:30万条新闻文本数据清洗
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,time
from StopWords import *
from wordbag import *

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

    filepath = os.path.abspath(r'../Corpus/CSCMNews')
    files = loadFiles(filepath)
    n = 5  # n 表示抽样率， n抽1
    for i, msg in enumerate(files):
        if i % n == 0:
            catg = msg[0]
            content = msg[1]
            # 每个文档的TFIDF向量化-->所有词集（gensim）
            word_list = seg_doc(content)
            vocabList=createVocabList(word_list)
            bagvec = bagOfWords2VecMN(vocabList, word_list)
            tfidf = TFIDF(bagvec)
            if int(i/n) % 1000 == 0:
                print('{t} *** {i} \t docs has been dealed'
                      .format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())),'\n',catg,':\t',tfidf)

    end = time.time()
    print('total spent times:%.2f' % (end-start)+ ' s')






