# 自定义函数模拟range(1,7,2)

def my_range(start,stop,step=1):
    while start<stop:
        yield start
        start+=step
    obj=my_range(1,7,2)
    print(next(obj))
    print(next(obj))
    print(next(obj))
    print(next(obj)) 
#应用于for循环
for i in my_range(1,7,2):
    print(i)