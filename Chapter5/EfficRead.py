# coding:utf-8

"""
DESC:   在文本预处理中，实现高效的读取文本文件
Author：伏草惟存
Prompt: code in Python3 env
"""

import os,time


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
                yield catg, file



if __name__=='__main__':
    start = time.time()

    filepath = os.path.abspath(r'../Corpus/CSCMNews')
    files = loadFiles(filepath)
    for i, msg in enumerate(files):
        if i%5000 == 0:
            print('{t} *** {i} \t docs has been Read'.format(i=i, t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))

    end = time.time()
    print('total spent times:%.2f' % (end-start)+ ' s')






