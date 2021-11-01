#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Filename:my_test
# Author:  tianguoxing
# Date:    2021/10/30 22:56

count_dict = {}


def func1(x):
    global count_dict
    tmp_res = ''
    for i in x:
        tmp = dict[x[i]]
        if tmp is None:
            tmp = 0
        dict[x[i]] = tmp + 1
        tmp_res = tmp_res.join(',').join(dict[x[i]])
    return tmp_res


if __name__ == '__main__':
    print('')