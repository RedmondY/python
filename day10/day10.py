# 1、将names=['albert','james','kobe','kd']中的名字全部变大写

names=['albert','james','kobe','kd']
names=[name.upper() for name in names]  #应记住的表达方式，很python
print(names)
　　

# 2、将names=['albert','jr_shenjing','kobe','kd']中以shenjing结尾的名字过滤掉，然后保存剩下的名字长度

names=['albert','jr_shenjing','kobe','kd']
names=[len(name) for name in names if not name.endswith('shenjing')]
print(names)
　　

# 3、求文件a.txt中最长的行的长度（长度按字符个数算，需要使用max函数）

with open('access.log',encoding='utf-8') as f:
    print(max(len(line) for line in f))
　　


# 4、求文件a.txt中总共包含的字符个数？思考为何在第一次之后的n次sum求和得到的结果为0？（需要使用sum函数）

with open('access.log', encoding='utf-8') as f:
    print(sum(len(line) for line in f))
    f.seek(0)
    print(sum(len(line) for line in f))
    f.seek(0)
    print(sum(len(line) for line in f))