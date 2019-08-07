# coding:utf-8

import sys  # 首先导入这个模块

list_test = sys.argv  # 它的返回值是一个列表


with open(list_test[1], 'rb', ) as f, open(list_test[2], 'wb') as f1:
    for line in f:
        f1.write(line)
