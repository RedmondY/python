# 1. 使用__new__实现
import threading
class Singleton(object):
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instance

obj1 = Singleton()
print(obj1)

def task(arg):
    obj = Singleton()
    print(obj)

for i in range(10):
    t = threading.Thread(target=task,args=[i,])
    t.start()

#2、使用__metaclass__

class Singleton2(type):
    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        return cls._instance


class Create2(metaclass=Singleton2):
    s = 111


a = Create2()
b = Create2()
b.s = 323
print(a is b, a.s)


# 3、装饰器
def Singleton3(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton

@Singleton
class A(object):
    a = 1
    def __init__(self, x=0):
        self.x = x

a1 = A(2)
a2 = A(3)

#4、使用模块
#其实，Python 的模块就是天然的单例模式，因为模块在第一次导入时，
#会生成 .pyc 文件，当第二次导入时，就会直接加载 .pyc 文件，
#而不会再次执行模块代码。
class Singleton4(object):
    def foo(self):
        pass
singleton = Singleton4()
#将上面的代码保存在文件中，使用时，直接在其他文件中导入此文件中的对象
from a import singleton
