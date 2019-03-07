import os, socket
import struct, pickle, time
import hashlib, subprocess
import queue
from conf import settings
from core.user_handle import UserHandle
from lib import common
from threading import Thread, Lock
from socketserver import BaseRequestHandler

logger=common.get_logger(__name__)

class FTPServer():
    MAX_SOCKET_LISTEN = 5
    MAX_RECV_SIZE = 8192

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((settings.HOST, settings.PORT))
        self.socket.listen(self.MAX_SOCKET_LISTEN)
        self.q = queue.Queue(settings.MAX_CONCURRENT_COUNT)  #可以配置最大并发数

    def server_accept(self):
        print('starting...')
        while True:
            self.conn,self.client_addr = self.socket.accept()
            print('客户端地址:', self.client_addr)
            logger.info('输出客户端地址')

            try:
                t = Thread(target=self.server_handle, args=(self.conn, ))
                self.q.put(t)
                t.start()
            except Exception as e:
                print(e)
                logger.warning('warn')
                self.conn.close()
                self.q.get()

    def get_recv(self):
        return pickle.loads(self.conn.recv(self.MAX_RECV_SIZE))

    def get_time(self):
        message = self.get_recv()
        i1, i2, message = struct.unpack('!2b8s', message)
        if i1 == 3 and i2 == 7 and message == 'get_time':
            cur_time = int(time.time())
            response = struct.pack('>2bi', i1, i2, cur_time)
            self.conn.sendall(response)
            logger.info(" Message: %s" % (cur_time))
        else:
            logger.error("Message Error!")

    def auth(self):
        while True:
            user_dic = self.get_recv()
            
            username = user_dic.get('username')
            user_handle = UserHandle(username)
            user_data = user_handle.judge_user()
            if user_data:
                if user_data[0][1] == hashlib.md5(user_dic.get('password').encode('utf-8')).hexdigest():  # 密码也相同
                    self.conn.send(struct.pack('i', 1)) 
                    self.username = username
                    self.homedir_path = '%s\%s\%s'%(settings.BASE_DIR, 'home', self.username)
                    os.chdir(self.homedir_path)
                    self.quota_bytes = int(user_data[2][1]) * 1024 * 1024 
                    user_info_dic = {
                        'username': username,
                        'homedir': user_data[1][1],
                        'quota': user_data[2][1]
                    }
                    self.conn.send(pickle.dumps(user_info_dic)) 
                    return True
                else:
                    self.conn.send(struct.pack('i', 0)) 
                    logger.info('send')
            else:
                self.conn.send(struct.pack('i', 0))
                logger.info('send')

    def readfile(self):
        with open(self.filepath, 'rb') as f:
            filedata = f.read()
            logger.info('readfile')
        return filedata

    def getfile_md5(self):
        logger.info('getfile md5')
        return hashlib.md5(self.readfile()).hexdigest()


    # download
    def get(self):
        if len(self.cmds) > 1:
            filename = self.cmds[1]
            filepath = os.path.join(os.getcwd(), filename)
            if os.path.isfile(filepath):
                exist_file_size = struct.unpack('i', self.conn.recv(4))[0]
                self.filepath = filepath
                header_dic = {
                    'filename': filename,
                    'file_md5': self.getfile_md5(),
                    'file_size': os.path.getsize(self.filepath)
                }
                header_bytes = pickle.dumps(header_dic)
                if exist_file_size: 
                    self.conn.send(struct.pack('i', len(header_bytes)))
                    self.conn.send(header_bytes)
                    if exist_file_size != os.path.getsize(self.filepath):
                        with open(self.filepath, 'rb') as f:
                            f.seek(exist_file_size)
                            for line in f:
                                self.conn.send(line)
                    else:
                        print('断点和文件本身大小一样')
                        logger.info('断点和文件本身大小一样')
                else:
                    self.conn.send(struct.pack('i', len(header_bytes)))
                    self.conn.send(header_bytes)
                    with open(self.filepath, 'rb') as f:
                        for line in f:
                            self.conn.send(line)
            else:
                print('当前目录下文件不存在')
                logger.warning('当前目录下文件不存在')
                self.conn.send(struct.pack('i',0))
        else:
            print('用户没有输入文件名')
            logger.warning('用户没有输入文件名')

    def recursion_file(self,menu):
        res = os.listdir(menu) #指定目录下所有的文件和和目录名
        for i in res:
            path = '%s\%s' % (menu, i)
            if os.path.isdir(path):#判断指定对象是否为目录
                self.recursion_file(path)
            elif os.path.isfile(path):
                self.home_bytes_size += os.path.getsize(path)

    def current_home_size(self):
        self.home_bytes_size = 0
        self.recursion_file(self.homedir_path)
        print('字节：', self.home_bytes_size)  # 单位是字节
        home_m_size = round(self.home_bytes_size / 1024 / 1024, 1)
        print('单位M:', home_m_size)  # 单位时 M

    def put(self):
        if len(self.cmds) > 1:
            state_size = struct.unpack('i', self.conn.recv(4))[0]
            if state_size:
                self.current_home_size()
                header_bytes = self.conn.recv(struct.unpack('i', self.conn.recv(4))[0])
                header_dic = pickle.loads(header_bytes)
                print(header_dic)
                filename = header_dic.get('filename')
                file_size = header_dic.get('file_size')
                file_md5 = header_dic.get('file_md5')

                upload_filepath = os.path.join(os.getcwd(), filename)
                self.filepath = upload_filepath  # 为了全局变量读取文件算md5时方便
                if os.path.exists(upload_filepath):  #文件已经存在
                    self.conn.send(struct.pack('i', 1))
                    has_size = os.path.getsize(upload_filepath)
                    if has_size == file_size:
                        print('文件已经存在')
                        logger.warning('文件已经存在')
                        self.conn.send(struct.pack('i', 0))
                    else: 
                        self.conn.send(struct.pack('i', 1))
                        if self.home_bytes_size + int(file_size - has_size) > self.quota_bytes:
                            print('超出了用户的配额')
                            logger.warning('超出了用户的配额')
                            self.conn.send(struct.pack('i', 0))
                        else:
                            self.conn.send(struct.pack('i', 1))
                            self.conn.send(struct.pack('i', has_size))
                            with open(upload_filepath, 'ab') as f:
                                f.seek(has_size)
                                while has_size < file_size:
                                    recv_bytes = self.conn.recv(self.MAX_RECV_SIZE)
                                    f.write(recv_bytes)
                                    has_size += len(recv_bytes)
                                    self.conn.send(struct.pack('i', has_size))

                            if self.getfile_md5() == file_md5:
                                print('    上传成功     ')
                                logger.info('    上传成功     ')
                                self.conn.send(struct.pack('i', 1))
                            else:
                                print('    上传失败     ')
                                logger.warning('    上传失败     ')
                                self.conn.send(struct.pack('i', 0))
                else:  #第一次上传
                    self.conn.send(struct.pack('i', 0))
                    if self.home_bytes_size + int(file_size) > self.quota_bytes:
                        print('超出了用户的配额')
                        logger.warning('超出了用户的配额')
                        self.conn.send(struct.pack('i', 0))
                    else:
                        self.conn.send(struct.pack('i', 1))
                        with open(upload_filepath, 'wb') as f:
                            recv_size = 0
                            while recv_size < file_size:
                                file_bytes = self.conn.recv(self.MAX_RECV_SIZE)
                                f.write(file_bytes)
                                recv_size += len(file_bytes)
                                self.conn.send(struct.pack('i', recv_size))

                        if self.getfile_md5() == file_md5: 
                            print('    上传成功     ')
                            logger.info('    上传成功     ')
                            self.conn.send(struct.pack('i', 1))
                        else:
                            print('    上传失败     ')
                            logger.warning('    上传失败     ')
                            self.conn.send(struct.pack('i', 0))
            else:
                print('待传的文件不存在')
                logger.warning('待传的文件不存在')
        else:
            print('用户没有输入文件名')
            logger.warning('用户没有输入文件名')

    def ls(self):
        subpro_obj = subprocess.Popen('dir', shell=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        stdout = subpro_obj.stdout.read()
        stderr = subpro_obj.stderr.read()
        self.conn.send(struct.pack('i', len(stdout + stderr)))
        self.conn.send(stdout)
        self.conn.send(stderr)

    def cd(self):
        """切换目录"""
        if len(self.cmds) > 1:
            dir_path = os.path.join(os.getcwd(), self.cmds[1])
            if os.path.isdir(dir_path): #查看是否是目录名
                previous_path = os.getcwd()  #拿到当前工作的目录
                os.chdir(dir_path) #改变工作目录到...
                target_dir = os.getcwd()
                if self.homedir_path in target_dir:  #判断homedir_path是否在目标目录
                    print('切换成功')
                    logger.info('切换成功')
                    self.conn.send(struct.pack('i', 1)) #切换成功返回1
                else:
                    print('切换失败')  # 切换失败后,返回到之前的目录下
                    logger.warning('切换失败')

                    os.chdir(previous_path)
                    self.conn.send(struct.pack('i', 0))
            else:
                print('要切换的目录不在该目录下')
                logger.warning('要切换的目录不在该目录下')

                self.conn.send(struct.pack('i', 0))
        else:
            print('没有传入切换的目录名')
            logger.warning('没有传入切换的目录名')


    def server_handle(self, conn):
        if self.auth():
            print('    用户登录成功     ')
            logger.info('    用户登录成功     ')
            while True:
                try: 
                    user_input = self.conn.recv(self.MAX_RECV_SIZE).decode('utf-8')
                    self.cmds = user_input.split()
                    if hasattr(self,self.cmds[0]):
                        getattr(self,self.cmds[0])()
                    else:
                        print('      请用户重复输入     ')
                        logger.info('    请用户重复输入     ')
                except Exception:
                    break

    def run(self):
        self.server_accept()

    def close(self):
        self.socket.close()

