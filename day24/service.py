### 服务端
from socket import *
import subprocess
 
ip_port=('127.0.0.1',8080)
back_log=5
buffer_size=1024
 
tcp_server=socket(AF_INET,SOCK_STREAM)
tcp_server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
tcp_server.bind(ip_port)
tcp_server.listen(5)
while True:
    conn,addr=tcp_server.accept()
    print('客户端链接',addr)
    while True:
        try:
            cmd=conn.recv(buffer_size)
            if not cmd: break
            print('收到客户端命令',cmd)
            res=subprocess.Popen(cmd.decode('gbk'),shell=True,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            err=res.stderr.read()
            if err:
                com_res=err
 
            else:
                com_res=res.stdout.read()
 
            conn.send(com_res)
        except Exception as e:
            print(e)
            break
 
conn.close()
tcp_server.close()
 
