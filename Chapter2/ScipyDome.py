# coding:utf8

"""
DESC: Python数据预处理之Scipy教程
Author：伏草惟存
Prompt: code in Python3 env
"""

#************1 Scipy Linalg*******************

import numpy as np
from scipy import linalg

# 求解线性方程组
# 3x+2y=2
#  x- y=4
# 5y+ z=-2
a = np.array([[3, 2, 0], [1, -1, 0], [0, 5, 1]])
b = np.array([2, 4, -2])
res1 = linalg.solve(a, b)
print (res1)
# [ 2. -2.  8.]


# 求解行列式
# |A|是一个方阵
A = np.array([[1,2],[3,4]])
res2 = linalg.det(A)
print (res2)
# 1*4-2*3=-2.0


# 求解特征值和特征向量
# A是方阵，特征值λ和相应的特征向量v
# Av = λv
A = np.array([[1,2],[3,4]])
l, v = linalg.eig(A)
print ("特征值:\n",l,"\n特征向量\n", v)
# 特征值:
#  [-0.37228132+0.j  5.37228132+0.j]
# 特征向量
#  [[-0.82456484 -0.41597356]
#  [ 0.56576746 -0.90937671]]


# 奇异值分解(SVD)
# 矩阵a分解为两个酉矩阵U和Vh，以及一个奇异值(实数，非负)的一维数组s，使得
# a == U * S * Vh
a = np.random.randn(2, 3) + 1.j*np.random.randn(2, 3)
U, s, Vh = linalg.svd(a)
print ('酉矩阵:\n',U,'\n酉矩阵\n', Vh,'\n奇异值\n',s)
# 酉矩阵:
#  [[-0.55728327+6.19565045e-18j  0.83032244+1.53440325e-16j]
#  [-0.73499882+3.86279815e-01j -0.4933054 +2.59257451e-01j]]
# 酉矩阵
#  [[-0.01859058+0.2815052j   0.48875549-0.51402169j -0.59175181-0.25911153j]
#  [ 0.05125373-0.51573816j -0.43163592-0.32192764j -0.03326072-0.66357664j]
#  [-0.6951096 +0.41063251j -0.24183519-0.38531617j  0.37284682-0.04728662j]]
# 奇异值
#  [4.13890535 0.88993684]


#************2 Scipy 文件操作*******************

import scipy.io as sio
import numpy as np

#保存一个matlab文件
vect = np.arange(10)
sio.savemat('array.mat', {'vect':vect})

#加载一个matlab文件
mat_file_content = sio.loadmat('data/array.mat')
print (mat_file_content)

# 列出MATLAB文件中的变量
mat_file_content = sio.whosmat('data/array.mat')
print (mat_file_content)


#************3 Scipy 插值*******************

import numpy as np
from scipy.interpolate import *
import matplotlib.pyplot as plt

# 两个维度空间点绘图
x = np.linspace(0, 4, 12)
y = np.cos(x**2/3+4)
print (x,y)
plt.plot(x, y,'o')
plt.show()


# 一维插值
f1 = interp1d(x, y,kind = 'linear')
f2 = interp1d(x, y, kind = 'cubic')
xnew = np.linspace(0, 4,30)
plt.plot(x, y, 'o', xnew, f1(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic','nearest'], loc = 'best')
plt.show()


# 样条曲线

# 默认平滑参数
x = np.linspace(-3, 3, 50)
y = np.exp(-x**2) + 0.1 * np.random.randn(50)
plt.plot(x, y, 'ro', ms = 5)

# 手动更改平滑量
spl = UnivariateSpline(x, y)
xs = np.linspace(-3, 3, 1000)
spl.set_smoothing_factor(0.5)
plt.plot(xs, spl(xs), 'b', lw = 3)
plt.show()

#************4 Scipy Ndimage*******************


from scipy import misc,ndimage
import scipy.ndimage as nd
import numpy as np
import matplotlib.pyplot as plt


# 打开图像
f = misc.face()
misc.imsave('data/face.png', f)
plt.imshow(f)
plt.show()

# 图像倒置
face = misc.face()
flip_ud_face = np.flipud(face)
plt.imshow(flip_ud_face)
plt.show()

# 指定的角度旋转图像
face = misc.face()
rotate_face = ndimage.rotate(face, 45)
plt.imshow(rotate_face)
plt.show()

# 模糊图像
face = misc.face()
blurred_face = ndimage.gaussian_filter(face, sigma=5)
plt.imshow(blurred_face)
plt.show()



#************5 Scipy 优化算法*******************
# 梯度下降优化算法
# 我们求解方程：x^2-2x的最小值？常规方法求解如下：

def f(x):
    return x**2-2*x
x = np.arange(-10, 10, 0.1)
plt.plot(x, f(x))
plt.show()

from scipy import optimize
# 梯度下降优化算法
def f(x):
    return x**2-2*x
initial_x = 0
optimize.fmin_bfgs(f,initial_x)



# 最小二乘法优化算法
# 最小二乘
from scipy.optimize import least_squares
def fun_rosenbrock(x):
   return np.array([10 * (x[1] - x[0]**2), (1 - x[0])])
input = np.array([2, 2])
res = least_squares(fun_rosenbrock, input)
print ('最小值是：',res)


