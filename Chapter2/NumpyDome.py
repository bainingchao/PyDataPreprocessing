# coding:utf8

"""
DESC: Python数据预处理之NumPy教程
Author：伏草惟存
Prompt: code in Python3 env
"""

import numpy as np

#***********1 数组操作********************
# 创建一维数组
arr1 = np.array([1, 2, 3])
print(arr1)
'''结果：
[1 2 3]
'''

 # 创建多维数组
arr2 = np.array([[1, 2], [3, 4],[5, 6]])
print(arr2)


# 数组的维数:维度的数量
print("数组的维数:",arr2.ndim)
'''结果：2'''

# 数组的维度:对于矩阵，n 行 m 列
print("数组的维度",arr2.shape)
'''结果：(3, 2)'''

# 数组元素的总个数，相当于 n*m 的值
print("数组元素总个数",arr2.size)
'''结果：6'''

# ndarray 对象的元素类型
print("元素类型",arr2.dtype)
'''结果：int32'''

# 创建零数组,shape数组形状;dtype数据类型，可选;order	有"C"和"F"两个选项,分别代表，行优先和列优先.
arr3 = np.zeros((2,3), dtype = float, order = 'C')
print(arr3)
'''结果：
[[0. 0. 0.]
 [0. 0. 0.]]
'''

# 创建1数组,shape数组形状;dtype数据类型，可选;order	有"C"和"F"两个选项,分别代表，行优先和列优先.
arr4 = np.ones([2,3], dtype = None, order = 'C')
print(arr4)
'''结果：
[[1. 1. 1.]
 [1. 1. 1.]]
'''

# 从数值范围创建数组,从1开始到10终止，步长为2的浮点型数组
arr5 = np.arange(1,10,2,dtype=float)
print(arr5)
'''结果：[1. 3. 5. 7. 9.]'''

# 切片和索引
arr6 = np.arange(20)
s = slice(1,20,3)   # 从索引1开始到索引20停止，间隔为3
print (arr6[s])
'''结果：[ 1  4  7 10 13 16 19]'''
b = arr6[2:14:2]   # 从索引 2 开始到索引 14 停止，间隔为 2
print(b)
'''结果：[ 2  4  6  8 10 12]'''


#***********2 数学函数********************

# 三角函数：标准的三角函数：sin()、cos()、tan()
arr7 = np.array([0,45,90]) # 不同角度的正弦值
# 通过乘 pi/180 转化为弧度
print (np.sin(arr7*np.pi/180))
'''结果：[0.    0.70710678 1.  ]'''
# 类似的：正弦np.sin 余弦np.cos 正切np.tan；arcsin，arccos，和 arctan 函数返回给定角度的 sin，cos 和 tan 的反三角函数

# 加减乘除: add()，subtract()，multiply() 和 divide()、
arr8 = np.arange(9, dtype = np.float_).reshape(3,3)
print ('第一个数组：\n',arr8)
arr9 = np.array([10,10,10])
print ('第二个数组：\n',arr9)
print ('两个数组之和：\n',np.add(arr8,arr9))
'''结果：
第一个数组：
 [[0. 1. 2.]
 [3. 4. 5.]
 [6. 7. 8.]]
第二个数组：
 [10 10 10]
两个数组之和：
 [[10. 11. 12.]
 [13. 14. 15.]
 [16. 17. 18.]]
'''

# numpy.reciprocal() 函数返回参数逐元素的倒数。如 1/4 倒数为 4/1。
# numpy.power() 函数将第一个输入数组中的元素作为底数，计算它与第二个输入数组中相应元素的幂。
# numpy.mod() 计算输入数组中相应元素的相除后的余数。 函数 numpy.remainder() 也产生相同的结果。
# numpy.amin() 用于计算数组中的元素沿指定轴的最小值。
# numpy.amax() 用于计算数组中的元素沿指定轴的最大值。
# numpy.ptp()函数计算数组中元素最大值与最小值的差（最大值 - 最小值）
# numpy.percentile()百分位数是统计中使用的度量，表示小于这个值的观察值的百分比。
# numpy.median() 函数用于计算数组 a 中元素的中位数（中值）
# numpy.mean() 函数返回数组中元素的算术平均值。
# numpy.average() 函数根据在另一个数组中给出的各自的权重计算数组中元素的加权平均值。
# numpy.std()标准差公式如下：std = sqrt(mean((x - x.mean())**2))
# numpy.var()方差是每个样本值与全体样本值的平均数之差的平方值的平均数，即 mean((x - x.mean())** 2)。换句话说，标准差是方差的平方根。arr8 = np.arange(9, dtype = np.float).reshape(3,3)
# numpy.sort() 函数返回输入数组的排序副本。
# numpy.argsort() 函数返回的是数组值从小到大的索引值。
# numpy.argmax() 和 numpy.argmin()函数分别沿给定轴返回最大和最小元素的索引。
# ndarray.copy() 函数创建一个副本。


#***********3  矩阵运算********************
import numpy.matlib

# numpy.matlib.zeros() 函数创建一个以 0 填充的矩阵
print (np.matlib.zeros((3,3)))
'''结果：
[[0. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
'''

# numpy.matlib.identity() 函数返回给定大小的单位矩阵。
# 大小为4，整型单位矩阵
print(np.matlib.identity(5, dtype = int))
'''结果：
[[1 0 0 0 0]
 [0 1 0 0 0]
 [0 0 1 0 0]
 [0 0 0 1 0]
 [0 0 0 0 1]]
'''

# 类似的：
# numpy.matlib.ones()函数创建一个以 1 填充的矩阵。
# numpy.matlib.eye() 函数返回一个矩阵，对角线元素为 1，其他位置为零。
# numpy.matlib.rand() 函数创建一个给定大小的矩阵，数据是随机填充的。


#***********4  线性代数********************
# numpy.dot() 两个数组的点积，即元素对应相乘
arr10 = np.array([[1,2],[3,4]])
arr11 = np.array([[5,6],[7,8]])
print(np.dot(arr10,arr11))
'''结果：
[[19 22]
 [43 50]]
 '''

# numpy.vdot() 函数是两个向量的点积。 如果第一个参数是复数，那么它的共轭复数会用于计算。 如果参数是多维数组，它会被展开。
print(np.vdot(arr10,arr11))
'''结果：70 '''

# numpy.inner() 函数返回一维数组的向量内积。对于更高的维度，它返回最后一个轴上的和的乘积。
print (np.inner(arr10,arr11))

'''结果：
[[17 23]
 [39 53]]

计算：
1*5+2*6=17，1*7+2*8=23
3*5+4*6=39,3*7+4*8=53
 '''

 # numpy.matmul 函数返回两个数组的矩阵乘积。
 # numpy.linalg.det() 函数计算输入矩阵的行列式。
 # numpy.linalg.solve() 函数给出了矩阵形式的线性方程的解。
 # numpy.linalg.inv() 函数计算矩阵的乘法逆矩阵。

 #***********5  IO操作********************

 # NumPy 为 ndarray 对象引入了一个简单的文件格式：npy。npy 文件用于存储重建 ndarray 所需的数据、图形、dtype 和其他信息。
 # numpy.save() 函数将数组保存到以 .npy 为扩展名的文件中。
arr12 = np.array([[17,23],[39,53]])
 # 保存到 outfile.npy 文件上
np.save('data/outfile.npy',arr12)
# 保存到 outfile2.npy 文件上，如果文件路径末尾没有扩展名 .npy，该扩展名会被自动加上
# np.save('outfile2',arr12)

# numpy.load()
arr13 = np.load('data/outfile.npy')
print (arr13)
'''结果：
[[17. 23.]
 [39. 53.]]
 '''

# savetxt() 函数是以简单的文本文件格式存储数据，对应的使用 loadtxt() 函数来获取数据。
np.savetxt('out.txt',arr12)
arr14 = np.loadtxt('data/out.txt')
print(arr14)
'''结果：
[[17. 23.]
 [39. 53.]]
 '''