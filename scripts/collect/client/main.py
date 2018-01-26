# -*- coding:utf-8 -*-
from collect import collect

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import time

class Systeminfo(object):

    def __init__(self):
        self.root = Tk()
        self.root.title(u"系统信息收集工具")
        self.root.resizable(False,False)
        self.root.configure(background="#e1d8b9")
        # root.mainloop()
        #header
        self.frame_header = Frame(self.root,bg="#e1d8b9")
        self.frame_header.pack()
        Label(self.frame_header,text=u"系统信息收集",bg="#e1d8b9",font = ('Arial',14)).grid(row=0,column=0,padx=5,pady=10)
        # content
        self.frame_content = Frame(self.root,bg="#e1d8b9")
        self.frame_content.pack()
        self.text_info = Text(self.frame_content)
        self.text_info.grid(row=0,column=0,padx=5,sticky = 'sw')
        #footer
        self.frame_footer = Frame(self.root,bg="#e1d8b9")
        self.frame_footer.pack(side=LEFT)
        self.btn_collect = Button(self.frame_footer,text=u"收集",height=2,width=5,fg="red",font = ('Arial',10),command=self.getData)
        self.btn_collect.grid(row=0,column=0,padx=5,sticky=N+S)
        self.btn_send = Button(self.frame_footer,text=u"上报",height=2,width=5,fg="green",font = ('Arial',10),state="disabled",command=self.sendData)
        self.btn_send.grid(row=0,column=1,padx=5,sticky=N+S)
        self.btn_clear = Button(self.frame_footer,text=u"清空",height=2,width=5,fg="blue",font = ('Arial',10),command=self.clearData)
        self.btn_clear.grid(row=0,column=2,padx=5,sticky=N+S)


    def getData(self):
        _data = collect()
        print(_data)
        self.text_info.delete(0.0,END)
        self.text_info.insert(0.0,_data)
        self.btn_send.config(state="normal")

    def clearData(self):
        self.text_info.delete(0.0,END)
        self.btn_send.config(state="disabled")

    def sendData(self):
        _success = True
        if _success == True:
            messagebox.showinfo(u'上报结果', u'上报成功')
        else:
            messagebox.showerror(u'上报结果', u'上报失败')

def main():
    obj = Systeminfo()
    # obj.root.mainloop()
    mainloop()

if __name__ == '__main__':
    main()
