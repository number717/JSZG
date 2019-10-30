#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 16:30
# @Author  : Sand
# @FileName: 教师资格证2.0.py
# @Project : automation


import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from bs4 import BeautifulSoup


class Email:
    def __init__(self, server, sender, password, receiver, title, message=None, path=None):
        """初始化Email

        :param title: 邮件标题，必填。
        :param message: 邮件正文，非必填。
        :param path: 附件路径，可传入list（多附件）或str（单个附件），非必填。
        :param server: smtp服务器，必填。
        :param sender: 发件人，必填。
        :param password: 发件人密码，必填。
        :param receiver: 收件人，多收件人用“；”隔开，必填。
        """
        self.title = title
        self.message = message
        self.files = path

        self.msg = MIMEMultipart('related')

        self.server = server
        self.sender = sender
        self.receiver = receiver
        self.password = password

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver

        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message))

        # 连接服务器并发送
        try:
            smtp_server = smtplib.SMTP(self.server)  # 连接sever
        except (gaierror and error) as e:
            print('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)  # 登录
            except smtplib.SMTPAuthenticationError as e:
                print('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(';'), self.msg.as_string())  # 发送邮件
            finally:
                smtp_server.quit()  # 断开连接


if __name__ == '__main__':

    key_words = ["2019年", "下半年", "中小学教师资格考试", '笔试', '报名']
    URL = "http://www.hbea.edu.cn/html/zhks/index.shtml"

    wb_data = requests.get(URL)
    wb_data.encoding = 'utf-8'

    soup = BeautifulSoup(wb_data.text, 'lxml')
    message = []

    for item in soup.find_all('a'):
        head_line = item.get_text().strip()
        link = item.get('href')
        count = 0
        for key_word in key_words:
            if key_word in head_line:
                count += 1
        if count == len(key_words):
            message.append(head_line + ' ' + link)
        else:
            count = 0

    if message:
        msg = '\n'.join(message)
        print("Hi All,\n  以下是湖北考试院发布的最新关于教师资格证考试的通知:\n" + msg)
        e = Email(title='教师资格证考试通知',
                  message="Hi ALl,\n 以下是湖北考试院发布的最新关于教师资格证考试的通知\n" + msg,
                  receiver='yinl10@chinaunicom.cn;41489377@qq.com',
                  server='smtp.qq.com',
                  sender='29268036@qq.com',
                  password='714yy714717rr717',
                  path=''
                  )
        e.send()
    else:
        print('没有考试通知。')
