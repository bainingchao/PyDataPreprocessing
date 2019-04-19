# coding=utf-8

"""
DESC:  批量文档格式自动转化txt
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,time

'''
功能描述：遍历目录，对子文件单独处理
'''
# 2 遍历目录文件
def TraversalDir(rootDir):
    # 返回指定目录包含的文件或文件夹的名字的列表
    for i,lists in enumerate(os.listdir(rootDir)):
        # 待处理文件夹名字集合
        path = os.path.join(rootDir, lists)
        # 核心算法，对文件具体操作
        if os.path.isfile(path):
            if i%5000 == 0:
                print('{t} *** {i} \t docs has been read'.format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
        # 递归遍历文件目录
        if os.path.isdir(path):
            TraversalDir(path)



if __name__ == '__main__':
    t1=time.time()

    # 根目录文件路径
    rootDir = r"../Corpus/CSCMNews"
    TraversalDir(rootDir)

    t2=time.time()
    print('totally cost %.2f' % (t2-t1)+' s')