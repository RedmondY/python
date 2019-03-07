import time
from socket import *
 
 
def main():
    ip_port = ('127.0.0.1', 8888)
    buffer_size = 1024
 
    s1 = socket(AF_INET,SOCK_DGRAM) #数据报
    s1.bind(ip_port)
 
    while True:
        data,addr=  s1.recvfrom(buffer_size)
        if not data:
            fmt = '%Y-%m-%d %X'
        else:
            fmt = '%'+data.decode('utf-8') #自定义格式
 
        back_time=time.strftime(fmt)
        s1.sendto(back_time.encode('utf-8'),addr)
 
 
 
if __name__ =='__main__':
    main()