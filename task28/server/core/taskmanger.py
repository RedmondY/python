from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support, Queue

# 任务个数
task_number = 10

# 收发队列
task_quue = Queue(task_number)
result_queue = Queue(task_number)


def get_task():
    return task_queue


def get_result():
    return result_queue


# 创建类似的queueManager
class QueueManager(BaseManager):
    pass


def win_run():
    QueueManager.register('get_task_queue', callable=get_task)
    QueueManager.register('get_result_queue', callable=get_result)
    # 绑定端口和设置验证口令
    manager = QueueManager(address=('127.0.0.1', 8080), authkey='1111'.encode())

    # 启动管理，监听信息通道
    manager.start()

    try:

        # 通过网络获取任务队列和结果队列
        task = manager.get_task_queue()
        result = manager.get_result_queue()

        # 添加任务
        for url in ["ImageUrl_" + str(i) for i in range(10)]:
            print('url is %s' % url)
            task.put(url)

    except:
        print 'Manager error'
    finally:
        manager.shutdown()


if __name__ == '__main__':
    # window下多进程可能有问题，添加这句话缓解
    freeze_support()
    win_run()