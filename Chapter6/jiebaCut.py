#coding:utf8

"""
DESC: jieba分词操作详解
Author：伏草惟存
Prompt: code in Python3 env
"""

import jieba,os
import jieba.posseg
import jieba.analyse


'''
支持三种分词模式与特点：
    精确模式:试图将句子最精确地切开，适合文本分析；
    全模式:把句子中所有的可以成词的词语都扫描出来, 速度非常快，但是不能解决歧义；
    搜索引擎模式:在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
    支持繁体分词
    支持自定义词典
安装方法：
    自动安装： pip install jieba
    半自动安装：下载 http://pypi.python.org/pypi/jieba/解压后运行 python setup.py install
    手动安装：将 jieba 目录放置于当前目录或者 site-packages 目录,
    通过 import jieba 来引用

核心算法：
    基于前缀词典实现高效的词图扫描，生成句子中汉字所有可能成词情况所构成的有向无环图 (DAG)
    采用了动态规划查找最大概率路径, 找出基于词频的最大切分组合
    对于未登录词，采用了基于汉字成词能力的 HMM 模型，使用了 Viterbi 算法
主要功能：
    jieba.cut 三个输入参数: 待分词的字符串；cut_all参数是否全模式；HMM 参数是否 HMM 模型
    jieba.cut_for_search 两个参数：待分词的字符串；是否 HMM 模型。该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细
    jieba.lcut 以及 jieba.lcut_for_search 直接返回 list
    jieba.Tokenizer(dictionary=DEFAULT_DICT) 新建自定义分词器，可用于同时使用不同词典。jieba.dt 为默认分词器。

'''


#********************1 结巴中文分词基本操作***********************************

print('='*40)
print('1. 分词')
print('-'*40)

# 1 全模式，扫描所有可以成词的词语, 速度非常快，不能解决歧义.
seg_list = jieba.cut("我来到成都四川大学", cut_all=True)
print("\nFull Mode: " + "/ ".join(seg_list))

# 2 默认是精确模式，适合文本分析.
seg_list = jieba.cut("我来到成都四川大学", cut_all=False)
print("\nDefault Mode: " + "/ ".join(seg_list))  # 默认模式

seg_list = jieba.cut("他来到了网易杭研大厦")
print('\n默认切词：'+"/ ".join(seg_list))

# 3 搜索引擎模式,对长词再次切分，提高召回率，适合用于搜索引擎分词。
#jieba.cut_for_search 该方法适合用于搜索引擎构建倒排索引的分词，粒度比较细

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造",HMM=False)
print('\n搜索引擎模式：'+", ".join(seg_list))



print('='*40)
print('2. 添加自定义词典/调整词典')
print('-'*40)

print('原文档：\t'+'/'.join(jieba.cut('如果放到数据库中将出错。', HMM=False)))
#如果/放到/数据库/中将/出错/。
print(jieba.suggest_freq(('中', '将'), True))
#494
print('改进文档：\t'+'/'.join(jieba.cut('如果放到数据库中将出错。', HMM=False)))
#如果/放到/数据库/中/将/出错/。
print('\n原文档：\t'+'/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
#「/台/中/」/正确/应该/不会/被/切开
print(jieba.suggest_freq('台中', True))
#69
print('改进文档：\t'+'/'.join(jieba.cut('「台中」正确应该不会被切开', HMM=False)))
#「/台中/」/正确/应该/不会/被/切开

#********************2 加载自定义分词词典***********************************
import sys
sys.path.append("../")
jieba.load_userdict("../Files/user_dict.txt") # 加载自定义分词词典

seg_list1 = jieba.cut("今天很高兴在慕课网和大家交流学习")
print('\n\n加载自定义分词词典：\n'+"/ ".join(seg_list1))


print('='*40)
print('3. 关键词提取')
print('-'*40)
print(' TF-IDF')
print('-'*40)

'''
extract_tags(sentence, topK=20, withWeight=False, allowPOS=())
sentence 为待提取的文本
topK 为返回几个 TF/IDF 权重最大的关键词，默认值为 20
withWeight 为是否一并返回关键词权重值，默认值为 False
allowPOS 仅包括指定词性的词，默认值为空，即不筛选
jieba.analyse.TFIDF(idf_path=None) 新建 TFIDF 实例，idf_path 为 IDF 频率文件
'''
s = "此外，公司拟对全资子公司吉林欧亚置业有限公司增资4.3亿元，增资后，吉林欧亚置业注册资本由7000万元增加到5亿元。吉林欧亚置业主要经营范围为房地产开发及百货零售等业务。目前在建吉林欧亚城市商业综合体项目。2013年，实现营业收入0万元，实现净利润-139.13万元。"
for x, w in jieba.analyse.extract_tags(s,10, withWeight=True):
    print('%s %s' % (x, w))

print('-'*40)
print(' TextRank')
print('-'*40)


# textrank(sentence, topK=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')) 直接使用，接口相同，注意默认过滤词性。

for x, w in jieba.analyse.textrank(s, 10,withWeight=True):
    print('%s %s' % (x, w))


print('='*40)
print('4. 词性标注')
print('-'*40)

words = jieba.posseg.cut("我爱北京天安门")
for word, flag in words:
    print('%s %s' % (word, flag))

print('='*40)
print('6. Tokenize: 返回词语在原文的起止位置')
print('-'*40)
print(' 默认模式')
print('-'*40)

result = jieba.tokenize('永和服装饰品有限公司')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))

print('-'*40)
print(' 搜索模式')
print('-'*40)

result = jieba.tokenize('永和服装饰品有限公司', mode='search')
for tk in result:
    print("word %s\t\t start: %d \t\t end:%d" % (tk[0],tk[1],tk[2]))