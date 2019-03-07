import time,random
db = 'db.txt'
login_status = {'user':None,'status':False,'login_time':None,'timeout':2}
 
def timeer(func):
    def wrapper(*args,**kwargs):
        s1 = time.time()
        res = func(*args,**kwargs)
        s2 = time.time()
        print('%s' %(s2-s1))
        return res
    return wrapper
 
def auth(auth_type='file'):
    def auth2(func):
        def warpper(*args,**kwargs):
            if auth_type == 'file':
                if login_status['user']:
                    timeout = time.time()-login_status['login_time']
                    if timeout < login_status['timeout']:
                        return func(*args, **kwargs)
                tag = True
                while tag:
                    with open(db,'r',encoding='utf-8') as read_f:
                        dic = eval(read_f.read())
                    name = input('请输入用户名：').strip()
                    passwd = input('请输入密码：').strip()
                    if name in dic and passwd == dic[name]:
                        login_status['user'] = name
                        login_status['status'] = True
                        login_status['login_time'] = time.time()
                        res = func(*args,**kwargs)
                        tag = False
                        return res
                    else:
                        print('您输入的用户名或密码错误！')
            elif auth_type == 'mysql':
                pass
        return warpper
    return auth2
 
 
@auth()
def index():
    time.sleep(random.randrange(3))
    print('欢迎来到首页')
 
@auth()
def home(name):
    time.sleep(random.randrange(3))
    print('欢迎来到%s的首页' %name)
 
@auth()
def  shopping(name):
    time.sleep(random.randrange(3))
    print('欢迎来到%s的购物车' %name)
 
@auth()
def order(name):
    time.sleep(random.randrange(3))
    print('欢迎来到%s的订单列表' %name)
 
index()
home('stealth')
shopping('stealth')
order('stealth')
