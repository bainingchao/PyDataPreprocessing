#coding=utf-8

"""
DESC:  抽取Word文档文本信息
Author：伏草惟存
Prompt: code in Python3 env
Install package： pip install pypiwin32
"""

# pip安装方式： pip install pypiwin32
# pypiwin32下载地址：https://github.com/mhammond/pywin32/releases


import os,fnmatch
from win32com import client as wc
from win32com.client import Dispatch



'''
功能描述：word文件转存txt文件，默认存储当前路径下；用户可以指定存储文件路径。
参数描述：1 filePath：文件路径   2 savePath： 指定保存路径
'''
def Word2Txt(filePath,savePath=''):
    # 1 切分文件上级目录和文件名
    dirs,filename = os.path.split(filePath)
    # print(dirs,'\n',filename)

    # 2 修改转化后的文件名
    new_name = ''
    if fnmatch.fnmatch(filename,'*.doc'):
        new_name = filename[:-4]+'.txt'
    elif fnmatch.fnmatch(filename,'*.docx'):
        new_name = filename[:-5]+'.txt'
    else: return
    print('->',new_name)

    # 3 文件转化后的保存路径
    if savePath=='': savePath = dirs
    else: savePath = savePath
    word_to_txt = os.path.join(savePath,new_name)
    print('->',word_to_txt)

    # 4 加载处理应用,word转化txt
    wordapp = wc.Dispatch('Word.Application')  # 打开word应用程序
    mytxt = wordapp.Documents.Open(filePath)
    mytxt.SaveAs(word_to_txt,FileFormat = 4) #  4表示提取文本
    mytxt.Close()



if __name__=='__main__':
    filepath = os.path.abspath(r'../Files/wordtotxt/Python数据预处理.docx')
    # savepath = '' # 自定义保存路径
    Word2Txt(filepath)