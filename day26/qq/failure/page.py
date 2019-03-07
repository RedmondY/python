from  tkinter import *
from socket import *
import threading

class index(object):
    def __init__(self,  master=None):
        #self.name = name
        self.root = master
        self.root.geometry("800x480") 
        self.bufsize = 1024  
        self.serveraddr = ('127.0.0.1',8888) 
        self.udpClient = socket(AF_INET,SOCK_DGRAM) 
        self.content = list()
        self.createPage()

    def createPage(self):
        self.frame1=Frame(self.root)
        self.frame2=Frame(self.root)
        self.frame1.pack()
        self.frame2.pack(side=BOTTOM)
        self.inp_text=Entry(self.frame2,width=60)
        self.btn = Button(self.frame2,text="发送",width=15,command=self.sendmsg) 
        self.inp_text.pack(side=LEFT)
        self.btn.pack(side=LEFT)

    def sendmsg(self):
        self.get_inp = self.inp_text.get() 
        if self.get_inp:
            #self.get_inp = self.name+':' + self.get_inp 
            self.get_inp = self.get_inp.encode(encoding="utf-8")
            self.udpClient.sendto(self.get_inp,self.serveraddr)
            self.inp_text.delete('0','end')

    def recmsg(self):
        self.data,self.addr = self.udpClient.recvfrom(self.bufsize) 
        self.data = self.data.decode(encoding="utf-8")
        return self.data
 
class myThread(threading.Thread):
    def __init__(self,id,mypage = None):
        self.mypage = mypage    
        threading.Thread.__init__(self)
        self.id=id
    def run(self):
        if self.id == 1:
            while True:
                self.ss = self.mypage.recmsg()
                if  self.ss:
                    print(self.ss)
                    self.mypage.text=Label(self.mypage.frame1,text=self.ss) #创建聊天内容标签
                    self.mypage.text.pack(side=TOP,padx=1)
 
 
 