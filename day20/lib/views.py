from lib.accounts import *
from lib.schools import *
from lib.courses import *
from lib.classes import *
from lib.db import *
from core.logger import logger


class View(object):
    """ 视图父类 """

    account = Accounts()  # 关联Accounts对象，后续的登录，注册都需要使用
    school = Schools()
    account_storage = inter_db_handler(settings.ACCOUNT_DATABASE)
    base_storage = inter_db_handler(settings.BASE_DATABASE)
    user_data = {'account_id': None,
                 'is_authenticated': False,
                 'account_data': None,
                 }
    base_data = {'school': None,
                 'course': {},
                 'class': {},
                 'teacher': {},
                 'student': {}
                 }
    access_log = logger('access')

    def __init__(self):
        self.menu = None
        self.menu_dict = None
        self.result = None
        self.account_obj = None

    def login(self, account_type):
        exit_flag = True
        while exit_flag:
            if not self.user_data['is_authenticated']:
                username = input('Please input username:').strip()
                password = input('Please input password:').strip()
                account_obj = self.account.getter(username, password)
                if account_obj and account_obj['account_data'].account_type == account_type:  # 判断账户的类型与账户是否存在
                    self.user_data = account_obj
                    self.user_data['is_authenticated'] = True
                    print('\033[%s] Login Success！\033' % username)
                    self.access_log.info('[%s] Login Success!' % username)
                    return self.user_data

                else:
                    print('\033 Username or Password error!\033')
                    return False
            else:
                return self.user_data

    def register(self, account_type, account_status):
        exit_flag = True
        while exit_flag:
            username = input('Please input username:').strip()
            password = input('Please input password:').strip()
            re_password = input('Please input password confirmation:').strip()
            account_obj = self.account.setter(username, password, account_type, account_status)
            if not username or not password:
                print('\033 Error:Username or Password cannot be null!\033')
                continue
            elif username == password:
                print('\033 Error:Username Cannot be equal to Password !\033')
                continue
            elif password != re_password:
                print('\033 Error:Password do not match!\033')
                continue
            elif not account_obj:
                print('\033 The user has already existed!\033')
            else:
                # 注册新账号
                print('\033 Registry Success！\033')
                print('\033 "%s" account login！\033' % username)
                self.user_data['account_id'] = account_obj.id
                self.user_data['is_authenticated'] = True
                self.user_data['account_data'] = account_obj
                self.account_storage.nonquary(account_obj.id, self.user_data)
                exit_flag = False
                # 调试代码

    def tell_info(self):
        """ 展示账户信息方法
            本方法是一个视图，用来展示用户的个人信息。

        :return:
        """
        user_data_obj = self.user_data['account_data']
        user_info_data = user_data_obj.user_info
        # 通过反射，判断user_info_data对象中是否想相应的属性。如有就赋值。如没有设置为Null
        if hasattr(user_info_data, 'name'):
            name = getattr(user_info_data, 'name')
        else:
            name = 'Null'

        if hasattr(user_info_data, 'age'):
            age = getattr(user_info_data, 'age')
        else:
            age = 'Null'

        if hasattr(user_info_data, 'sex'):
            sex = getattr(user_info_data, 'sex')
        else:
            sex = 'Null'

        info = '''
==================账户信息==================
         ID：         \033 :%s\033
         Account：    \033 :%s\033
         Fullname：   \033 :%s\033
         Age：        \033 :%s\033
         Sex：        \033 :%s\033
         Type：       \033 :%s\033
         Status:      \033 :%s\033
============================================
        ''' % (user_data_obj.id, user_data_obj.username, name, age,
               sex, user_data_obj.account_type, user_data_obj.status)
        print(info)

    def set_info(self):
        """ 设置个人信息
        :return:
        """
        exit_flag = True
        while exit_flag:
            fullname = input('Please input your fullname:').strip()
            sex = input('Please input your sex:').strip()
            age = input('Please input your age:').strip()
            account_obj = self.account.set_info(self.user_data['account_data'], fullname, sex, age)
            if account_obj:
                self.user_data['account_data'] = account_obj
                self.account_storage.nonquary(self.user_data['account_id'], self.user_data)
                print('\033 Set Success！\033')
                exit_flag = False
                # 调试代码
                # print(self.user_data)
                # print(self.user_data['account_data'].__dict__)

    def change_password(self):
        """ 修改账号密码视图方法

        :return:
        """
        exit_flag = True
        while exit_flag:
            old_password = input('Please input your old password:').strip()
            new_password = input('Please input your new password:').strip()
            re_new_password = input('Please input your new password confirmation:').strip()
            account_obj = self.account.getter(self.user_data['account_data'].username, old_password)
            if account_obj:
                if not new_password or not re_new_password:
                    print('\033 Error:Password cannot be null!\033')
                elif new_password != re_new_password:
                    print('\033 Error:Password do not match!\033')
                else:
                    result = self.account.change_password(account_obj, new_password)
                    if result:
                        self.account_storage.nonquary(self.user_data['account_id'], result)
                        exit_flag = False
            else:
                print('\033 Error: Old password error!\033')

    def logout(self):
 
        if self.user_data['account_data']:
            username = self.user_data['account_data'].username
            self.user_data = {
                'account_id': None,
                'is_authenticated': False,
                'account_data': None}
            print('\033 [%s] Account logout!\033' % username)
            self.access_log.info('[%s] Account logout!' % username)


    @staticmethod
    def back_off():
        print('\033  Back off!\033')


class StudentView(View):
    """ 学生视图 """
    account = StudentAccounts()
    user_data = {'account_id': None,
                 'is_authenticated': False,
                 'account_data': None,
                 'student_data': {'school': None, 'course': [], 'class': [], 'teacher': []},
                 'study_record': None
                 }

    def __init__(self):
        super(StudentView, self).__init__()

    def register(self, account_type, account_status):
        # 注册视图方法
        print('================创建学生=================')
        # 重用父类的注册账号代码
        super(StudentView, self).register(account_type, account_status)

    def choise_courses(self):
        print('================购买课程=================')
        exit_flag = True
        while exit_flag:
            school_name = input('Please choise school:').strip()
            course_name = input('Please choise course:').strip()
            school_result = self.school.getter(school_name)
            if not school_name or not course_name:
                print('\033  Error：Input cannot null!\033')
                exit_flag = False
            elif not school_result:
                print('\033  School does not exist\033')
                exit_flag = False
            elif course_name not in school_result['course']:
                print('\033  Course does not exist\033')
                exit_flag = False
            elif course_name in self.user_data['student_data']['course']:
                print('\033  The course has been purchased\033')
                exit_flag = False
            else:
                course_price = school_result['course'][course_name].price
                if self.payment(course_price):
                    account_name = self.user_data['account_data'].username
                    school_result['course'][course_name].students.append(account_name)
                    school_result['student'][account_name] = self.user_data
                    self.user_data['student_data']['school'] = school_name
                    self.user_data['student_data']['course'].append(course_name)
                    self.base_storage.nonquary(school_name, school_result)
                    self.account_storage.nonquary(self.user_data['account_id'], self.user_data)
                    print('\033  The success of the course purchase!\033 ')
                    exit_flag = False
                else:
                    print('\033  Error:Failure of course purchase!\033')


    def payment(self, pay):
        exit_flag = True
        while exit_flag:
            tuition = input('Please pay tuition [%s RMB]：' % pay).strip()
            if not tuition:
                print('\033  Error:Tuition cannot be null!\033')
            else:
                if int(tuition) == pay:
                    return True
                else:
                    return False

    def tell_record(self):
        if not self.user_data['account_data'].study_record:
            study_record = '成绩未公布'
        else:
            study_record = self.user_data['account_data'].study_record.score
        info = '''
================学习记录=================

            Score:  \033 %s\033

=========================================
        ''' % study_record
        print(info)


class TeacherView(View):
    """ 老师视图 """
    user_data = {
        'account_id': None,
        'is_authenticated': False,
        'account_data': None,
        'teacher_data': {'school': None, 'course': [], 'class': []}
    }

    def __init__(self):
        super(TeacherView, self).__init__()
        self.teach_class = None

    def choice_class(self):

        exit_flag = True
        while exit_flag:
            class_name = input('Please input name of class:').strip()
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])
            if class_name not in school_result['class']:
                print('\033 Error: You input class error!\033')
            else:
                if school_result['class'][class_name].teacher != self.user_data['account_data'].username:
                    print('\033  Error: You do not teach the class!\033')
                else:
                    self.teach_class = class_name
                    print('\033  Choice class success!\033')
                    exit_flag = False
                    break

    def tell_students(self):
        #查看班级的学生视图方法
        if not self.teach_class:
            print('\033  Error: Please choice class first!\033')
        else:
            print('================班级学生列表=================')
            print('Class: \033 %s\033' % self.teach_class)
            print('Students: ')
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])

            for student in school_result['student']:
                if self.teach_class in school_result['student'][student]['student_data']['class']:
                    print('\033 %s\033' % student)
            print('=============================================')

    def homework_correcting(self):
        # 修改学生成绩的视图方法
        if not self.teach_class:
            print('\033  Error: Please choice class first!\033')
        else:
            school_result = self.base_storage.quary(self.user_data['teacher_data']['school'])
            print('================作业批改=================')
            exit_flag = True
            while exit_flag:
                student_name = input('Please input name of student:').strip()
                score = input('Please input score of student:').strip()
                if not student_name or not score:
                    print('\033  Error: Student name or Student score cannot be null!\033')
                elif student_name not in school_result['student']:
                    print('\033  Error: %s is not your student!\033' % student_name)
                elif self.teach_class not in school_result['student'][student_name]['student_data']['class']:
                    print('\033  Error: %s is not your student!\033' % student_name)
                else:
                    confirm = input('Confirm input "yes". Back off input "b":').strip()
                    if confirm.upper() == 'YES':
                        username_hash = self.account.create_hash(student_name)
                        student_data = self.account_storage.quary(username_hash)
                        student_data['account_data'].set_score(score)
                        self.account_storage.nonquary(username_hash, student_data)
                        print('\033 [%s] homework to be corrected\033' % student_name)
                    elif confirm.upper() == 'B':
                        exit_flag = False


class AdminView(View):
    """ 管理员视图 """
    account = Accounts()
    account.setter(username=settings.DEFAULT_ADMIN_ACCOUNT,
                   password=settings.DEFAULT_ADMIN_PASSWORD, account_type=1, status=0)
    user_data = {
        'account_id': account.id,
        'is_authenticated': False,
        'account_data': account}

    account_storage = inter_db_handler(settings.ACCOUNT_DATABASE)
    account_storage.nonquary(account.id, user_data)

    def __init__(self):
        super(AdminView, self).__init__()

    def login(self, account_type):
        # 管理员登录视图方法
        account_result = super(AdminView, self).login(account_type)
        if not account_result:
            return False
        else:
            return account_result

    def create_school(self):
        # 管理员创建学校视图方法
        exit_flag = True
        while exit_flag:
            print('================创建学校=================')
            name = input('Please input name of school:').strip()
            city = input('Please input city of school:').strip()
            location = input('Please input address of school:').strip()
            school_result = self.school.setter(name, city, location)
            if not name or not city or not location:
                print('\033  Error: Cannot be null!')
                exit_flag = False
            elif not school_result:
                print('\033  School has already existed!\033')
                exit_flag = False
            else:
                self.base_data['school'] = school_result
                self.base_storage.nonquary(name, self.base_data)
                print('\033  Create school success!\033')
                exit_flag = False

    def create_courses(self):
        # 管理员创建课程视图方法
        print('================创建课程=================')
        exit_flag = True
        while exit_flag:
            course_name = input('Please input course name:')
            price = input('Please input price:')
            period = input('Please input term:')
            school_name = input('Please input associated school:')
            school_result = self.school.getter(school_name)
            # print(school_result)
            if not course_name or not price or not period or not school_name:
                print('\033  Cannot be null!\033')
                exit_flag = False
            elif not price.isdigit() or not period.isdigit():
                print('\033  Price and Period must be integer!\033')
                exit_flag = False
            elif not school_result:
                print('\033  School does not exist\033')
                exit_flag = False
            elif course_name in school_result['course']:
                print('\033  Course has already existed!\033')
                exit_flag = False
            else:
                course_obj = Courses(course_name, int(price), int(period))
                if course_obj:
                    school_result['course'][course_name] = course_obj
                    self.base_storage.nonquary(school_name, school_result)
                    print('\033  Create course success!\033')
                    exit_flag = False
                else:
                    print('\033  Create course failed!\033')
                    exit_flag = False

    def create_classes(self):
        #创建班级视图方法
        print('================创建班级=================')
        exit_flag = True
        while exit_flag:
            class_name = input('Please input class name:').strip()
            school_name = input('Please input associated school:').strip()
            course_name = input('Please input associated course:').strip()
            teacher_name = input('Please input associated teacher:').strip()

            school_result = self.school.getter(school_name)
            if not class_name or not course_name or not school_name:
                print('\033  Cannot be null!\033')
                exit_flag = False
            elif not school_result:
                print('\033  School does not exist\033')
                exit_flag = False
            elif not course_name in school_result['course']:
                print('\033  Course does not exist\033')
                exit_flag = False
            elif not teacher_name in school_result['teacher']:
                print('\033  Teacher does not exist\033')
                exit_flag = False
            else:
                course_obj = school_result['course'][course_name]
                course_obj.classes.append(class_name)  # 在课程对象中添加班级的名称
                classes_obj = Classes(class_name, teacher=teacher_name)  # 创建班级对象
                school_result['class'][class_name] = classes_obj
                self.base_storage.nonquary(school_name, school_result)
                print('\033  Create class success!\033')
                exit_flag = False
                
    def create_teachers(self, account_type, account_status):
        #创建老师视图方法
        print('================创建老师=================')
        exit_flag = True
        while exit_flag:
            username = input('Please input username:').strip()
            password = input('Please input password:').strip()
            re_password = input('Please input password confirmation:').strip()
            school_name = input('Please input associated school:').strip()
            school_result = self.school.getter(school_name)
            account_obj = self.account.setter(username, password, account_type, account_status)
           
            if not username or not password:
                print('\033 Error: Username or Password cannot be null!\033')
                exit_flag = False
            elif not school_result:
                print('\033  Error: School does not exist\033')
                exit_flag = False
            elif username == password:
                print('\033 Error:Username Cannot be equal to Password !\033')
                exit_flag = False
            elif password != re_password:
                print('\033 Error:Password do not match!\033')
                exit_flag = False
            elif not account_obj:
                print('\033 The user has already existed!\033')
                exit_flag = False
            else:
                # 创建新老师账号
                TeacherView.user_data['account_id'] = account_obj.id
                TeacherView.user_data['account_data'] = account_obj
                TeacherView.user_data['teacher_data']['school'] = school_name
                # print(TeacherView.user_data)
                school_result['teacher'][username] = account_obj
                self.base_storage.nonquary(school_name, school_result)
                self.account_storage.nonquary(account_obj.id, TeacherView.user_data)
                print('\033  Registry Success！\033')
                exit_flag = False

    def tell_student(self):
        # 管理员查看学校中的学生视图方法
        exit_flag = True
        while exit_flag:
            school_name = input('Please input school:').strip()
            school_result = self.school.getter(school_name)
            if not school_name:
                print('\033 Error: School cannot be null!\033')
                exit_flag = False
            elif not school_result:
                print('\033  Error: School does not exist!\033')
                exit_flag = False
            else:
                students = school_result['student']
                if not students:
                    print('\033  Students does not exist!\033')
                    exit_flag = False
                else:
                    for student_name in students:
                        student_id = students[student_name]['account_id']
                        account_data = students[student_name]['account_data']
                        student_data = students[student_name]['student_data']
                        account_type = account_data.account_type
                        account_status = account_data.status
                        account_school = student_data['school']
                        account_course = ','.join(student_data['course'])
                        # print(student_data)
                        account_class = ','.join(student_data['class'])
                        if not account_class:
                            account_class = "未分配班级"
                        account_teacher = ','.join(student_data['teacher'])
                        if not account_teacher:
                            account_teacher = "未分配导师"
                        info = '''
==================学生信息==================

         ID：         \033 :%s
         Account：    \033 :%s\033
         Type：       \033 :%s\033
         Status:      \033 :%s\033
         School:      \033 :%s\033
         Course:      \033 :%s\033
         Class:       \033 :%s\033
         Teacher:     \033 :%s\033
         
============================================
                                        ''' % (student_id, student_name, account_type, account_status,
                                               account_school, account_course, account_class, account_teacher)
                        print(info)
                    exit_flag = False
                    # 调试代码

    def assign_class(self):
        # 管理员分配班级视图方法
        print('================分配班级=================')
        exit_flag = True
        while exit_flag:
            school_name = input('Please input name of school:').strip()
            student_name = input('Please input account of student:').strip()
            course_name = input('Please input name of course:').strip()
            class_name = input('Please input name of class:').strip()
            school_result = self.school.getter(school_name)
            if not school_name or not student_name or not class_name or not course_name:
                print('\033  Error: School or Student or Class or Course cannot be null!\033')
                exit_flag = False
            elif not school_result:
                print('\033  Error: School does not exist!!\033')
                exit_flag = False
            else:
                school_student = school_result['student']
                school_course = school_result['course']
                school_class = school_result['class']
                if student_name not in school_student:
                    print('\033  Error: Student does not exist!!\033')
                    exit_flag = False
                else:
                    student_data = school_student[student_name]
                    if course_name not in school_course:
                        print('\033  Error: Course does not exist!!\033')
                        exit_flag = False
                    elif class_name not in school_class:
                        print('\033  Error: Class does not exist!!\033')
                        exit_flag = False
                    elif course_name not in student_data['student_data']['course']:
                        print('\033  Error: Student does not buy Course!!\033')
                        exit_flag = False
                    elif class_name not in school_course[course_name].classes:
                        print('\033  Error: Course!!\033')
                        exit_flag = False
                    else:
                        school_student[student_name]['student_data']['class'].append(class_name)
                        school_student[student_name]['student_data']['teacher'].append(school_class[class_name].teacher)
                        self.account_storage.nonquary(school_student[student_name]['account_id'], school_student[student_name])
                        self.base_storage.nonquary(school_name, school_result)
                        print('\033  Students have bound courses!\033')
                        exit_flag = False

