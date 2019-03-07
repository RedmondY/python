from socket import *
from struct import *
import json

client = socket(AF_INET, SOCK_STREAM)
client.connect(('127.0.0.1', 8081))

# 通信循环
while True:
    cmd=input('>>: ').strip()
    if len(cmd) == 0:continue
    client.send(cmd.encode('utf-8'))
    #1. 先收4bytes,解出报头的长度
    header_size=unpack('i',client.recv(4))[0]

    #2. 再接收报头,拿到header_dic
    header_bytes=client.recv(header_size)
    header_json=header_bytes.decode('utf-8')
    header_dic=json.loads(header_json)
    print(header_dic)
    total_size=header_dic['total_size']

    #3. 接收真正的数据
    cmd_res=b''
    recv_size=0
    while recv_size < total_size:
        data=client.recv(512)
        recv_size+=len(data)
        cmd_res+=data

    print(cmd_res.decode('gbk'))

client.close()