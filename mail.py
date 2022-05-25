#!/usr/bin/python
#coding=utf-8
# 去掉首行，main函数无法执行mail文件 ；去掉第二行，程序会报错

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

lspider = []                  # 存放爬取到的信息
with open('bbs_server.txt','r') as f1:
    for line in f1.readlines():
        lspider.append(line.split(' ',3))
                              # 对pipelines写的.txt文件进行读取

luser = []
with open('user.txt','r') as f2:
    for line in f2.readlines():
        luser.append(line.split())
                              # 这一段读取存储用户信息的文件

# 以下先对单个用户所有话题发送邮件

def contexts(lis):
    Dtitle = {'22': 'Triangle', '71': 'SecondHand', '72':'Joke', '99': 'Job', '167': 'PieBridge', '230': 'House',
            '251': 'Counterculture', '342': 'AcademicInfo', '351': 'CampusInfo', '414': 'SecretGarden', '896': 'Intern',
            '914': 'SecondBook', '1431': 'CanteenDorm'}                            # 定义url-话题对应关系
    Dcolor = {'22': 'navy', '71': 'purple', '99': 'green', '167': 'hotpink', '230': 'darkslategray',
            '251': 'olive', '342': 'orangered', '351': 'red', '414': 'gold', '896': 'royalblue',
            '914': 'darkorange', '1431': 'limegreen'}                              # 定义url-主题颜色对应
    lis.sort(key=lambda x: x[1])                        # 同类话题归类
    ltitle = [lis[i][1] for i in range(len(lis))]
    context = '<html><body>'                      # 正文的开始
    i = 0
    while i < len(lis):
        k = ltitle.count(ltitle[i])
        context += '<h1 align="center" style=“font-family:verdana;color:{};”>{}</h1>'.format(Dcolor[lis[i][1]],Dtitle[lis[i][1]])    # 标题
        for j in range(k):
            context += '<p><big>{}</big><div><i>{} minutes ago</i></div>'.format(str(j + 1) + ': ' + lis[i+j][3], lis[i+j][0][:-7])  # 内容，时间
            context += 'click to view <a href="{}">details</a>...</p>'.format('https://bbs.pku.edu.cn/v2/' + lis[i+j][2])            # 链接
        context += '<HR style="FILTER: alpha(opacity=80,finishopacity=0,style=3)" align=center color=#987cb9 SIZE=1>'                # 分割线
        i += k
    context += '<footer align="center" style="color:blue;" ><em>Thanks for your support.<br/>Best wishes!</em></footer>'             # 脚注
    context += '</body></html>'
    return context
                      #编辑html正文内容

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
                      #定义格式化邮件函数

from_addr = 'pku_bbs_server@163.com'    # 这里需补充上发件人邮箱
password = '3lzx2wjs1wyc'              # 这里需补充上邮箱密码
to_addr = 'bbsserver2019@163.com'
smtp_server = 'smtp.163.com'

msg = MIMEText(contexts(lspider), 'html', 'utf-8')
msg['From'] = _format_addr('bbs_server_developer <%s>' % from_addr)
msg['To'] = _format_addr('bbs_server_user <%s>' % to_addr)
msg['Subject'] = Header('We found several posts matching your need', 'utf-8').encode()
      #格式化邮件

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
      #发送邮件