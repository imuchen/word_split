#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# Filename:split_words
# Author:  tianguoxing
# Date:    2021/10/30 20:54
# 导入相关库
import collections
import operator

import pandas as pd
import jieba
import re


classify_dict = collections.defaultdict(str)


def init_classify_dict():
    global classify_dict
    f = open("classify.txt", "r", encoding="utf-8")
    for line in f.readlines():
        line_split = line.strip().split('@')
        if line_split is not None and len(line_split) == 2:
            value = line_split[0].strip()
            keys = line_split[1]
            key_list = keys.split('#')
            if key_list is not None and len(key_list) > 0:
                for key in key_list:
                    classify_dict[key] = value
    print(classify_dict)


if __name__ == '__main__':
    init_classify_dict()

