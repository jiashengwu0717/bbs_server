#!/usr/bin/python
#coding=utf-8
# 去掉首行，main函数无法执行mail文件 ；去掉第二行，程序会报错

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

Dtitle = {'22': 'Triangle三角地', '71': 'SecondHand跳蚤市场', '72':'Joke', '99': 'Job工作', '167': 'PieBridge鹊桥', '230': 'House租房',
            '251': 'Counterculture非主流文化', '342': 'AcademicInfo讲座动态', '351': 'CampusInfo校园热点', '414': 'SecretGarden别问我是谁',
          '896': 'Intern实习','914': 'SecondBook二手书', '1431': 'CanteenDorm燕园食宿'}                          # 定义url-话题对应关系
Dcolor = {'22': '#F3F3FA', '71': '#ECFFFF', '72':'#FFD2D2', '99': '#E8FFF5', '167': '#FFECF5', '230': '#D1E9E9',
            '251': '#E8E8D0', '342': '#FFEEDD', '351': '#FFD2D2', '414': '#EFFFD7', '896': '#FFE6FF',
            '914': '#F2E6E6', '1431': '#DFFFDF'}                              # 定义url-话题背景颜色对应

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
                      #定义格式化邮件函数

lspider = []                  # 存放爬取到的信息
with open('bbs_server.txt','r') as f1:
    for line in f1.readlines():
        lspider.append(line.split(' ',3))
lspider.sort(key=lambda x: x[1])
ltitle = [Dtitle[lspider[i][1]] for i in range(len(lspider))]
                              # 对pipelines写的.txt文件进行读取

luser = []
with open('user.txt','r') as f2:
    for line in f2.readlines():
        luser.append(line.split())
                              # 这一段读取存储用户信息的文件

def terms(time,str,addr):
    with open('html_initial_version/terms.html.txt','r') as f3:
        s = f3.read().replace('\n', '')
    return s.format(time,str,addr)                                 # 单个话题的爬取内容

def table(url,subject,bgcolor,preterms):
    with open('html_initial_version/table.html.txt','r') as f4:
        s = f4.read().replace('\n', '')
    return s.format(bgcolor,subject,preterms,url)                 # 每个话题的邮件版面

def framework(emailaddr,pretable):
    with open('html_initial_version/framework.html.txt','r') as f5:
        s = f5.read().replace('\n', '')
    return s.format('{text-decoration: none}',pretable,emailaddr)                       # 整个html文本

def contexts(emailaddr,lt,ls):
    context = ''
    temptable = ''
    for x in lt:
        if x in ltitle:
            m = ltitle.index(x)
            k = ltitle.count(x)
            tempitems = ''
            for i in range(k):
                tempitems += terms(ls[m+i][0],ls[m+i][3],ls[m+i][2])
            temptable += table(ls[m][1],x,Dcolor[ls[m][1]],tempitems)
    context += framework(emailaddr,temptable)
    return context
                                                             # 每个用户的html邮件全文
for x in luser:
    ltag = x[2:]
    if set(ltitle)&set(ltag) == set():                       # 排除暂时无需发送的邮件
        continue
    else:
        from_addr = 'pku_bbs_server@163.com'  # 这里需补充上发件人邮箱
        password = '3lzx2wjs1wyc'         # 这里需补充上邮箱密码
        to_addr = '{}'.format(x[1])
        smtp_server = 'smtp.163.com'

        msg = MIMEText(contexts(x[1], ltag, lspider), 'html', 'utf-8')
        msg['From'] = _format_addr('BBSServer developer <{}>'.format(from_addr))
        msg['To'] = _format_addr('{} <{}>'.format(x[0], to_addr))
        msg['Subject'] = Header('We found several posts matching your need', 'utf-8').encode()
        # 格式化邮件
        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        # 发送邮件