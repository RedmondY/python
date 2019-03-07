import time
import random
# 1 编写函数，（函数执行的时间是随机的）
def fun():
    time.sleep(random.randomrange(1,4))
    print(random.randomrange(1,4))
fun()
