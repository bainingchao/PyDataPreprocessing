# coding:utf8

"""
Description:matplotlib绘制复杂图
Author：伏草惟存
Prompt: code in Python3 env
"""

import matplotlib
import matplotlib.pyplot as plt
import csv
from datetime import datetime
#加入中文显示
import  matplotlib.font_manager as fm
# 解决中文乱码，本案例使用宋体字
myfont=fm.FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc")



def temper_char():
    fig = plt.figure()   # 将画布划分为1行1列1块
    dates,highs,lows = [],[],[]
    with open(r'./weather07.csv') as f:
        reader = csv.reader(f)
        header_row = next(reader) # 返回文件第一行
        for row in reader:
            current_date = datetime.strptime(row[0],"%Y-%m-%d")
            dates.append(current_date)
            highs.append(int(row[1]))
            lows.append((int(row[3])))


    # 接收数据并绘制图形,facecolor填充区域颜色
    plt.plot(dates,highs,c='red',linewidth=2,alpha=0.5)
    plt.plot(dates,lows,c='green',linewidth=2,alpha=0.5)
    plt.fill_between(dates,highs,lows,facecolor='blue',alpha=0.2)

    # 设置散点图标题和横纵坐标标题
    plt.title("日常最高气温，2018年7月",fontsize=10,fontname='宋体',fontproperties=myfont)
    plt.xlabel('横坐标',fontsize=10,fontname='宋体',fontproperties=myfont)
    plt.ylabel('温度',fontsize=10,fontname='宋体',fontproperties=myfont)

    # 绘制斜的日期
    fig.autofmt_xdate()

    # 设置刻度标记大小,axis='both'参数影响横纵坐标，labelsize刻度大小
    plt.tick_params(axis='both',which='major',labelsize=8)

    # 显示图形
    plt.show()



if __name__ == '__main__':
    xvalues = list(range(1,100)) #校正坐标点，即横坐标值列表
    yvalues = [x**2 for x in xvalues] # 纵坐标值列表

    x_result = [1,2,3,4,5,6]
    y_frequencies = [152,171,175,168,150,179]

    temper_char()
