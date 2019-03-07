import os,sys, socket
import struct, pickle
import hashlib, subprocess
import time
import queue
from lib import common
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support

# 任务个数
task_num = 10

# 定义收发队列
task_queue = queue.Queue(task_num)
result_queue = queue.Queue(task_num)

# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass

def return_task_queue():
    global task_queue
    return task_queue  # 返回发送任务队列
def return_result_queue ():
    global result_queue
    return result_queue # 返回接收结果队列



logger=common.get_logger(__name__)

class FTPClient():
    HOST = '127.0.0.1'  # 服务端的IP
    SSHHOST = '127.0.1.1'  # 处理端的IP
    PORT = 8080  # 服务端的端口
    SSHPORT = 8088  # 服务端的端口
    MAX_RECV_SIZE = 8192
    DOWNLOAD_PATH =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download')
    UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
        self.ntp(self.socket)

    def connect(self):
        try:
            self.socket.connect((self.HOST, self.PORT))
        except Exception:
            exit('      server还未启动      ')
            logger.info('      server还未启动      ')
    
    def ntp(self, sock):
        message = struct.pack(b'>2b8s', 3, 7, b'get_time')
        try:
            sock.sendall(message)
            response = sock.recv(self.MAX_RECV_SIZE)
            i1, i2, cur_time = struct.unpack('!2bi', response)
            formattime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(cur_time)))
            ret = subprocess.call('date -s %s' %(formattime), shell=True)
            print("client received: %s format: %s" % (response, formattime))
            logger.info("client received: %s format: %s" % (response, formattime))
        except(Exception):
            print("遇到错误")
            logger.warning('warning')
        else:
            sock.close()
            return ret

    def get_recv(self):
        return pickle.loads(self.socket.recv(self.MAX_RECV_SIZE))

    def auth(self):
        count = 0
        while count < 3:
            name = input('username>>>:').strip()
            if not name: continue
            password = input('password>>>:').strip()
            user_dic = {
                'username': name,
                'password': password
            }
            self.socket.send(pickle.dumps(user_dic)) #把用户名和密码发送给server
            res = struct.unpack('i',self.socket.recv(4))[0]
            if res:  #接收返回的信息，并判断
                print('welcome'.center(20,'-'))
                user_info_dic = self.get_recv()
                self.username = user_info_dic.get('username')
                print(user_info_dic)
                return True
            else:
                print('      用户名或密码不对!      ')
                logger.warning('      用户名或密码不对!      ')
            count += 1
 
    def readfile(self):
        with open(self.filepath, 'rb') as f:
            filedata = f.read()
        return filedata

    def getfile_md5(self):
        return hashlib.md5(self.readfile()).hexdigest()

    def progress_bar(self, num, get_size, file_size):
        float_rate = get_size / file_size
        rate = round(float_rate * 100,2)

        if num == 1:  #1表示下载
            sys.stdout.write('\r已下载:      {0}%      '.format(rate))
        elif num == 2:  #2 表示上传
            sys.stdout.write('\r已上传:      {0}%      '.format(rate))
        sys.stdout.flush()

    def get(self):
        if len(self.cmds) > 1:
            filename = self.cmds[1]
            self.filepath = os.path.join(self.DOWNLOAD_PATH, filename) #结合目录名和文件名
            if os.path.isfile(self.filepath): #如果文件存在 支持断点续传
                temp_file_size = os.path.getsize(self.filepath)
                self.socket.send(struct.pack('i', temp_file_size))
                header_size = struct.unpack('i', self.socket.recv(4))[0]
                if header_size: #如果存在
                    header_dic = pickle.loads(self.socket.recv(header_size))
                    print(header_dic)
                    filename = header_dic.get('filename')
                    file_size = header_dic.get('file_size')
                    file_md5 = header_dic.get('file_md5')

                    if temp_file_size == file_size:
                        print('      文件已存在      ')
                        logger.info('      文件已存在      ')
                    else:
                        print('      正在进行断点续传...      ')
                        logger.info('      正在进行断点续传...      ')
                        download_filepath = os.path.join(self.DOWNLOAD_PATH, filename)
                        with open(download_filepath, 'ab') as f:
                            f.seek(temp_file_size)
                            get_size = temp_file_size
                            while get_size < file_size:
                                file_bytes = self.socket.recv(self.MAX_RECV_SIZE)
                                f.write(file_bytes)
                                get_size += len(file_bytes)
                                self.progress_bar(1, get_size, file_size)  # 1表示下载

                        if self.getfile_md5() == file_md5:  #判断下载下来的文件MD5值和server传过来的MD5值是否一致
                            print('\n      下载成功      ')
                            logger.info('\n      下载成功      ') 
                        else:
                            print('\n      下载文件大小与源文件大小不一致，请重新下载，将会支持断点续传      ')
                            logger.info('\n      下载文件大小与源文件大小不一致，请重新下载，将会支持断点续传      ')
                else:
                    print('      该文件,之前被下载了一部分,但是server端的该文件,已被删除,无法再次下载      ')
                    logger.info('      该文件,之前被下载了一部分,但是server端的该文件,已被删除,无法再次下载      ')
            else:  #文件第一次下载
                self.socket.send(struct.pack('i', 0))  # 0表示之前没有下载过
                header_size = struct.unpack('i', self.socket.recv(4))[0]
                if header_size:
                    header_dic = pickle.loads(self.socket.recv(header_size))
                    print(header_dic)
                    filename = header_dic.get('filename')
                    file_size = header_dic.get('file_size')
                    file_md5 = header_dic.get('file_md5')

                    download_filepath = os.path.join(self.DOWNLOAD_PATH, filename)
                    with open(download_filepath, 'wb') as f:
                        get_size = 0
                        while get_size < file_size:
                            file_bytes = self.socket.recv(self.MAX_RECV_SIZE)
                            f.write(file_bytes)
                            get_size += len(file_bytes)
                            self.progress_bar(1, get_size, file_size)  #1表示下载
                            print('总大小:%s已下载:%s'% (file_size, get_size))
                    if self.getfile_md5() == file_md5:  #判断下载下来的文件MD5值和server传过来的MD5值是否一致
                        print('\n      恭喜您,下载成功      ')
                        logger.info('\n      恭喜您,下载成功      ')
                    else:
                        print('\n      下载失败，再次下载支持断点续传      ')
                        logger.info('\n      下载失败，再次下载支持断点续传      ')
                else:
                    print('      当前目录下,文件不存在      ')
                    logger.info('      当前目录下,文件不存在      ')
        else:
            print('用户没有输入文件名')
            logger.info('用户没有输入文件名')

    def put(self):
        if len(self.cmds) > 1:  #确保用户输入了文件名
            filename = self.cmds[1]
            filepath = os.path.join(self.UPLOAD_PATH, filename)
            if os.path.isfile(filepath):
                self.socket.send(struct.pack('i', 1))
                self.filepath = filepath
                filesize = os.path.getsize(self.filepath)
                header_dic = {
                    'filename': filename,
                    'file_md5': self.getfile_md5(),
                    'file_size': filesize
                }
                header_bytes = pickle.dumps(header_dic)
                self.socket.send(struct.pack('i', len(header_bytes)))
                self.socket.send(header_bytes)

                state = struct.unpack('i', self.socket.recv(4))[0]
                if state:  #已经存在了
                    has_state = struct.unpack('i', self.socket.recv(4))[0]
                    if has_state:
                        quota_state = struct.unpack('i', self.socket.recv(4))[0]
                        if quota_state:
                            has_size = struct.unpack('i', self.socket.recv(4))[0]
                            with open(self.filepath, 'rb') as f:
                                f.seek(has_size)
                                for line in f:
                                    self.socket.send(line)
                                    recv_size = struct.unpack('i', self.socket.recv(4))[0]
                                    self.progress_bar(2, recv_size, filesize)
                            success_state = struct.unpack('i', self.socket.recv(4))[0]
                            if success_state == filesize:
                                success_state = struct.unpack('i', self.socket.recv(4))[0]

                            if success_state:
                                print('\n      恭喜您，上传成功      ')
                            else:
                                print('\n      上传失败      ')
                        else: #超出了配额
                            print('      超出了用户的配额      ')
                    else:  # 存在的大小 和文件大小一致 不必再传
                        print('      当前目录下，文件已经存在      ')
                else:  #第一次传
                    quota_state = struct.unpack('i', self.socket.recv(4))[0]
                    if quota_state:
                        with open(self.filepath, 'rb') as f:
                            send_bytes = b''
                            for line in f:
                                self.socket.send(line)
                                send_bytes += line
                                print('总大小:%s 已上传:%s' % (filesize, len(send_bytes)))

                                recv_size = struct.unpack('i', self.socket.recv(4))[0]
                                self.progress_bar(2, recv_size, filesize)

                        success_state = struct.unpack('i', self.socket.recv(4))[0]

                        if success_state == filesize:
                            success_state = struct.unpack('i', self.socket.recv(4))[0]

                        if success_state:
                            print('\n      恭喜您，上传成功      ')
                        else:
                            print('\n      上传失败      ')
                    else:  # 超出了配额
                        print('      超出了用户的配额      ')
            else:  #文件不存在
                print('      文件不存在      ')
                self.socket.send(struct.pack('i', 0))
        else:
            print('用户没有输入文件名')

    def ls(self):
        dir_size = struct.unpack('i', self.socket.recv(4))[0]
        recv_size = 0
        recv_bytes = b''
        while recv_size < dir_size:
            temp_bytes = self.socket.recv(self.MAX_RECV_SIZE)
            recv_bytes += temp_bytes
            recv_size += len(temp_bytes)
        print(recv_bytes.decode('gbk'))  # gbk适合windows utf-8 适合linux

    def cd(self):
        if len(self.cmds) > 1:
            res = struct.unpack('i', self.socket.recv(4))[0]
            if res:
                print('      切换成功      ')
            else:
                print('      切换失败      ')
        else:
            print('没有输入要切换的目录名')


    def interactive(self):

        if self.auth():
            while True:
                QueueManager.register('get_task_queue', callable=return_task_queue)   
                QueueManager.register('get_result_queue', callable=return_result_queue)

                manager = QueueManager(address=('127.0.1.1', 8081), authkey=b'aaaa')

                # 启动
                manager.start()
                
                task = manager.get_task_queue()
                result = manager.get_result_queue()

                try:
                    n = task.get(timeout = 1)
                    user_input = input('[%s]>>>:'%self.username)
                    if not user_input: continue
                    self.socket.send(user_input.encode('utf-8'))
                    self.cmds = user_input.split()
                    c = self.cmds
                    if hasattr(self, self.cmds[0]):
                        getattr(self, self.cmds[0])
                        task.put(self, c)
                    else:
                        print('请重新输入')
                    a = result.get(timeout=1)
                    a()
                    
                except Exception as e:  # server关闭了
                    print(e)
                    break
                finally:
                    manager.shutdown()
    def close(self):
        self.socket.close()


if __name__ == '__main__':
    freeze_support()
    ftp_client = FTPClient()
    ftp_client.interactive()

    ftp_client.close()