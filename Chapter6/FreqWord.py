# coding:utf8

"""
DESC:NLTK词频统计
Author：伏草惟存
Prompt: code in Python3 env
"""

from nltk import *
from StopWords import readFile,seg_doc


#解决中文显示
import matplotlib
# （1）查看当前使用字体格式
# from matplotlib.font_manager import findfont, FontProperties
# print(findfont(FontProperties(family=FontProperties().get_family())))
# （2）在C:\Windows\Fonts查找中文字体SimHei.ttf，并将其复制到../mpl-data/font/ttf文件夹下面
# (3) 设置使用字体
matplotlib.rcParams['font.sans-serif'] = 'SimHei'


# 利用nltk进行词频特征统计
def nltk_wf_feature(word_list=None):
    # ********统计词频方法1**************
    fdist=FreqDist(word_list)
    print(fdist.keys(),fdist.values())

    print('='*3,'指定词语词频统计','='*3)
    w='训练'
    print(w,'出现频率：',fdist.freq(w)) # 给定样本的频率
    print(w,'出现次数：',fdist[w]) # 出现次数

    print('='*3,'频率分布表','='*3)
    fdist.tabulate(10) # 频率分布表

    # print('='*3,'可视化词频','='*3)
    # fdist.plot(30) # 频率分布图
    fdist.plot(30,cumulative=True) # 频率累计图

    # print('='*3,'根据词语长度查找词语','='*3)
    # wlist =[w for w in fdist if len(w)>2]
    # print(wlist)


    # ********统计词频方法2**************
    from collections import Counter
    Words = Counter(word_list)
    print(Words.keys(),Words.values())
    wlist =[w for w in Words if len(w)>2]
    print(wlist)

    return fdist



if __name__=='__main__':
    # 1 读取文本
    path= r'../Corpus/CSCMNews/体育/0.txt'
    str_doc = readFile(path)
    # print(str_doc)

    # 2 词频特征统计
    word_list =seg_doc(str_doc)
    fdist = nltk_wf_feature(word_list)
