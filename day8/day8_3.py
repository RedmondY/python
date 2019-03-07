import time
import random

# 3 编写装饰器，为函数加上认证的功能
def auth(dirver='file'):
    def auth2(func):
        def wrapper(*args,**kwargs):
            name = input("user:")
            pwd = input("pwd:")
 
            if dirver == 'file':
                if name == 'egon' and pwd == '123':
                    print('登录成功')
                    res = func(*args,**kwargs)
                    return res
                else:
                    res = '用户名或密码错误！'
                    print(res)
            elif dirver == 'ldap':
                print('ldap')
        return wrapper
    return auth2
 
@auth(dirver='file')
def foo(name):
    print(name)
 
foo('egon')