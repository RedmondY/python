# 模拟管道，实现功能:tail -f access.log | grep '404'
import time
def tail(filepath):
    with open(filepath,'rb') as f:
        f.seek(0,2)
        while True:
            line=f.readline()
            if line:
                #print(line)
                yield line
            else:
                #continue
                time.sleep(0.05)

def grep(pattern,lines):
    for line in lines:
        line=line.decode('utf-8')
        if pattern in line:
            yield line

for line in grep('404',tail('access.log')):
    print(line,end='')

# 输入字符的py程序
with open('access.log','a',encoding='utf-8') as f:
    f.write('出错啦404\n')
    f.flush()