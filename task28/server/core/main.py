from core.user_handle import UserHandle
from core.server import FTPServer
from lib import common
import time, sys, queue
import time
import multiprocessing
from multiprocessing.managers import BaseManager

logger=common.get_logger(__name__)


# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


# 第一步：使用QueueManager注册用于获取Queue的方法名称
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 第二步：连接服务器
server_addr = '127.0.0.1'



class Manager():
    def __init__(self):
        pass



    def start_ftp(self):
        server = FTPServer()
        server.run()
        server.close()

    def create_user(self):
        username = input('username>>>:').strip()
        UserHandle(username).add_user()

    def quit_func(self):
        quit('bye bye ...')

    def run(self):
        msg = '''
        1.启动ftp服务器
        2.创建用户
        3.退出\n
        '''
        msg_dic = {'1': 'start_ftp', '2': 'create_user', '3': 'quit_func'}
        while True:
            pool = multiprocessing.Pool(processes=3)
            msg1 = 'test:'
            print(msg)
            num = input('num>>>:').strip()

            if num in msg_dic:
                if num == '1':
                    logger.info('启动服务器')
                elif num == '2':
                    logger.info('创建用户')
                elif num == '3':
                    logger.info('退出')
                else:
                    logger.warning('输入错误字符')
                
                pool.apply_async(getattr(self, msg_dic[num])(), (msg1,))
                # 端口和验证口令注意保持与服务进程完全一致
                m = QueueManager(address=(server_addr, 8080), authkey=b'aaaa')

                # 从网络连接
                m.connect()

                task = m.get_task_queue()
                result = m.get_result_queue()
                #while not task.empty():
                a, c = task.get(True, timeout=10)
                b = getattr(a, c[0])
                print(b)
                result.put(b)
            else:
                print('请重新选择')
                logger.warning('输入错误字符')