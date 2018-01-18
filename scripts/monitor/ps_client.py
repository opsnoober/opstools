#-*- coding: utf-8 -*-
from tkinter import *
from socket import *

class Ps_server:
    def __init__(self):
        self.ip = None
        self.port = None
        self.data = None
        self.c_sock = None

        self.root = Tk()
        self.root.geometry('300x300+250+250')

        self.et_ip = Entry(self.root,width=30)
        self.et_port = Entry(self.root,width=6)

        self.ip_label = Label(self.root,text='IP地址',width=10)
        self.port_label = Label(self.root,text='端口',width=10)

        self.bt_conn = Button(self.root,text='连接',width=5,
            height=1,command=self.connect,
            )
        self.bt_close = Button(self.root,text='断开',width=5,height=1,
            state='disable',
            command=self.close,
            )
        self.bt_get_info = Button(self.root,text='获取',width=5,height=1,
            state='disable',
            command=self.get_info
            )

        self.la_data = Label(self.root,text='信息...')

    def main(self):
        self.et_ip.place(x=0,y=0)
        self.ip_label.place(x=150,y=0)

        self.et_port.place(x=0,y=30)#下一行是下一个输入框
        self.port_label.place(x=50,y=30)

        self.bt_conn.place(x=0,y=60)
        self.bt_close.place(x=100,y=60)
        self.bt_get_info.place(x=200,y=60)

        self.la_data.place(x=0,y=110)
        self.root.mainloop()

    def connect(self):
        self.ip = self.et_ip.get()#获取输入框的文本
        self.port = self.et_port.get()
        print('ip:',self.ip)
        print('port:',self.port)
        if not self.ip and not self.port :
            self.la_data['text'] = '输入有效信息...'
            return 
        self.la_data['text'] = '正在连接...'
        self.c_sock = socket(AF_INET,SOCK_STREAM)
        try:
            self.c_sock.connect((self.ip,int(self.port)))
        except Exception as e:
            print(e)
            self.la_data['text'] = '连接失败...'
        else:
            self.bt_close['state'] = 'active'
            self.bt_get_info['state'] = 'active'
            self.la_data['text'] = '连接成功...'

    def close(self):
        self.c_sock.close()
        self.bt_close['state'] = 'disable'
        self.bt_get_info['state'] = 'disable'
        self.la_data['text'] = '连接断开...'

    def get_info(self):
        self.c_sock.send('cpu'.encode('utf-8'))
        data = self.c_sock.recv(1024).decode('utf-8')
        if not data:
            self.la_data['text'] = '远程主机关闭连接...'
        self.la_data['text'] = data

ps = Ps_server()
ps.main()
