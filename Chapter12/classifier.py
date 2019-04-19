# coding:utf8

"""
Description:测试分类效果
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,re,time,jieba
import numpy as np
import pickle as pkl
from gensim import corpora, models
from sklearn import metrics
from scipy.sparse import csr_matrix

import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot





#############################高效遍历文件######################################
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





###########################分词并去除停用词#####################################
'''
str_doc  参数值 待处理的字符串，数据类型为string
word_list 返回值 返回分词并进行数据清洗后的结果 数据类型是list
'''
def seg_doc(str_doc):
    sent_list = str_doc.split('\n')
    sent_list = map(textParse, sent_list)  # 去掉一些字符，例如\u3000
    stwlist = get_stop_words()
    word_2dlist = [rm_tokens(jieba.cut(part),stwlist) for part in sent_list]  # 分词
    word_list = sum(word_2dlist, [])
    return word_list

def textParse(str_doc):
    str_doc = re.sub('\u3000', '', str_doc)
    return str_doc

def get_stop_words(path=r'../Files/NLPIR_stopwords.txt'):
    file = open(path, 'r',encoding='utf-8').read().split('\n')
    return set(file)


# 去掉一些停用词和数字
'''
words 单行数据分词的结果，数据类型list
stwlist 停用词列表，数据类型list
'''
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





####################数据预处理过程#########################################
# ******************预处理阶段1：生成词典*****************
'''
path_doc_root：存放训练数据的根路径
path_dictionary： 存放中间输出结果的根路径（为第二阶段使用）
'''
def GeneDict(path_doc_root,path_dictionary):
    # 数据预处理阶段1：生成词典并去掉低率项，如果词典不存在则重新生成。反之跳过该阶段
    print('=== 未检测到有词典存在，开始遍历生成词典 ===')
    dictionary = corpora.Dictionary()
    files = loadFiles(path_doc_root)
    for i, msg in enumerate(files):
        if i % n == 0:
            catg = msg[0]
            content = seg_doc(msg[1]) # 对文本内容分词处理
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


# ******************预处理阶段2：生成TFIDF*****************
'''
path_doc_root：存放训练数据的根路径
path_dictionary：存放中间输出结果的根路径
path_tmp_tfidf： 存档TF-IDF特征向量的目录（为第三阶段使用）
'''
def GeneTFIDF(path_doc_root,path_dictionary,path_tmp_tfidf):
    print('=== 未检测到有tfidf文件夹存在，开始生成tfidf向量 ===')
    dictionary = corpora.Dictionary.load(path_dictionary)
    os.makedirs(path_tmp_tfidf)
    files = loadFiles(path_doc_root)
    tfidf_model = models.TfidfModel(dictionary=dictionary)
    corpus_tfidf = {}
    for i, msg in enumerate(files):
        if i % n == 0:
            catg = msg[0]
            word_list = seg_doc(msg[1])
            file_bow = dictionary.doc2bow(word_list)
            file_tfidf = tfidf_model[file_bow]
            tmp = corpus_tfidf.get(catg, [])
            tmp.append(file_tfidf)
            if tmp.__len__() == 1:
                corpus_tfidf[catg] = tmp
        if i % 5000 == 0:
            print('{t} *** {i} \t docs has been dealed'.format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    # 将tfidf中间结果储存起来
    catgs = list(corpus_tfidf.keys())
    for catg in catgs:
        corpora.MmCorpus.serialize('{f}{s}{c}.mm'.format(f=path_tmp_tfidf, s=os.sep, c=catg),corpus_tfidf.get(catg),id2word=dictionary )
        print('catg {c} has been transformed into tfidf vector'.format(c=catg))
    print('=== tfidf向量已经生成 ===')


# ******************预处理阶段3：TFIDF向量模型生成LSI主题模型*****************
'''
num_topics： 设置保存权重最大的前N个数据特征，默认300
path_tmp_tfidf：存档TF-IDF特征向量的目录
path_tmp_lsimodel： lsi模型保存路径 （为使用）
'''
def GeneLSI(path_dictionary,path_tmp_tfidf,path_tmp_lsimodel,path_tmp_lsi,num_topics=300):
    print('=== 未检测到有lsi文件夹存在，开始生成lsi向量 ===')
    dictionary = corpora.Dictionary.load(path_dictionary)
    # 从对应文件夹中读取所有类别
    catg_list = []
    for file in  os.listdir(path_tmp_tfidf):
        t = file.split('.')[0]
        if t not in catg_list:
            catg_list.append(t)

    # 从磁盘中读取corpus
    corpus_tfidf = {}
    for catg in catg_list:
        path = '{f}{s}{c}.mm'.format(f=path_tmp_tfidf, s=os.sep, c=catg)
        corpus = corpora.MmCorpus(path)
        corpus_tfidf[catg] = corpus
    print('tfidf文档读取完毕，开始转化成lsi向量 ...')

    # 生成lsi model
    corpus_tfidf_total = []
    for catg in list(corpus_tfidf.keys()):
        tmp = corpus_tfidf.get(catg)
        corpus_tfidf_total += tmp
    lsi_model = models.LsiModel(corpus=corpus_tfidf_total, id2word=dictionary, num_topics=num_topics)

    # 将lsi模型存储到磁盘上
    lsi_file = open(path_tmp_lsimodel, 'wb')
    pkl.dump(lsi_model, lsi_file)
    lsi_file.close()
    del corpus_tfidf_total # lsi model已经生成，释放变量空间
    print('--- lsi模型已经生成 ---')

    # 生成corpus of lsi, 并逐步去掉 corpus of tfidf
    corpus_lsi = {}
    for catg in list(corpus_tfidf.keys()):
        corpu = [lsi_model[doc] for doc in corpus_tfidf.get(catg)]
        corpus_lsi[catg] = corpu
        corpus_tfidf.pop(catg)
        corpora.MmCorpus.serialize('{f}{s}{c}.mm'.format(f=path_tmp_lsi, s=os.sep, c=catg),corpu,id2word=dictionary)
    print('=== lsi向量已经生成 ===')





#######################生成分类器阶段######################################
'''
path_tmp_lsi 各类主题mm保存的父目录
path_tmp_predictor： 分类器模型保存路径
train_test_ratio: 训练集与测试集划分比例，默认70%训练集和30%测试集
'''
def GeneClassifier(path_tmp_lsi,path_tmp_predictor,train_test_ratio=0.7):
    print('=== 未检测到分类器存在，开始进行分类过程 ===')
    print('--- 未检测到lsi文档，开始从磁盘中读取 ---')
    catg_list = []
    for file in os.listdir(path_tmp_lsi):
        t = file.split('.')[0]
        if t not in catg_list:
            catg_list.append(t)

    # 从磁盘中读取corpus
    corpus_lsi = {}
    for catg in catg_list:
        path = '{f}{s}{c}.mm'.format(f=path_tmp_lsi, s=os.sep, c=catg)
        corpus = corpora.MmCorpus(path)
        corpus_lsi[catg] = corpus
    print('--- lsi文档读取完毕，开始进行分类 ---')
    # 类别标签、文档数、 语料主题
    tag_list,doc_num_list,corpus_lsi_total = [],[],[]
    for count, catg in enumerate(catg_list):
        tmp = corpus_lsi[catg]
        tag_list += [count]*tmp.__len__()
        doc_num_list.append(tmp.__len__())
        corpus_lsi_total += tmp
        corpus_lsi.pop(catg)
    print("文档类别数目:", len(doc_num_list))
    # 将gensim中的mm表示转化成numpy矩阵表示
    print("LSI语料总大小:", len(corpus_lsi_total))

    data,rows,cols = [], [] , []
    line_count = 0
    for line in corpus_lsi_total:
        for elem in line:
            rows.append(line_count)
            cols.append(elem[0])
            data.append(elem[1])
        line_count += 1
    lsi_matrix = csr_matrix((data, (rows, cols))).toarray()
    print("LSI矩阵规模:", lsi_matrix.shape)
    print("数据样本数目:", line_count)
    # 生成训练集和测试集
    rarray = np.random.random(size=line_count)
    train_set,train_tag,test_set,test_tag = [],[],[],[]
    for i in range(line_count):
        if rarray[i] < train_test_ratio:
            train_set.append(lsi_matrix[i, :])
            train_tag.append(tag_list[i])
        else:
            test_set.append(lsi_matrix[i, :])
            test_tag.append(tag_list[i])
    # 生成分类器
    predictor = xgboost_multi_classify(train_set, test_set,train_tag, test_tag)
    x = open(path_tmp_predictor, 'wb')
    pkl.dump(predictor, x)
    x.close()


'''
x_train 训练集样本
x_test  训练集标签
y_train 测试集样本
y_test  测试集标签
train_test_ratio： 训练集与测试集划分比例
'''
#*********************xgboost训练分类模型************************
def xgboost_multi_classify(train_set, test_set,train_tag, test_tag):
    # 统计信息
    print("训练集大小:", len(train_tag), " 测试集大小:", len(test_tag))
    train_info = {k: train_tag.count(k) for k in train_tag}
    print("训练集类别对应的样本数:", train_info)
    test_info = {k: test_tag.count(k) for k in test_tag}
    print("测试集类别对应的样本数", test_info)

    # XGBoost
    data_train = xgb.DMatrix(train_set, label=train_tag)
    data_test = xgb.DMatrix(test_set, label=test_tag)
    watch_list = [(data_test, 'eval'), (data_train, 'train')]
    param = {
        'objective': 'multi:softmax',  # 多分类的问题
        'num_class': 6 ,# 类别数，与 multisoftmax 并用
        'max_depth': 8,  # 构建树的深度，越大越容易过拟合
        'eta': 0.3, # 如同学习率
        'eval_metric': 'merror',
        'silent': 1,   # 设置成1则没有运行信息输出，最好是设置为0.
        'subsample': 0.9, # 随机采样训练样本
    }  # 参数
    xgb_model = xgb.train(param, data_train, num_boost_round=250, evals=watch_list) # num_boost_round控制迭代次数
    y_hat = xgb_model.predict(data_test)
    validateModel(test_tag, y_hat)
    return xgb_model

    # 显示重要特征
    # plot_importance(xgb_model[20])
    # pyplot.show()


#*********************xgboost分类结果验证************************
'''
y_true 文本对应的正确类别
y_pred 分类器预测的类别
'''
def validateModel(y_true, y_pred):
    classify_report = metrics.classification_report(y_true, y_pred)
    confusion_matrix = metrics.confusion_matrix(y_true, y_pred)
    overall_accuracy = metrics.accuracy_score(y_true, y_pred)
    acc_for_each_class = metrics.precision_score(y_true, y_pred, average=None)
    average_accuracy = np.mean(acc_for_each_class)
    score = metrics.accuracy_score(y_true, y_pred)
    print('classify_report : \n', classify_report)
    print('confusion_matrix : \n', confusion_matrix)
    print('acc_for_each_class : \n', acc_for_each_class)
    print('average_accuracy: {0:f}'.format(average_accuracy))
    print('overall_accuracy: {0:f}'.format(overall_accuracy))
    print('score: {0:f}'.format(score))





#######################新闻文本进行分类######################################
'''
demo_doc 待分类的新闻文本
path_dictionary 训练好的词典模型存储路径
path_tmp_lsimodel 训练好的主题模型存放路径
path_tmp_predictor: 训练的的分类器模型存储路径
path_tmp_lsi 各类主题mm存放路径
'''
def TestClassifier(demo_doc,path_dictionary,path_tmp_lsimodel,path_tmp_predictor,path_tmp_lsi):
    # 1 文本数据预处理,分词并转化为TF-IDF向量
    dictionary = corpora.Dictionary.load(path_dictionary) # 加载词典
    demo_bow = dictionary.doc2bow(list(jieba.cut(demo_doc, cut_all=False)))
    tfidf_model = models.TfidfModel(dictionary=dictionary)
    demo_tfidf = tfidf_model[demo_bow]

    # 2 文本转化主题模型
    lsi_file = open(path_tmp_lsimodel, 'rb')
    lsi_model = pkl.load(lsi_file)
    lsi_file.close()
    demo_lsi = lsi_model[demo_tfidf]

    # 3 主题mm类型数据表示成numpy矩阵
    data,cols,rows = [],[],[]
    for item in demo_lsi:
        data.append(item[1])
        cols.append(item[0])
        rows.append(0)
    demo_matrix = csr_matrix((data, (rows, cols))).toarray()

    # 4 加载分类器
    x = open(path_tmp_predictor, 'rb')
    predictor = pkl.load(x)
    x.close()
    DMatrix = xgb.DMatrix(demo_matrix)
    y_hat = predictor.predict(DMatrix)

    # 5 获取所有类别
    catg_list = []
    for file in  os.listdir(path_tmp_lsi):
        t = file.split('.')[0]
        if t not in catg_list:
            catg_list.append(t)

    print('\n分类结果为：',catg_list[int(y_hat[0])])





#########################模型训练过程###########################################
def GeneModel():
    path_doc_root = '../Corpus/CSCMNews' # 根目录 即存放按类分类好的文本数据集
    path_tmp = '../Corpus/CSCMNews_model' # 存放中间结果的位置
    # 数据预处理阶段1：生成词典并去掉低率项，如果词典不存在则重新生成。反之跳过该阶段
    path_dictionary = os.path.join(path_tmp, 'CSCMNews.dict') # 词典路径
    if os.path.exists(path_dictionary):
        print('=== 检测到词典已生成，跳过数据预处理阶段1 ===')
    else:
        os.makedirs(path_tmp) #创建中间结果保存路径
        GeneDict(path_doc_root,path_dictionary)


    # 数据预处理阶段2：开始将文档转化成tfidf
    path_tmp_tfidf = os.path.join(path_tmp, 'tfidf_corpus') # tfidf存储路径
    if os.path.exists(path_tmp_tfidf):
        print('=== 检测到tfidf向量已经生成，跳过数据预处理阶段2 ===')
    else:
        GeneTFIDF(path_doc_root,path_dictionary,path_tmp_tfidf)


    # 数据预处理阶段3：TFIDF向量模型生成LSI主题模型
    num_topics = 300  # 特征维度
    train_test_ratio = 0.7  # 训练集和测试集比率
    param = str(n)+'_'+str(num_topics)+'_'+str(train_test_ratio)
    # 存放中间结果的位置
    path_tmp = os.path.join(path_tmp, param)
    path_tmp_lsi = os.path.join(path_tmp, 'lsi_corpus_'+param)
    # lsi模型保存路径
    path_tmp_lsimodel = os.path.join(path_tmp, 'lsi_model_'+param+'.pkl')
    if os.path.exists(path_tmp_lsi):
        print('=== 检测到LSI主题模型已经生成，跳过数据预处理阶段3 ===')
    else:
        os.makedirs(path_tmp_lsi)
        GeneLSI(path_dictionary,path_tmp_tfidf,path_tmp_lsimodel,path_tmp_lsi,num_topics)


    # 生成分类器阶段：xgboost训练分类模型
    path_tmp_predictor = os.path.join(path_tmp, 'predictor_'+param+'.pkl')
    print("\n特征维度:",num_topics, "\n训练集和测试集划分比率:", train_test_ratio)
    if os.path.exists(path_tmp_predictor):
        print('=== 检测到分类器已经生成，跳过生成分类器阶段 ===')
    else:
        GeneClassifier(path_tmp_lsi,path_tmp_predictor,train_test_ratio)

    return path_dictionary,path_tmp_lsi, path_tmp_lsimodel,path_tmp_predictor


########################主函数#############################################

n = 5 # n 表示抽样率
if __name__ == '__main__':
    print('Start....{t}'.format(t=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
    print('\n\n\n',"*"*15,'分类器训练过程',"*"*15)
    # 模型训练过程
    path_dictionary,path_tmp_lsi, path_tmp_lsimodel,path_tmp_predictor = GeneModel()
    print("*"*15,'分类器训练结束',"*"*15,'\n\n\n\n\n')


    print("*"*15,'分类开始',"*"*15)
    demo_doc = """这次大选让两党的精英都摸不着头脑。以媒体专家的传统观点来看，要选总统首先要避免失言，避免说出一些“offensive”的话。希拉里，罗姆尼，都是按这个方法操作的。罗姆尼上次的47%言论是在一个私人场合被偷录下来的，不是他有意公开发表的。今年希拉里更是从来没有召开过新闻发布会。川普这种肆无忌惮的发言方式，在传统观点看来等于自杀。 '腾讯娱乐讯 热播都市剧《欢乐颂 2》截至目前故事已接近尾声。可就在最近，《欢乐颂 2》全集盗版资源在网络上被肆意散布传播。对此今日下午，《欢乐颂 2》主要出品方 "正午阳光影业 " 在官微上正式发出声明做出回应，称 "将对侵权信息的发布者、传播者将不遗余力追查到源头，绝不姑息！针对侵权行为，不排除后续提起民事诉讼等一切必要的法律行动。"然而有趣的是，针对该份声明大部分网友都表示 " 盗版可耻，支持维权 "，还有一部分看完《欢乐颂 2》未删减版（送审版）的网友表示 " 某些戏删减得太多了 "，关注点很别出心裁。"""

    demo_doc2 = """2019年第8期《求是》杂志发表习近平的重要文章《一个国家、一个民族不能没有灵魂》。这是习近平2019年3月4日在参加全国政协十三届二次会议文化艺术界、社会科学界委员联组会时的讲话。在讲话中，他对文化文艺工作者、哲学社会科学工作者提出了四点希望：希望大家坚持与时代同步伐、希望大家坚持以人民为中心、希望大家坚持以精品奉献人民、希望大家坚持用明德引领风尚。
“首先要搞清楚为谁创作、为谁立言的问题”、“大师、大家，不是说有大派头，而是说要有大作品”、“在市场经济大潮面前自尊自重、自珍自爱”……习近平这7段话语重心长，值得认真读一读。"""

    print("未知文本类别内容为：\n\n",demo_doc2,'\n')
    TestClassifier(demo_doc2,path_dictionary,path_tmp_lsimodel,path_tmp_predictor,path_tmp_lsi)
    print("*"*15,'分类结束',"*"*15,'\n\n\n')


    print('End......{t}'.format(t=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))