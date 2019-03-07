from socket import *
import threading
host = '1111' 
port = 8888 
bufsize = 1024
addrlist = list()
addr = (host,port)
udpServer = socket(AF_INET,SOCK_DGRAM)
udpServer.bind(addr) #绑定地址
while True:
    data,clientaddr = udpServer.recvfrom(bufsize)  #接收数据 自动阻塞 等待客户端请求:
    data = data.decode(encoding='utf-8')
    print('客户端的来信：',data,clientaddr)
    if clientaddr not in addrlist:
        addrlist.append(clientaddr)
    for i in addrlist:
        udpServer.sendto(data.encode(encoding='utf-8'),i)
udpServer.close()