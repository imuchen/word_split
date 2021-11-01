# -*- coding: utf-8 -*-
import urllib.request
import re
import time
import json

from selenium import webdriver
from bs4 import BeautifulSoup
import random
from lxml import etree
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

'''
====================测试结果=======================
商品ID 价格(原价) 1星 2星 3星 4星 5星 评论数 平均评分 好评数 好评率 中评数 中评率 差评数 差评率 :
967821 3199.00(3800.00) 19 7 35 175 556 792 5 731 0.924 42 0.053 19 0.023
本次京东爬虫执行时间约为： 0.48 s
商品ID、价格、评论数、评分、月销量、总库存:
39086934885 85.00 0 4.6 3 1315
'''


def getjd(pid):
    '''通过京东服务器查'''
    pid = str(pid)
    # 上面获取了商品ID，下面就是把ID添加到京东那个查价格的json地址里
    url = 'http://p.3.cn/prices/get?skuid=J_' + str(pid)
    html = urllib.request.urlopen(url).read().decode('utf-8')

    nprice = re.search(r'"p":"(.*?)"', html).group(1)

    price = nprice
    url = r'http://club.jd.com/productpage/p-{}-s-0-t-3-p-0.html'.format(
        pid)
    headers1 = {'GET': '',
                'Host': "club.jd.com",
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                'Referer': 'http://item.jd.com/%s.html' % (pid)}

    req = urllib.request.Request(url, headers=headers1)
    scode = urllib.request.urlopen(req).read().decode('gbk', 'ignore')
    dd = json.loads(scode)

    name = dd["comments"][0]["referenceName"]

    return (pid, price, name)


# 测试京东

print('商品ID', '价格(原价)')

print(*getjd(5605230))

print(*getjd(5605230))

print(*getjd(100006937602))

print(*getjd(100013589838))
print(*getjd(64678870524))

print(*getjd(1268059))

print(*getjd(100006937602))

print(*getjd(100013589838))
print(*getjd(64678870524))

print(*getjd(1268059))

print(*getjd(100006937602))

print(*getjd(100013589838))
