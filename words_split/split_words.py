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

count_dict = collections.defaultdict(int)
dict_set = set()
classify_dict = collections.defaultdict(str)


def init_my_dict():
    global dict_set
    f = open("dict.txt", "r", encoding="utf-8")
    for i in f.readlines():
        dict_set.add(i.strip())
    print(dict_set)


# dict key:关键词，value:优化分类
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


def dict_word_stat(x):
    global count_dict
    global dict_set
    tmp_res = ''
    for i in x:
        tmp = count_dict[i]
        count_dict[i] = tmp + 1
        if i in dict_set:
            tmp_res = tmp_res + ',' + i
    return tmp_res[1:]


# 获取关键词（分词list）对应的分类
def get_word_classify(x):
    for i in x:
        classify = classify_dict[i]
        if classify is not None and len(classify) > 0:
            return classify


if __name__ == '__main__':
    init_my_dict()
    init_classify_dict()

    jieba.load_userdict('dict.txt')

    # 读取停用词数据
    stopwords = pd.read_csv('StopwordsCN.txt', encoding='utf8', names=['stopword'], index_col=False)

    # 停用词列表
    stop_list = stopwords['stopword'].tolist()

    # 读取数据
    # data = pd.read_csv('my_words_20211030.csv', encoding='utf-8').astype(str)
    data = pd.read_excel('11.10-11.10 VS 11.17-11.23.xlsx', sheet_name='11.17-11.23')

    # 查看数据
    # data.head()
    # data = df.values
    # print(format(data))

    # 中文
    chinese_pattern = re.compile('[^\u4e00-\u9fa50-9]')
    # 标点符号
    punctuation_pattern = re.compile(r'[^\w\s]')

    # 提取中文
    data['chinese'] = data['问题概述'].apply(lambda x: "".join(chinese_pattern.split(str(x))))
    # 过滤掉标点符号
    data['punctuation'] = data['chinese'].apply(lambda x: re.sub(punctuation_pattern, '', x))
    # 去除停用词
    data['cut'] = data['punctuation'].apply(lambda x: [i for i in set(jieba.cut(x)) if i not in stop_list])

    # pd.set_option('max_colwidth', 100)
    pd.set_option('display.max_rows', 100, 'display.max_columns', None,
                  'display.width', 200, 'display.max_colwidth', 100,
                  # 'display.unicode.ambiguous_as_wide', True, 'display.unicode.east_asian_width', True
                  )

    # print(data.head(100), flush=True)
    # print(type(data))

    data['res'] = data['cut'].apply(lambda x: dict_word_stat(x))
    data['classify'] = data['cut'].apply(lambda x: get_word_classify(x))

    list = sorted(count_dict.items(), key=operator.itemgetter(1), reverse=True)
    for x in list:
        print(x)

    # 删除临时列
    data.drop(columns=['chinese', 'punctuation'])

    # 入库

    data.insert(4, '标签', data['res'])
    data.insert(5, '分词分类', data['classify'])
    data.insert(6, '分词', data['cut'])
    data.drop(columns=['res', 'punctuation'])
    data.drop(columns=['classify', 'punctuation'])
    data.drop(columns=['cut', 'punctuation'])
    # 导出文件
    data.to_excel(excel_writer='save_as_11.17.xlsx')
