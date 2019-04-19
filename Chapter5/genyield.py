# coding:utf-8

"""
DESC:  yield生成器
Author：伏草惟存
Prompt: code in Python3 env
"""

import random,os,time


'''
斐波那契数列: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144......
              这个数列从第3项开始，每一项都等于前两项之和
数学上定义：F(0)=1，F(1)=1, F(n)=F(n-1)+F(n-2)（n>=2，n∈N*）
'''
# 普通斐波那契数列
def fab1(max):
    n, a, b = 0, 0, 1
    while n < max:
        a, b = b, a + b
        n = n + 1


# 生成器：斐波那契数列
def fab2(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b      # 使用 yield
        a, b = b, a + b
        n = n + 1


# 生成器案例。 Generator / yield
def GeneratorDome():
    maxnum = 100000 # 最大迭代次数
    # 普通斐波那契数列耗时
    t1 = time.time()
    fab1(maxnum)
    t2 = time.time()
    print('fab1 total tims %.2f ' % (1000*(t2-t1)) + ' ms')

    # 生成器方法耗时
    b = fab2(maxnum)
    t3 = time.time()
    print('fab2 total tims %.2f ' % (1000*(t3-t2)) + ' ms')



if __name__=='__main__':
    GeneratorDome()


# 1：数组、链表、字符串、文件等缺点就是所有数据都在内存里，海量的数据耗内存。
# 2：生成器是可以迭代的，工作原理就是重复调用next()方法，直到捕获一个异常。
# 3：有yield的函数不再是一个普通的函数，而是一个生成器generator，可用于迭代。
# 4：yield是一个类似return 的关键字