# coding:utf-8

"""
DESC:  正则表达式：提取特殊字符
Author：伏草惟存
Prompt: code in Python3 env
"""

import re

# ^ 表示开头
# . 任意字符
# * 任意次数
# $ 结尾
# ? 非贪婪模式，提取第一个字符
# + 至少出现一次
# {1} 出现一次
# {3,} 出现3次以上
# {2,5} 最少2次最多5次
# | 或的关系
# [] 满足任意一个都可以,[2435]任意 [0-9]区间  [^1]非1
# \s 为空格 \S非空格
# \w 匹配[A-Za-z0-9_] \W 反匹配[A-Za-z0-9_]
# [\u4E00-\u9FA5] 汉字的匹配
# \d 匹配数字

line = 'this is a dome about  this  scrapy2.0'
line1 = '这是Scrapy学习课程,这次课程很好'
# line1 = 'xxx出生于1989年'

# regex_str='^t.*0$'
# regex_str=".*?(t.*?t).*" # 提取tt之间的子串
# regex_str="(this\Wis)"
regex_str=".*?([\u4E00-\u9FA5]+课程)"
# regex_str=".*?(\d+)年"
match_obj = re.match(regex_str,line1)
if match_obj:
    print(match_obj.group(1))


'''出生日期的提取'''

# line = '张三出生于1990年10月1日'
# line = '李四出生于1990-10-1'
# line = '王五出生于1990-10-01'
# line = '孙六出生于1990/10/1'
# line = '张七出生于1990-10'

# regex_str='.*出生于(\d{4}[年/-]\d{1,2}([月/-]\d{1,2}|[月/-]$|$))'
# match_obj = re.match(regex_str,line)
# if match_obj:
#     print(match_obj.group(1))



