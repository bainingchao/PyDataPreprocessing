# coding:utf8

"""
Description:matplotlib绘制折线图
Author：伏草惟存
Prompt: code in Python3 env
"""



'''
折线图定义：
折线图用于显示数据在一个连续的时间间隔或者时间跨度上的变化，它的特点是反映 事物随时间或有序类别而变化的趋势。在折线图中，数据是递增还是递减、增减的速率、增 减的规律（周期性、螺旋性等）、峰值等特征都可以清晰地反映出来。所以，折线图常用来 分析数据随时间变化的趋势，也可用来分析多组数据随时间变化的相互作用和相互影响。

折线图应用场景：
适用场景：
1 有序的因变量，比如时间。某监控系统的折线图表，显示了请求次数和响应时间随时 间的变化趋势。
2 不同月份的温度。
不适合的场景：
1 当水平轴的数据类型为无序的分类或者垂直轴的数据类型为连续时间时，不适合使用 折线图。
2 当折线的条数过多时不建议将多条线绘制在一张图上。

'''








import matplotlib
import matplotlib.pyplot as plt
#加入中文显示
import  matplotlib.font_manager as fm

# 解决中文乱码，本案例使用宋体字
myfont=fm.FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc")

def line_chart(xvalues,yvalues):
    # 绘制折线图,c颜色设置，alpha透明度
    plt.plot(xvalues,yvalues,linewidth=5,alpha=0.5,c='red') # num_squares数据值，linewidth设置线条粗细

    # 设置折线图标题和横纵坐标标题
    plt.title("Python绘制折线图",fontsize=20,fontname='宋体',fontproperties=myfont)
    plt.xlabel('横坐标',fontsize=15,fontname='宋体',fontproperties=myfont)
    plt.ylabel('纵坐标',fontsize=15,fontname='宋体',fontproperties=myfont)

    # 设置刻度标记大小,axis='both'参数影响横纵坐标，labelsize刻度大小
    plt.tick_params(axis='both',labelsize=10)

    # 显示图形
    plt.show()



if __name__ == '__main__':
    # xvalues = list(range(1,100)) #校正坐标点，即横坐标值列表
    # yvalues = [x**2 for x in xvalues] # 纵坐标值列表

    x_result = [1,2,3,4,5,6]
    y_frequencies = [152,171,175,168,150,179]

    line_chart(x_result,y_frequencies)
