#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: kuilong.liu
# desc: 运维黑盒部署自检及修复工具,检查部署完成的系统ip地址及时区,并修复

import platform
import re
import time   
import datetime
import httplib
import os
import argparse
import sys
import socket
import fcntl
import struct
import subprocess

ok = " \033[1;32m [ok] \033[0m".ljust(20)
fail = " \033[1;31m [fail] \033[0m".ljust(20)
running = "\033[1;33m===================={}====================\033[0m"

def banner():
    print("*"*50)
    name = '''
    
 _                   _               _    
| |__   _____  _____| |__   ___  ___| | __
| '_ \ / _ \ \/ / __| '_ \ / _ \/ __| |/ /
| |_) | (_) >  < (__| | | |  __/ (__|   < 
|_.__/ \___/_/\_\___|_| |_|\___|\___|_|\_\ 
                                          


    '''
    print(name)
    print("运维黑盒部署自检及修复工具: v1.0")
    print("*"*50)

def get_webservertime(host="www.baidu.com"):
    '''获取标准服务器时间'''
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("GET", "/")
        r = conn.getresponse()
        ts = r.getheader('date')
        ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
        ttime =time.localtime(time.mktime(ltime)+8*60*60)
        return time.mktime(ltime)+8*60*60
    except:
        return None
        
def get_ifname():
    '''获取主机网卡名称列表,e开头的,em1,eno1,eth0'''
    cmd = 'ip a s'
    sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    p = sub.communicate()
    pattern = re.compile("\d: [e]\w+")
    mach_list = re.findall(pattern,p[0])    
    net_list = []
    for i in mach_list:
        j = i.split(":")[1].strip()
        net_list.append(j)
    return net_list

def get_ip_addr(ifname):
    '''获取指定网卡的ip地址'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
        return ip
    except:
        return None
        
def get_netmask(ifname):
    '''获取子网掩码'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
       netmask = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x891b,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
       return netmask
    except:
        return None

def get_gateway(ifname):
    '''获取网关地址'''
    cmd_show = 'ip r s dev %s' %ifname
    sub = subprocess.Popen(cmd_show,shell=True,stdout=subprocess.PIPE)
    p = sub.communicate()
    machObj = re.match('^default via',p[0])
    if machObj:
        try:
            gateway = p[0].split()[2]
            return gateway
        except:
            return None
    else:
        return None

class Check(object):
    '''检查类'''
    def __init__(self):
        pass

    def check_sys(self):
        
        return "%s %s" %(platform.dist()[0],platform.dist()[1])
    
    def check_ip_type(self):
        '''检查ip地址配置类型dhcp or static'''
 #       net_list = ["em1","eno1","eth0"]
        if platform.dist()[0] == "Ubuntu":
            with open("/etc/network/interfaces",'r') as f:
                lines = f.readlines()
            for line in lines:
                #machObj = re.match(r'^iface (.*?) dhcp',line,re.M|re.I)
                machObj = re.match(r'^iface (.*?) static',line,re.S)
                if machObj:
                    return machObj.group()
                else:
                    pass
        else:
            pass
    
    def check_timezone(self):
        timez = time.strftime('%Z', time.localtime()) 
        return timez 

    def check_hw_date(self):
        '''检查硬件时钟'''
        sub = subprocess.Popen('sudo hwclock',shell=True,stdout=subprocess.PIPE)
        hw_date_delta = abs(float(sub.communicate()[0].split()[-2]))
        return hw_date_delta

class Repair(object):
    '''修复类'''
    def __init__(self):
        print(running.format("修复系统开始"))
    
    def repair_ip_type(self):
        '''修改ip地址类型'''
        print(running.format("修复ip地址配置"))
        ifnames = get_ifname()
        lines = ["auto lo\n","iface lo inet loopback\n","\n"]
        for ifname in ifnames:
            ip = get_ip_addr(ifname)
            netmask = get_netmask(ifname)
            gateway = get_gateway(ifname)
            dns = "223.5.5.5"
            #print "auto {}".format(ifname) 
            #print "iface {} inet static".format(ifname)
            #print "address {}".format(ip)
            #print "netmask {}".format(netmask)
            lines.append("auto {}\n".format(ifname))
            lines.append("iface {} inet static\n".format(ifname))
            lines.append("address {}\n".format(ip))
            lines.append("netmask {}\n".format(netmask))
            if ifname in ["em2","eno2","eth1"]:
                print ""
                lines.append("\n")
            else:
                #print "gateway {}\n".format(gateway)
                lines.append("gateway {}\n".format(gateway))
                lines.append("dns-nameservers {}\n".format(dns))
                lines.append("\n")
            print ""
        for i in lines:
            print i.strip()
        answer = raw_input("确认网卡信息是否正确[Y|N] ? ")
        if answer in ["y","Y"]:
            #with open("interfaces",'w') as f:
            with open("/etc/network/interfaces",'w') as f:
                f.writelines(lines)
        else:
            print("网卡未完成配置")
        
    def repair_timezone(self):
        '''修改时区'''
        print(running.format("修改时区"))
        os.system("sudo dpkg-reconfigure tzdata")

    def sync_time(self):
        '''同步时间'''
        print(running.format("同步系统和硬件时间"))
        time1 = get_webservertime()
        ltime = time.localtime(time1)
        cmd_date = "sudo date -s '%s-%s-%s %s:%s:%s'"%(ltime.tm_year,ltime.tm_mon,ltime.tm_mday,ltime.tm_hour,ltime.tm_min,ltime.tm_sec)
        cmd_hw = 'sudo hwclock -w'
        os.system(cmd_date)
        os.system(cmd_hw)
    

def check():
    obj = Check()
    s = obj.check_sys()
    print("%s ===> 当前系统版本为 : %s" %(ok,s))
    ip_type = obj.check_ip_type()
    if ip_type:
        print("%s ===> 当前ip地址配置方式为: 静态分配 "%ok)
    else:
        print("%s ===> 当前ip地址配置方式为: DHCP "%fail)
    timez = obj.check_timezone()
    if timez == "CST":
        print("%s ===> 当前系统时区为 :  %s" %(ok,timez))
    else:
        print("%s ===> 当前系统时区为 :  %s" %(fail,timez))
    t = get_webservertime()
    c = time.time()
    if t:
        if abs(t-c) > 300:
            print("%s ===> 当前系统时间不准,与标准时间相差%s s "%(fail,abs(t-c)))
        else:
            print("%s ===> 当前系统时间准确: %s " %(ok,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    else:
        print("%s ===> 无法获取标准服务器时间,请检查网络"%(fail))
    hw_date_delta = obj.check_hw_date()
    if hw_date_delta > 1:
        print("%s ===> 当前硬件时间不准,与系统时间相差%s s "%(fail,hw_date_delta))
    else:
        print("%s ===> 当前硬件时间准确: %s" %(ok,subprocess.Popen("sudo hwclock",shell=True,stdout=subprocess.PIPE).communicate()[0]))
    

def repair():
    obj = Repair()
    obj.repair_timezone()
    obj.repair_ip_type()
    obj.sync_time()

def start():
    banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--check", help="check system",action="store_true")
    parser.add_argument("-r", "--repair", help="repair system",action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    elif args.repair:
        repair()
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.argv.append('-h')
        start()
    else:
        start()