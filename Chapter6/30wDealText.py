# coding:utf8

"""
DESC:30万条新闻文本数据清洗
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,re,time,jieba


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


# 利用jieba对文本进行分词，返回切词后的list
def seg_doc(str_doc):
    sent_list = str_doc.split('\n')
    # 1 正则处理，去掉一些字符，例如\u3000
    sent_list = map(textParse, sent_list)
    # 2 获取停用词
    stwlist = get_stop_words()
    # 3 分词并去除停用词
    word_2dlist = [rm_tokens(jieba.cut(part, cut_all=False),stwlist) for part in sent_list]
    # 4 合并列表
    word_list = sum(word_2dlist, [])
    return word_list


# 正则对字符串清洗
def textParse(str_doc):
    # 去掉字符
    str_doc = re.sub('\u3000', '', str_doc)
    return str_doc


# 创建停用词列表
def get_stop_words(path=r'../Files/NLPIR_stopwords.txt'):
    file = open(path, 'r',encoding='utf-8').read().split('\n')
    return set(file)


# 去掉一些停用词和数字
def rm_tokens(words,stwlist):
    words_list = list(words)
    stop_words = stwlist
    for i in range(words_list.__len__())[::-1]:
        if words_list[i] in stop_words: # 去除停用词
            words_list.pop(i)
        elif words_list[i].isdigit(): # 去除数字
            words_list.pop(i)
        elif len(words_list[i]) == 1:  # 去除单个字符
            words_list.pop(i)
        elif words_list[i] == " ":  # 去除空字符
            words_list.pop(i)
    return words_list


# 读取文本信息
def readFile(path):
    str_doc = ""
    with open(path,'r',encoding='utf-8') as f:
        str_doc = f.read()
    return str_doc




if __name__=='__main__':
    start = time.time()

    filepath = os.path.abspath(r'../Corpus/CSCMNews')
    files = loadFiles(filepath)
    n = 5  # n 表示抽样率， n抽1
    for i, msg in enumerate(files):
        if i % n == 0:
            catg = msg[0]
            file = msg[1]
            file = seg_doc(file)
            if int(i/n) % 1000 == 0:
                print('{t} *** {i} \t docs has been dealed'
                      .format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())),'\n',catg,':\t',file[:30])

    end = time.time()
    print('total spent times:%.2f' % (end-start)+ ' s')






