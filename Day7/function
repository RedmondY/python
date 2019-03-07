# 1、写函数，，用户传入修改的文件名，与要修改的内容，执行函数，完成批了修改操作
import os
def fuc1(file,val,map):
    f_1 = open(file,'r')
    f_2 = open('b.txt','w')
    for line in f_1.readlines():
        lines = line.replace(val,map)
        f_2.write(lines)
    f_1.close()
    f_2.close()
    os.remove(file)
    os.rename('b.txt',file)
# fuc1('a.txt','s','b')
# 2、写函数，计算传入字符串中【数字】、【字母】、【空格] 以及 【其他】的个数
def fuc2(str):
    dig = 0
    dic = 0
    blank = 0
    other = 0
    for s in str:
        if '0'<=s and s<='9':
            dig+=1
        elif ('a'<=s and s<='z') or ('A'<=s and s<='Z'):
            dic+=1
        elif s==' ':
            blank+=1
        else:
            other+=1
    return dig,dic,blank,other
# print(fuc2('assssa 11234 __'))
# 3、写函数，判断用户传入的对象（字符串、列表、元组）长度是否大于5。
def fuc3(str):
    num=0
    for s in str:
        num+=1
    if num>5:
        print('>5')
        return True
    else:
        print('<5')
        return False
# print(fuc3([1,2,3,4,5]))
# print(fuc3('aaasdf'))
# 4、写函数，检查传入列表的长度，如果大于2，那么仅保留前两个长度的内容，并将新内容返回给调用者。
def fuc4(list):
    new = []
    for i in range(len(list)):
        if i<2:
            new.append(list[i])
    return new
# print(fuc4([1,3,4,5]))

# 5、写函数，检查获取传入列表或元组对象的所有奇数位索引对应的元素，并将其作为新列表返回给调用者。
def fuc5(list):
    new = []
    for i in range(len(list)):
        if i%2==0:
            new.append(list[i])
    return new
# print(fuc5([1,2,3,4,6,7,0]))
# 6、写函数，检查字典的每一个value的长度,如果大于2，那么仅保留前两个长度的内容，并将新内容返回给调用者。
# dic = {"k1": "v1v1", "k2": [11,22,33,44]}
# PS:字典中的value只能是字符串或列表
def fuc6(dict):
    new = {}
    for ke in dict.keys():
        dict[ke] = fuc4(dict[ke])#应该分字符串和列表分开
    return dict
dic = {"k1": "v1v1", "k2": [11,22,33,44]}
print(fuc6(dic))
