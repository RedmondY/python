'''
第一题：
使用组合与继承设计一个学生选择课程的程序，使老师和学生初始化都具有课程属性，
但是属性值为空，可以动态添加，可打印出老师教授的的课程和学生学习的课程，
可以打印出课程名字和价格，尽量避免写重复代码
（提示：学生和老师都是属于人，都有课程属性）

'''

class Person:
    def __init__(self, name, tag, lesson=[], fee=[]):
        self.name = name
        self.tag = tag
        self.lesson = lesson
        self.fee = fee

    def addlesson(self, lesson, fee):
        lessonlist = []
        feelist = []
        lessonlist.append(lesson)
        feelist.append(fee)
        for lesson in lessonlist:
            for fee in feelist:
                print("课程信息\n类别: %s\n姓名：%s\n课程名称：%s\n课程价格：%s\n" % (self.tag,self.name,lesson,fee))

class Teacher(Person):
    pass

class Student(Person):
    pass

tea1 = Teacher('Tom','Teacher')
tea1.addlesson('Machine learning',1110)
tea1.addlesson('NLP',1101)
tea1.addlesson('Deep learning', 1011)

stu1 = Student('Jack','Student')
stu1.addlesson('Machine learning',1110)
stu2 = Student('Sam','Student')
stu2.addlesson('NLP',1101)
stu3 = Student('Joe','Student')
stu3.addlesson('Deep learning',1011)