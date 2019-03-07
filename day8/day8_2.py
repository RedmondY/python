import time

# 2 编写装饰器，为函数加上统计时间的功能

def timmer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        res = func(*args,**kwargs)
        stop_time = time.time()
        print('函数运行时间是：%s' %(stop_time-start_time))
        return res
    return wrapper
 
@timmer
def foo():
    time.sleep(2)
    print('这个是foo运行的结果')

