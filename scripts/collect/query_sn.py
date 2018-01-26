#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
远程查询服务器sn号工具
'''
__author__ = "kuilong.liu"

import subprocess
import shlex
import sys
import os
import traceback
import argparse

class Server(object):

    def __init__(self):
        self.ip = None
        self.username = None
        self.password = None
        self.port = 22
        self.os = None
        self.sn = None
        self.env = os.environ.copy()["ANSIBLE_HOST_KEY_CHECKING"] = False # 首次连接不需要输入yes

    def genInventory(self):
        hosts_info = '{} ansible_ssh_port={} ansible_ssh_user={} ansible_ssh_pass={} ansible_sudo_pass={}'.format(self.ip,self.port,self.username,self.password,self.password)
        with open('hosts','w') as f:
            f.write("[remote]\n")
            f.write(hosts_info)

    def getPing(self):
        cmd = shlex.split("ansible -i hosts remote -m ping")
        p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (out,err) = p.communicate()
        # print out.split("\n")[0].split(" ")[2].strip()
        if out.split("\n")[0].split(" ")[2].strip() == "UNREACHABLE!":
            print("无法连接目标主机")
            sys.exit(1)


    def queryOsType(self):
        cmd = shlex.split("ansible -i hosts remote -m setup -a 'filter=ansible_system'")
        p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (out,err)= p.communicate()
        # print p.returncode
        if p.returncode:
            raise Exception('program returned error code {0}'.format(p.returncode))
        else:
            # print out.split("\n")[2].split(":")[-1].replace('"','').strip()
            self.os = out.split("\n")[2].split(":")[-1].replace('"','').strip()


    def querySn(self):
        _ansible_str = ''
        if self.os == "Linux":
            _ansible_str = "ansible -i hosts remote -m shell -a 'dmidecode -s system-serial-number' -s"
        elif self.os == "Darwin":
            # _ansible_str =  "ioreg -d2 -c IOPlatformExpertDevice"
            _ansible_str =  "ansible -i hosts remote -m shell -a 'ioreg -l | grep IOPlatformSerialNumber'"
        cmd = shlex.split(_ansible_str)
        # print cmd
        p = subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        # self.sn = p.stdout.readlines()[1]
        (out,err)= p.communicate()
        # print p.returncode
        if p.returncode:
            raise Exception('program returned error code {0}'.format(p.returncode))
        else:
            # print out.split('\n')[1]
            if self.os == "Linux":
                self.sn = out.split("\n")[1]
            elif self.os == "Darwin":
                # print out.split(' ')[-1].replace('"','').strip("")
                self.sn = out.split(' ')[-1].replace('"','').replace("\n","").strip("")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--ip", help="remote ip")
    parser.add_argument("-p","--port", type=int, default=22, help="remote port")
    parser.add_argument("-u","--username", default='secneo', help="remote username")
    parser.add_argument("-P","--password", help="remote password")
    args = parser.parse_args()

    obj = Server()
    obj.ip = args.ip
    obj.username = args.username
    obj.password = args.password
    obj.port = args.port
    obj.genInventory()
    obj.getPing()
    obj.queryOsType()
    obj.querySn()
    print obj.sn

if __name__ == '__main__':
    main()
