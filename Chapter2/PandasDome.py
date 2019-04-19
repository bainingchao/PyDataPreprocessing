# coding:utf8

"""
DESC: Python数据预处理之Pandas教程
Author：伏草惟存
Prompt: code in Python3 env
"""


'''
系列(Series)是能够保存任何类型的数据(整数，字符串，浮点数，Python对象等)的一维标记数组。轴标签统称为索引。
'''


#************1 Pandas 数据结构*******************
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# 1 系列 Series
# pandas.Series( data, index, dtype, copy)。
#  data ：如 ndarray，list，constants
#  index   索引唯一与数据的长度相同。
#  dtype   dtype用于数据类型。
#  copy    复制数据，默认为false。

data = np.array(['a','b','c','d'])
index=[100,101,102,103]
obj = pd.Series(data,index)
print(obj)
'''
运行结果：
100    a
101    b
102    c
103    d
dtype: object
'''

# 2 数据帧 DataFrame
# pandas.DataFrame( data, index, columns, dtype, copy)
# data :如:ndarray，series，map，lists，dict，constant和另一个DataFrame。

data = {'Name':['Tom', 'Jack', 'Steve', 'Ricky'],'Age':[28,34,29,42]}
df = pd.DataFrame(data, index=['rank1','rank2','rank3','rank4'],dtype=float)
print(df[:2])
'''
       Name   Age
rank1   Tom  28.0
rank2  Jack  34.0
'''

# 3 面板 Panel:是3D容器的数据。
# axis 0:items，每个项目对应于内部包含的数据帧(DataFrame)。
# axis 1:major_axis ，每个数据帧(DataFrame)的索引(行)。
# axis 2:minor_axis ，它是每个数据帧(DataFrame)的列。
# pandas.Panel(data, items, major_axis, minor_axis, dtype, copy)
# items : axis=0
# major_axis : axis=1
# minor_axis : axis=2

data = {'Item1' : pd.DataFrame(np.random.randn(4, 3)),
        'Item2' : pd.DataFrame(np.random.randn(4, 2))}
p = pd.Panel(data)
print( p['Item1'])
# print( p.major_xs(1))
'''
运行结果：
          0         1         2
0 -1.586204  0.425280 -2.190339
1  1.456369 -1.974917  0.740831
2 -1.299986 -0.831230 -1.328189
3  1.013347  0.963660 -0.178311
'''


#************2 Pandas 数据统计*******************

import pandas as pd
import numpy as np

#Create a Dictionary of series
d = {'Name':pd.Series(['Tom','James','Ricky','Vin','Steve','Minsu','Jack',
   'Lee','David','Gasper','Betina','Andres']),
   'Age':pd.Series([25,26,25,23,30,29,23,34,40,30,51,46]),
   'Rating':pd.Series([4.23,3.24,3.98,2.56,3.20,4.6,3.8,3.78,2.98,4.80,4.10,3.65])}
df = pd.DataFrame(d)
print(df)
'''
      Name  Age  Rating
0      Tom   25    4.23
1    James   26    3.24
2    Ricky   25    3.98
3      Vin   23    2.56
4    Steve   30    3.20
5    Minsu   29    4.60
6     Jack   23    3.80
7      Lee   34    3.78
8    David   40    2.98
9   Gasper   30    4.80
10  Betina   51    4.10
11  Andres   46    3.65
'''

# 统计数据之和
print('数据之和:\n',df.sum())
# 统计数据的均值
print('数据的均值:\n',df.mean())
# 统计数据的标准偏差
print('数据的标准偏差:\n',df.std())

'''
count() 非空观测数量
sum()   所有值之和
mean()  所有值的平均值
median()    所有值的中位数
mode()  值的模值
std()   值的标准偏差
min()   所有值中的最小值
max()   所有值中的最大值
abs()   绝对值
prod()  数组元素的乘积
cumsum()    累计总和
cumprod()   累计乘积
'''


# pct_change()函数:DatFrames和Panel都有pct_change()函数。此函数将每个元素与其前一个元素进行比较，并计算变化百分比。

s = pd.Series([1,2,3,4,5,4])
print (s.pct_change())

# 协方差:DataFrame时，协方差方法计算所有列之间的协方差(cov)值。
frame = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
print (frame['a'].cov(frame['b']))
print (frame.cov())


# 相关性:相关性显示了任何两个数值(系列)之间的线性关系。
frame = pd.DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])

print (frame['a'].corr(frame['b']))
print (frame.corr())



#************3 Pandas 处理丢失值*******************
# 机器学习和数据挖掘等领域由于数据缺失导致的数据质量差，
# 在模型预测的准确性上面临着严重的问题。

import pandas as pd
import numpy as np

# 重构缺失值
# 使用重构索引(reindexing)，创建了一个缺少值的DataFrame。 在输出中，NaN表示不是数字的值
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print (df)

# 检查缺失值:Pandas提供isnull()和notnull()函数，它们也是Series和DataFrame对象的方法
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print (df.isnull())
# print (df['one'].notnull())


# 缺少数据的计算
# 在求和数据时，NA将被视为0.如果数据全部是NA，那么结果将是NA
# df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
# 'h'],columns=['one', 'two', 'three'])
# df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
# # print(df['one'])
# print (df['one'].sum())


# 清理/填充缺少数据
# 1 用标量值替换NaN:0替换NaN
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print ("NaN replaced with '0':")
print (df.fillna(0))


# 2 填写NA前进和后退:pad/fill 填充方法向前 和 bfill/backfill  填充方法向后

df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print (df.fillna(method='pad'))
# print (df.fillna(method='backfill'))

# 3 丢失缺少的值：axis=0在行上应用，axis=1在列上应用
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print (df.dropna(axis=0))


# 4 替换丢失(或)通用值
df = pd.DataFrame({'one':[10,20,30,40,50,2000],
'two':[1000,0,30,40,50,60]})
print (df.replace({1000:10,2000:60}))

# 5 处理无效值
df = pd.DataFrame({'one':[10,20,np.nan,40,50,2000],
'two':[1000,0,30,np.nan,50,60]})
print("df:\n{}\n".format(pd.isna(df)))

# 6 忽略无效值
df = pd.DataFrame(np.random.randn(5, 3), index=['a', 'c', 'e', 'f',
'h'],columns=['one', 'two', 'three'])
df = df.reindex(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
print("df.dropna():\n{}\n".format(df.dropna()))


#************4 Pandas 稀疏数据*******************
# 当任何匹配特定值的数据(NaN/缺失值或任何值)被省略时，稀疏对象被“压缩”。

import pandas as pd
import numpy as np

# 稀疏数据处理
df = pd.DataFrame(np.random.randn(10000, 4))
df.ix[:9998] = np.nan
sdf = df.to_sparse()
 # 通过调用to_dense标准密集
print (sdf.to_dense())
 # 稀疏率
print ('稀疏率：\n',sdf.density)


# 稀疏Dtypes
s = pd.Series([1, np.nan, np.nan])
print (s)
print ("=============================")
s.to_sparse()
print (s)




#************5 Pandas 可视化*******************
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 折线图

df = pd.DataFrame(np.random.randn(10,4),index=pd.date_range('2019/2/27',
   periods=10), columns=list('ABCD'))
df.plot()
plt.show()

# 条形图
df = pd.DataFrame(np.random.rand(10,4),columns=['a','b','c','d'])
df.plot.bar()
plt.show()


# 堆积条形图
df = pd.DataFrame(np.random.rand(10,4),columns=['a','b','c','d'])
df.plot.bar(stacked=True)
plt.show()

# 水平条形图
df = pd.DataFrame(np.random.rand(10,4),columns=['a','b','c','d'])
df.plot.barh(stacked=True)
plt.show()

# 直方图
df = pd.DataFrame({'a':np.random.randn(1000)+1,'b':np.random.randn(1000),'c':
np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
df.plot.hist(bins=20)
plt.show()


# 多个直方图
df=pd.DataFrame({'a':np.random.randn(1000)+1,'b':np.random.randn(1000),'c':
np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
df.hist(bins=20)
plt.show()

# 箱形图
df = pd.DataFrame(np.random.rand(10, 5), columns=['A', 'B', 'C', 'D', 'E'])
df.plot.box()
plt.show()

# 区域块图形
df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
df.plot.area()
plt.show()

# 散点图形
df = pd.DataFrame(np.random.rand(50, 4), columns=['a', 'b', 'c', 'd'])
df.plot.scatter(x='a', y='b')
plt.show()

# 饼状图
df = pd.DataFrame(3 * np.random.rand(4), index=['A', 'B', 'C', 'D'], columns=['x'])
df.plot.pie(subplots=True)
plt.show()



#************6 Pandas 文件操作*******************
# pandas库提供了一系列的read_函数来读取各种格式的文件，它们如下所示：
# read_csv
# read_table
# read_fwf
# read_clipboard
# read_excel
# read_hdf
# read_html
# read_json
# read_msgpack
# read_pickle
# read_sas
# read_sql
# read_stata
# read_feather
import pandas as pd
import numpy as np


# 读取Excel文件  pip install xlrd
df1 = pd.read_excel("data/test1.xlsx")
print("df1:\n{}\n".format(df1))

# 读取CSV文件
df2 = pd.read_csv("data/test2.csv", sep=",")
print("df2:\n{}\n".format(df2))


# 转存JSON文件
df = pd.DataFrame([['a', 'b'], ['c', 'd']],index=['row 1', 'row 2'],columns=['col 1', 'col 2'])
data_json=df.to_json(orient='columns')
print('JSON文件\n',data_json)

# 读取json文件
df3 = pd.read_json("data/test3.json")
print("\ndf3:\n{}\n".format(df2))