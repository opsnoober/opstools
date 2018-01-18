#-*- coding:utf-8 -*-
import psutil
from time import sleep
from socket import *
def get_cpu(t=1):
    t1 = psutil.cpu_times()#获取开始时间的CPU时间累计
    sleep(t)
    t2 = psutil.cpu_times()#获取结束时间的CPU时间累计
    t1_all = sum(t1)#求出总时间
    t2_all = sum(t2)
    t1_busy = t1_all - t1.idle #开始时间时的CPU非空闲时间
    t2_busy = t2_all - t2.idle
    if t2_busy - t1_busy < 0:
        return 0.0
    cpu_busy = t2_busy - t1_busy  #这一个时间区间内，CPU的工作时间累计
    all_time = t2_all - t1_all #CPU花费的所有时间
    cpu_time = (cpu_busy / all_time )* 100 #百分比
    return round(cpu_time,2)

s_sock = socket(AF_INET,SOCK_STREAM)#TCP/IPV4
s_sock.bind(('',8888))
s_sock.listen(5)
print('Wait For Connection...')
while True:
    c_sock,c_addr = s_sock.accept()#接收到这个用户链接
    print('Connection From: ', c_addr)
    while True:
        data = c_sock.recv(1024).decode('utf-8')
        print('Client:',data)
        if not data:
            print("Connection Close: ",c_addr)
            break
        if data == 'cpu':
            buf = str(get_cpu()).encode('utf-8')
            c_sock.send(buf)
    c_sock.close()
s_sock.close()
