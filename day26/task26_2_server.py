from socket import *
import subprocess
from struct import *
import json

server = socket(AF_INET, SOCK_STREAM)
server.bind(('127.0.0.1', 8081))
server.listen(5)

# 链接循环
while True:
    conn, client_addr = server.accept()
    print(client_addr)

    # 通信循环
    while True:
        try:
            cmd = conn.recv(512) 
            if len(cmd) == 0: break
            obj = subprocess.Popen(cmd.decode('utf-8'),
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE
                                   )
            stdout = obj.stdout.read()
            stderr = obj.stderr.read()
            # 1. 先制作报头
            header_dic = {
                'filename': 'a.txt',
                'md5': 'qwerqwerqwee123123x1',
                'total_size': len(stdout) + len(stderr)
            }
            header_json = json.dumps(header_dic)
            header_bytes = header_json.encode('utf-8')

            # 2. 先发送4个bytes(包含报头的长度)
            conn.send(pack('i', len(header_bytes)))
            # 3  再发送报头
            conn.send(header_bytes)

            # 4. 最后发送真实的数据
            conn.send(stdout)
            conn.send(stderr)
        except ConnectionResetError:
            break

    conn.close()

server.close()