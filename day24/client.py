###客户端
from socket import *
ip_port=('127.0.0.1',8080)
back_log=5
buffer_size=1024
tcp_client=socket(AF_INET,SOCK_STREAM)
data=tcp_client.connect(ip_port)
while True:
    cmd=input('>>').strip()
    if not cmd: continue
    if cmd == 'quit': break
    tcp_client.send(cmd.encode('gbk'))
    com_res=tcp_client.recv(buffer_size)
    print('命令的执行结果是:',com_res.decode('gbk'))
 
tcp_client.close()
