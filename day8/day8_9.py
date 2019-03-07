
import time,os
def logger(logfile):
    def deco(func):
        def wrapper(*args,**kwargs):
            res = func(*args,**kwargs)
            with open(logfile,'a+',encoding='utf-8') as f:
                f.write('%s run\n' %(time.strftime('%Y-%m-%d %X')))
            return res
        return wrapper
    return deco
 
 
 
@logger('log1.txt')
def index():
    print('欢迎来到首页')
 
index()
time.sleep(3)
index()
time.sleep(3)
index()