# coding:utf8

import re,itertools

"""
DESC:  正则清洗数据
Author：伏草惟存
Prompt: code in Python3 env
"""

'''
re.I    使匹配对大小写不敏感
re.L    做本地化识别（locale-aware）匹配
re.M    多行匹配，影响 ^ 和 $
re.S    使 . 匹配包括换行在内的所有字符
re.U    根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
re.X    该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
'''
# 正则对字符串清洗
def textParse(str_doc):
    # 正则过滤掉特殊符号、标点、英文、数字等。
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:：;；|<=>?@，—。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # 去除空格
    r2 = '\s+'
    # 去除换行符
    str_doc=re.sub(r1, ' ', str_doc)
    # 多个空格成1个
    str_doc=re.sub(r2, ' ', str_doc)
    # 去除换行符
    # str_doc = str_doc.replace('\n',' ')
    return str_doc


# 读取文本信息
def readFile(path):
    str_doc = ""
    with open(path,'r',encoding='utf-8') as f:
        str_doc = f.read()
    return str_doc



if __name__=='__main__':
    # 1 读取文本
    path= r'../Corpus/CSCMNews/体育/0.txt'
    str_doc = readFile(path)
    # print(str_doc)

    # 2 正则清洗字符串
    word_list=textParse(str_doc)
    print(word_list)

