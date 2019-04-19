# coding:utf8

"""
Description:matplotlib绘制直方图
Author：伏草惟存
Prompt: code in Python3 env
"""

'''
直方图定义：
直方图（英语：Histogram）是一种对数据分布情况的图形表示，是一种二维统计图表，它的两个坐标分别是统计样本和该样本对应的某个属性的度量。

优点：
可以很清晰地看出每个类的总和及各个属性的比例。
缺点：
不容易看出各个属性的频数。

应用场景
适合的场景：
适合应用到分类数据对比。比如一个游戏销量的图表，展示不同游戏类型的销量对比。 不适合的场景：
1 分类太多不适合使用纵向柱状图，如对比不同省份的人口数量。
2 不适合表示趋势。柱状图使用矩形的长度（宽度）来对比分类数据的大小，非常方便 临近的数据进行大小的对比，不适合展示连续数据的趋势。

'''


import matplotlib
import matplotlib.pyplot as plt
import pygal # Pygal生成可缩略的矢量图文件

#加入中文显示
import  matplotlib.font_manager as fm
# 解决中文乱码，本案例使用宋体字
myfont=fm.FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc")


def histogram(xvalues,yvalues):
    # 绘制直方图
    hist = pygal.Bar()

    # 设置散点图标题和横纵坐标标题
    hist.title = '事件频率的直方图'
    hist.x_title = '事件的结果'
    hist.y_title = '事件的频率'

    # 绘制气温图,设置图形大小
    fig = plt.figure(dpi=100,figsize=(10,6))

    # 事件的结果
    hist.x_labels = xvalues

    # 事件的统计频率
    hist.add('事件',yvalues)

    # 保存文件路径
    hist.render_to_file('die_visual.svg')

if __name__ == '__main__':
    xvalues = list(range(1,100)) #校正坐标点，即横坐标值列表
    yvalues = [x**2 for x in xvalues] # 纵坐标值列表

    x_result = [1,2,3,4,5,6]
    y_frequencies = [152,171,175,168,150,179]

    histogram(x_result,y_frequencies)
