# coding:utf8

"""
DESC: 实战案例：遍历文件批量抽取新闻文本内容
Author：伏草惟存
Prompt: code in Python3 env
"""

import ExtractTxt as ET
import os,time


'''
功能描述：遍历目录，对子文件单独处理
参数描述：1 rootDir 根目录  2 deffun：方法参数  3 saveDir: 保存路径
'''
class TraversalFun():
    # 1 初始化
    def __init__(self,rootDir,func=None,saveDir=""):
        self.rootDir = rootDir # 目录路径
        self.func = func   # 参数方法
        self.saveDir = saveDir # 保存路径

    # 2 遍历目录文件
    def TraversalDir(self):
        # 切分文件上级目录和文件名
        dirs,latername = os.path.split(self.rootDir)
        # print(rootDir,'\n',dirs,'\n',latername)

        # 保存目录
        save_dir = ""
        if self.saveDir=="": # 默认文件保存路径
            save_dir = os.path.abspath(os.path.join(dirs,'new_'+latername))
        else: save_dir = self.saveDir

        # 创建目录文件
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        print("保存目录：\n"+save_dir)

        # 遍历文件并将其转化txt文件
        TraversalFun.AllFiles(self,self.rootDir,save_dir)


    # 3 递归遍历所有文件，并提供具体文件操作功能
    def AllFiles(self,rootDir,save_dir=''):
        # 返回指定目录包含的文件或文件夹的名字的列表
        for lists in os.listdir(rootDir):
            # 待处理文件夹名字集合
            path = os.path.join(rootDir, lists)

            # 核心算法，对文件具体操作
            if os.path.isfile(path):
                self.func(os.path.abspath(path),os.path.abspath(save_dir))

            # 递归遍历文件目录
            if os.path.isdir(path):
                newpath = os.path.join(save_dir, lists)
                if not os.path.exists(newpath):
                    os.mkdir(newpath)
                TraversalFun.AllFiles(self,path,newpath)




if __name__ == '__main__':
    time_start=time.time()

    # 根目录文件路径
    rootDir = r"../Files/EnPapers"
    # saveDir = r"./Corpus/TxtEnPapers"
    tra=TraversalFun(rootDir,ET.Files2Txt) # 默认方法参数打印所有文件路径
    tra.TraversalDir()
    time_end=time.time()
    print('totally cost',time_end-time_start,'s')