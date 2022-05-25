#!/usr/bin/python
# coding:utf-8

import os
import time


if __name__ == '__main__':
    while True:
        os.system("scrapy crawl bbsspider")       # 运行爬虫
        os.popen('cd bbs_project')
        os.popen('chmod a+x multimail.py')
        os.popen('./multimail.py')                     # 发送邮件
        time.sleep(3600)                          # 每隔一小时执行一次程序（半小时可能用户收邮件太频繁了）


