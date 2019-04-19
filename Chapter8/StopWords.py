# coding:utf8

"""
Description:自定义去停用词
Author：伏草惟存
Prompt: code in Python3 env
"""

import re,jieba,sys

# 加载自定义分词词典
jieba.load_userdict("../Files/user_dict.txt")


#********************1 结巴中文分词***********************************

# 利用jieba对文本进行分词，返回切词后的list
def seg_doc(str_doc):
    # 1 正则处理原文本
    sent_list = str_doc.split('\n')
    # map内置高阶函数:一个函数f和list，函数f依次作用在list.
    sent_list = map(textParse, sent_list)  # 正则处理，去掉一些字符，例如\u3000

    # 2 获取停用词
    stwlist = get_stop_words()

    # 3 分词并去除停用词
    word_2dlist = [rm_tokens(jieba.cut(part, cut_all=False),stwlist) for part in sent_list]

    # 4 合并列表
    word_list = sum(word_2dlist, [])
    return word_list


# 正则对字符串清洗
def textParse(str_doc):
    # 正则过滤掉特殊符号、标点、英文、数字等。
    # r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:：;；|<=>?@，—。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # str_doc=re.sub(r1, ' ', str_doc)

    # 去掉字符
    str_doc = re.sub('\u3000', '', str_doc)

    # 去除空格
    # str_doc=re.sub('\s+', ' ', str_doc)

    # 去除换行符
    # str_doc = str_doc.replace('\n',' ')
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
    # 1 读取文本
    path= r'../dataSet/CSCMNews/体育/0.txt'
    str_doc = readFile(path)
    # print(str_doc)

    # 2 分词去停用词
    word_list = seg_doc(str_doc)
    print(word_list)