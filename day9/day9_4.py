import os
def init(func):
    def wrapper(*args,**kwargs):
        g=func(*args,**kwargs)
        next(g)
        return g
    return wrapper
 
@init
def search(target):
    while True:
        filepath=yield
        g=os.walk(filepath)
        for dirname,_,files in g:
            for file in files:
                abs_path=r'%s\%s' %(dirname,file)
                target.send(abs_path)
@init
def opener(target):
    while True:
        abs_path=yield
        with open(abs_path,'rb') as f:
            target.send((f,abs_path))
@init
def cat(target):
    while True:
        f,abs_path=yield
        for line in f:
            res=target.send((line,abs_path))
            if res:
                break
@init
def grep(pattern,target):
    tag=False
    while True:
        line,abs_path=yield tag
        tag=False
        if pattern.encode('utf-8') in line:
            target.send(abs_path)
            tag=True
@init
def printer():
    while True:
        abs_path=yield
        print(abs_path)
 
 
g=search(opener(cat(grep('你好',printer()))))
# g.send(r'E:\CMS\aaa\db')
g=search(opener(cat(grep('python',printer()))))
g.send(r'E:\CMS\aaa\db')
--------------------- 
作者：weixin_34191845 
来源：CSDN 
原文：https://blog.csdn.net/weixin_34191845/article/details/87569247 
版权声明：本文为博主原创文章，转载请附上博文链接！