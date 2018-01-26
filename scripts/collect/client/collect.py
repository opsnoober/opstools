# -*- coding:utf-8 -*-
import platform
import shlex
import subprocess
import json
import re

#定义一个设备类
class Device(object):

    def __init__(self):
        self.id = None              #编号
        self.name = None            #名称
        self.model = None           #型号
        self.dense = None           #密级
        self.uses = None            #用途
        self.f_department = None    #一级部门
        self.s_department = None    #二级部门
        self.location = None        #放置地点
        self.manager = None         #责任人
        self.os = None              #操作系统
        self.os_dist = None         #操作系统版本
        self.os_install_time = None #系统安装时间
        self.disk_sn = None         #磁盘序列号
        self.device_sn = None       #设备序列号
        self.cpu = None             #cpu型号
        self.ip = None              #IP地址
        self.mac = None             #MAC地址
        self.start_time = None      #启用时间

    def getOs(self):
        #获取操作系统类型
        _os_type = platform.system()
        if _os_type:
            if _os_type == "Darwin":
                self.os = "MacOS"
            else:
                self.os = _os_type
        return self.os

    def getOsDist(self):
        #获取操作系统版本
        _os_dist = ''
        if self.os == "Linux":
            _os_dist = platform.linux_distribution()
            self.os_dist = '{} {} {}'.format(_os_dist[0],_os_dist[1],_os_dist[2])
        elif self.os == "Windows":
            _os_dist = platform.win32_ver()
            self.os_dist = '{}{} {} {}'.format(self.os,_os_dist[0],_os_dist[1],_os_dist[2])
        elif self.os == "MacOS":
            _os_dist = platform.mac_ver()
            self.os_dist = '{} {}'.format(self.os,_os_dist[0])
        return self.os_dist

    def getDeviceSn(self):
        #获取设备序列号
        _sn = ''
        _cmd = ''
        if self.os == "Linux":
            _cmd = shlex.split("sudo dmidecode -s system-serial-number")
            _sn = subprocess.Popen(_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0].strip()
            if _sn:
                self.device_sn = _sn.decode("utf-8")
                print("------------------------------")
                print(self.device_sn)
        elif self.os == "Windows":
            pass
            # self.device_sn =
        elif self.os == "MacOS":
            _cmd = shlex.split("system_profiler SPHardwareDataType")
            _tmp_string = subprocess.Popen(_cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
            _machobj = re.compile("Serial Number \(system\): \w+")
            _sn = re.findall(_machobj,_tmp_string.decode("utf-8"))
            if _mach:
                self.device_sn = _sn[0].split(":")[-1].strip()
        return self.device_sn

    def getDiskSn(self):
        #获取磁盘序列号
        _disk_sn = ''
        if self.os == "Linux":
            pass
            # self.disk_sn =
        elif self.os == "Windows":
            pass
            # self.disk_sn =
        elif self.os == "MacOS":
            pass
            # self.disk_sn =
        return self.disk_sn

    def getMacAddr(self):
        import uuid
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
        self.mac = ":".join([mac[e:e+2] for e in range(0,11,2)])
        return self.mac

def collect():
    obj = Device()
    obj.getOs()
    obj.getOsDist()
    obj.getDeviceSn()
    obj.getDiskSn()
    obj.getMacAddr()
    data = {
        "os": obj.os,
        "os_dist": obj.os_dist,
        "device_sn": obj.device_sn,
        "disk_sn": obj.disk_sn,
        "mac": obj.mac
    }
    # print json.dumps(data,indent=4)
    return json.dumps(data,indent=4)

if __name__ == '__main__':
    collect()
