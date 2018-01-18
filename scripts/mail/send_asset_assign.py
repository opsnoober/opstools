#!/usr/bin/env python
# -*- coding:utf8 -*-
'''send mail for assign asset'''
__author__ = "kuilong.liu"

from datetime import datetime
import sys
import getopt

def usage():
    print("用法: ")
    print("	-t 资源类型[私有云|阿里云]")
    print("	-u ssh用户")
    print("	-i IP")
    print("	-a 申请人")
    print("	-m 管理员")
    print("	-U 用途")
    print("例子:python %s -t 私有云 -u secneo -i 172.16.31.85 -a 孙煜 -m 赵猛 -U 应用加固-5.2测试机"%sys.argv[0])

def gen_report(asset_type,ip,applicants,manager,uses,ssh_user='secneo'):
    ass_time = datetime.now().strftime("%Y-%m-%d")
    text = '''
资源已分配：
资源类型： %s服务器

ssh-user:  %s
ip:        %s
证书登录
申请人：   %s
管理员：   %s
用途：     %s
分配时间： %s
'''%(asset_type,ssh_user,ip,applicants,manager,uses,ass_time)
    print text
    return text
    

def send_mail():
    pass

def start():
    if len(sys.argv) < 12:
        usage()
        sys.exit(1)
    opts,args = getopt.getopt(sys.argv[1:],'ht:u:i:a:m:U:')
    for opt,arg in opts:
        if opt == '-h':
            usage()
        elif opt == '-t':
            asset_type = arg
        elif opt == '-u':
            ssh_user = arg
        elif opt == '-i':
            ip = arg
        elif opt == '-a':
            applicants = arg
        elif opt == '-m':
            manager = arg
        elif opt == '-U':
            uses = arg

    gen_report(asset_type=asset_type,ssh_user=ssh_user,ip=ip,applicants=applicants,manager=manager,uses=uses)
    send_mail()

if __name__ == "__main__":
    start()
