# coding:utf8
import re

"""
DESC:  处理文本的HTML标签、特殊符号
Author：伏草惟存
Prompt: code in Python3 env
"""


# 清洗HTML标签文本
# @param htmlstr HTML字符串.
def filter_tags(htmlstr):
    # 过滤DOCTYPE
    htmlstr = ' '.join(htmlstr.split()) # 去掉多余的空格
    re_doctype = re.compile(r'<!DOCTYPE .*?> ', re.S)
    s = re_doctype.sub('',htmlstr)

    # 过滤CDATA
    re_cdata = re.compile('//<!CDATA\[[ >]∗ //\] > ', re.I)
    s = re_cdata.sub('', s)

    # Script
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    s = re_script.sub('', s)  # 去掉SCRIPT

    # style
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    s = re_style.sub('', s)  # 去掉style

    # 处理换行
    re_br = re.compile('<br\s*?/?>')
    s = re_br.sub('', s)     # 将br转换为换行

    # HTML标签
    re_h = re.compile('</?\w+[^>]*>')
    s = re_h.sub('', s)  # 去掉HTML 标签

    # HTML注释
    re_comment = re.compile('<!--[^>]*-->')
    s = re_comment.sub('', s)

    # 多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('', s)

    blank_line_l = re.compile('\n')
    s = blank_line_l.sub('', s)

    blank_kon = re.compile('\t')
    s = blank_kon.sub('', s)

    blank_one = re.compile('\r\n')
    s = blank_one.sub('', s)

    blank_two = re.compile('\r')
    s = blank_two.sub('', s)

    blank_three = re.compile(' ')
    s = blank_three.sub('', s)

    # 剔除超链接
    http_link = re.compile(r'(http://.+.html)')
    s = http_link.sub('', s)
    return s



def readTxt(path):
    res = ''
    with open(path,'r',encoding='utf-8') as f:
        res = f.read()
    return res


if __name__=='__main__':
    str_doc = readTxt(r'../Files/htmldome.txt')
    s=filter_tags(str_doc)
    print(s)
