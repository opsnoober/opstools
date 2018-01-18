#!/usr/bin/python
# -*- coding: utf-8 -*-
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

def sendEmail(authInfo, fromAdd, toAdd, ccAdd, subject, plainText, htmlText):

        strFrom = fromAdd
        strTo = ','.join(toAdd)
        strCc = ','.join(ccAdd)

        server = authInfo.get('server')
        user = authInfo.get('user')
        passwd = authInfo.get('password')

        if not (server and user and passwd) :
                print 'incomplete login info, exit now'
                return

        # 设定root信息
        msgRoot = MIMEMultipart('related')
        msgRoot['Subject'] = subject
        msgRoot['From'] = strFrom
        msgRoot['To'] = strTo
        msgRoot['Cc'] = strCc
        msgRoot.preamble = 'This is a multi-part message in MIME format.'

        # Encapsulate the plain and HTML versions of the message body in an
        # 'alternative' part, so message agents can decide which they want to display.
        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        #设定纯文本信息
        # msgText = MIMEText(plainText, 'plain', 'utf-8')
        # msgAlternative.attach(msgText)

        #设定HTML信息
        msgText = MIMEText(htmlText, 'html', 'utf-8')
        msgAlternative.attach(msgText)

      #设定内置图片信息
        # fp = open('test.jpg', 'rb')
        # msgImage = MIMEImage(fp.read())
        # fp.close()
        # msgImage.add_header('Content-ID', '<image1>')
        # msgRoot.attach(msgImage)

       #发送邮件
        smtp = smtplib.SMTP()
       #设定调试级别，依情况而定
        smtp.set_debuglevel(1)
        smtp.connect(server)
        smtp.login(user, passwd)
        smtp.sendmail(strFrom, strTo+','+strCc, msgRoot.as_string())
        smtp.quit()
        return

if __name__ == '__main__' :
        authInfo = {}
        authInfo['server'] = ''
        authInfo['user'] = ''
        authInfo['password'] = ''
        fromAdd = ''
        toAdd = ['']
        ccAdd = ['m']
        subject = '资源分配'
        plainText = '这里是普通文本'
        #htmlText = '<B>HTML文本</B>'
        # with open('a.html','rb') as f:
        #     htmlText = f.read()
        from app import html
        htmlText = html
        sendEmail(authInfo, fromAdd, toAdd, ccAdd, subject, plainText, htmlText)
