import time
import random

# 4 编写装饰器，为多个函数加上认证的功能（用户的账号密码来源于文件）
#    要求：
#        登录成功一次，后续的函数都无需再输入用户名和密码
#    注意：
#        从文件中读出字符串形式的字典，可以用
#        eval('{"name":"albert","password":"123"}')转成字典格式

db = 'db.txt'
login_status = {'user':None,'status':False}
def auth(auth_type='file'):
    def auth2(func):
        def warpper(*args,**kwargs):
            if login_status['user'] and login_status['status']:
                return func(*args,**kwargs)
            if auth_type == 'file':
                tag = True
                while tag:
                    with open(db,'r',encoding='utf-8') as read_f:
                        dic = eval(read_f.read())
                    name = input('请输入用户名：').strip()
                    passwd = input('请输入密码：').strip()
                    if name in dic and passwd == dic[name]:
                        login_status['user'] = name
                        login_status['status'] = True
                        res = func(*args,**kwargs)
                        tag = False
                        return res
                    else:
                        print('您输入的用户名或密码错误！')
            elif auth_type == 'mysql':
                pass
        return warpper
    return auth2
 
 
 
def index():
    print('欢迎来到首页')
 
@auth()
def home(name):
    print('欢迎来到%s的首页' %name)
 
@auth()
def  shopping(name):
    print('欢迎来到%s的购物车' %name)
 
@auth()
def order(name):
    print('欢迎来到%s的订单列表' %name)
 
index()
home('stealth')
shopping('stealth')
order('stealth')
