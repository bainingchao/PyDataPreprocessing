# coding:utf8

"""
Description:matplotlib绘制散点图
Author：伏草惟存
Prompt: code in Python3 env
"""


'''
散点图定义：
散点图也叫 X-Y 图，它将所有的数据以点的形式展现在直角坐标系上，以显示变量之 间的相互影响程度，点的位置由变量的数值决定。
通过观察散点图上数据点的分布情况，我们可以推断出变量间的相关性。如果变量之间 不存在相互关系，那么在散点图上就会表现为随机分布的离散的点，如果存在某种相关性， 那么大部分的数据点就会相对密集并以某种趋势呈现。数据的相关关系主要分为：正相关 （两个变量值同时增长）、负相关（一个变量值增加另一个变量值下降）、不相关、线性相关、 指数相关等。那些离点集群较远的点称为离群点或者异常点。
散点图经常与回归线（就是最准确地贯穿所有点的线）结合使用，归纳分析现有数据以 进行预测分析。

散点图的特点：
散点图通常用于显示和比较数值。不仅可以显示趋势，还能显示数据集群的形状，以及 在数据云团中各数据点的关系。

散点图应用场景：
男女身高和体重的例子来展示上述所描述的散点图的功能。

'''


import matplotlib
import matplotlib.pyplot as plt

#加入中文显示
import  matplotlib.font_manager as fm
# 解决中文乱码，本案例使用宋体字
myfont=fm.FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc")


def scatter_chart(xvalues,yvalues):
    # 绘制散点图，s设置点的大小,c数据点的颜色，edgecolors数据点的轮廓
    plt.scatter(xvalues,yvalues,c='green',edgecolors='none',s=20)

    # 设置散点图标题和横纵坐标标题
    plt.title("Python绘制折线图",fontsize=30,fontname='宋体',fontproperties=myfont)
    plt.xlabel('横坐标',fontsize=20,fontname='宋体',fontproperties=myfont)
    plt.ylabel('纵坐标',fontsize=20,fontname='宋体',fontproperties=myfont)

    # 设置刻度标记大小,axis='both'参数影响横纵坐标，labelsize刻度大小
    plt.tick_params(axis='both',which='major',labelsize=10)

    # 设置每个坐标轴取值范围
    plt.axis([80,100,6400,10000])

    # 显示图形
    plt.show()

    # 自动保存图表,bbox_inches剪除图片空白区
    # plt.savefig('squares_plot.png',bbox_inches='tight')


if __name__ == '__main__':
    xvalues = list(range(1,100)) #校正坐标点，即横坐标值列表
    yvalues = [x**2 for x in xvalues] # 纵坐标值列表

    x_result = [1,2,3,4,5,6]
    y_frequencies = [152,171,175,168,150,179]

    scatter_chart(xvalues,yvalues)
