#!/usr/bin/python
# -*- coding: utf-8 -*-

import scrapy
import re
from bs4 import BeautifulSoup


class BbsspiderSpider(scrapy.Spider):
    name = 'bbsspider'
    start_urls = [
        'https://bbs.pku.edu.cn/v2/thread.php?bid=22',      # Triangle 三角地
        'https://bbs.pku.edu.cn/v2/thread.php?bid=71',      # SecondHand 跳蚤市场
        'https://bbs.pku.edu.cn/v2/thread.php?bid=72',      # Joke 笑口常开
        'https://bbs.pku.edu.cn/v2/thread.php?bid=99',      # Job 工作
        'https://bbs.pku.edu.cn/v2/thread.php?bid=167',     # PieBridge 鹊桥
        'https://bbs.pku.edu.cn/v2/thread.php?bid=230',     # House 租房
        'https://bbs.pku.edu.cn/v2/thread.php?bid=242'      # Volunteers 北大青年志愿者协会
        'https://bbs.pku.edu.cn/v2/thread.php?bid=251',     # Counterculture 非主流文化
        'https://bbs.pku.edu.cn/v2/thread.php?bid=342',     # AcademicInfo 讲座动态
        'https://bbs.pku.edu.cn/v2/thread.php?bid=351',     # CampusInfo 校园热点
        'https://bbs.pku.edu.cn/v2/thread.php?bid=414',     # SecretGarden 别问我是谁
        'https://bbs.pku.edu.cn/v2/thread.php?bid=896',     # Intern 实习
        'https://bbs.pku.edu.cn/v2/thread.php?bid=914',     # SecondBook 出书
        'https://bbs.pku.edu.cn/v2/thread.php?bid=1431',    # CanteenDorm 燕园食宿
    ]

    def parse(self, response):
        infoDict = {}
        soup = BeautifulSoup(response.body, 'html.parser')
        q = soup.find_all('div', string=re.compile('分钟前'))  # 找到所有一小时内发布的帖子
        for x in q:
            if x.parent.previous_sibling.previous_sibling.attrs['class'][0] == 'avatar':
                link = x.parent.parent.find('a').attrs['href']             # 提取发帖链接
                key = link[link.index('=')+1:link.index('&')]
                val = []
                val.append(x.string)                                       # 提取发帖时间
                val.append(link[link.index('=')+1:link.index('&')])        # 提取版面特征url
                val.append(link)
                val.append(x.parent.previous_sibling.previous_sibling.previous_sibling \
                           .previous_sibling.contents[1].string)           # 提取发帖主题
                infoDict[key] = val
            else:
                continue
        yield infoDict           # 提供给后面pipelines处理