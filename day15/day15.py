'''
1.根据姓名查看学生所有成绩
2.查看所有人的某学科成绩
3.查看总平均分
4.查看某人的某学科成绩
5.根据姓名删除学生信息
'''
class student:
    school = 'deepshare'
    def __init__(self,name,nianji,math,english):
        self.name = name
        self.nianji = nianji
        self.math = math
        self.english = english
 
    def get_name(self):
        return self.name
 
    def get_nianji(self):
        return self.nianji
 
    def get_math(self):
        return self.math
 
    def get_english(self):
        return self.english
 
    def print_all_score(self):
        print('%s的数学成绩：%3d,语文成绩：%3d'%(self.name,
                                      self.math,
                                      self.english))
 
    def print_one_score(self,subject):
        if subject == 'math':
            print ('%s的数学成绩：%3d'%(self.name,
                                  self.math))
        elif subject == 'english':
            print('%s的语文成绩：%3d'%(self.name,
                                 self.english))
                                 
    def delete(self):
        print("删除%s的成绩".center(50,'=')%(self.name))
        if self.english:
            del self.english
        if self.math:
            del self.math
 
 
stu1 = student('A',1,100,90)
stu2 = student('B',2,90,100)
stu3 = student('C',3,60,70)
stu = {stu1, stu2, stu3}
print (type(stu))
 
#查看所有成绩
for astu in stu:
    astu.print_all_score()
print ('='*20)
 
# 查看所有人的某学科成绩
for astu in stu:
    astu.print_one_score('math')
print ('='*20)
# .查看总平均分
total = 0
num = 0
for astu in stu:
    total += astu.get_math()
    total += astu.get_english()
    num += 2
print('总平均分',total/num)
print ('='*20)
#4.查看某人的某学科成绩
name = 'A'
xueke = 'math'
for astu in stu:
    if name == astu.get_name():
        astu.print_one_score(xueke)
print ('='*20)
#5.根据姓名删除学生信息
name1 = 'C'
for astu in stu:
    astu.print_all_score()
print ('='*20)
stu3.delete()

