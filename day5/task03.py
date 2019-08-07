import sys  # 首先导入这个模块

list_test = sys.argv

with open('test03.txt', 'w+', ) as f:
    f.seek(0, 0)
    print(f.tell())
    f.write('[txt]')
