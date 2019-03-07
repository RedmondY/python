'''
代码优化
如下示例, 在没有学习类这个概念时，数据与功能是分离的,请用面向对象的形式优化以下代码：

def exc1(host,port,db,charset):  
    conn=connect(host,port,db,charset)   
    conn.execute(sql)
    return xxx
def exc2(host,port,db,charset,proc_name):
    conn=connect(host,port,db,charset)
    conn.call_proc(sql)
    return xxx 

# 每次调用都需要重复传入一堆参数
exc1('127.0.0.1',3306,'db1','utf8','select * from tb1;')
exc2(‘127.0.0.1’,3306,'db1','utf8','存储过程的名字')
'''

class Try:
    def __init__(self, host, port, db, charset):
        self.host = host
        self.port = port
        self.db = db
        self.charset = charset

    def exc1(self, sql):
        conn = connect(self.host, self.port, self.db, self.charset)
        conn.execute(sql)
        return None

    def exc2(self, proc_name):
        conn = connect(self.host, self.port, self.db, self.charset)
        conn.call_proc(proc_name)
        return None

# 调用
try1 = Try('127.0.0.1', 3306, 'db1', 'utf8')
try1.exc1('select * from tb1;')
try1.exc2('存储过程的名字')

#print(try1)