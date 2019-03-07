from lib import db
from conf import settings
import hashlib
import os
from interface.persion import *
from interface.student import *
from interface.teacher import *
from lib.study_record import *


class Accounts(object):
    """ 账号父类 """
    storage = db.inter_db_handler(settings.ACCOUNT_DATABASE)
    human = Persion()

    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.new_password = None
        self.account_type = None
        self.status = None
        self.user_info = None

    def getter(self, username, password):
 
        self.id = self.create_hash(username)
        self.username = username
        self.password = self.create_hash(password)
        if self.__check_username():
            return False

        else:
            result = self.storage.quary(self.id)
            if self.password == result['account_data'].password:
                return result
            else:
                return False

    def setter(self, username, password, account_type, status):

        self.id = self.create_hash(username)
        self.username = username
        self.password = self.create_hash(password)
        self.account_type = account_type
        self.status = status
        if self.__check_username():
            return self
        else:
            return False

    @staticmethod
    def create_hash(arg):
        md5_id = hashlib.md5()
        md5_id.update(arg.encode('utf-8'))
        return md5_id.hexdigest()

    def __check_username(self):
        if not os.path.exists('%s/%s' % (self.storage.db_path,self.id)):
            return True
        else:
            return False

    def set_info(self, account_data, name, sex, age):
        self.human.name = name
        self.human.sex = sex
        self.human.age = age
        account_data.user_info = self.human
        return account_data

    def change_password(self, account_data, new_password):
        self.new_password = self.create_hash(new_password)
        account_data['account_data'].password = self.new_password
        return account_data


class TeacherAccounts(Accounts):

    def __init__(self):
        super(TeacherAccounts, self).__init__()

    def getter(self, username, password):

        result = super(TeacherAccounts, self).getter(username, password)
        if result:
            return result
        else:
            return False

    def setter(self, username, password, account_type, status):
        # print(username, password)
        super(TeacherAccounts, self).setter(username, password, account_type, status)

    def __check_username(self):
        if not os.path.exists('%s/%s' % (self.storage.db_path, self.id)):
            return True
        else:
            return False


class StudentAccounts(Accounts):

    def __init__(self):
        super(StudentAccounts, self).__init__()
        self.study_record = None

    def set_score(self, value):
        study_record = StudyRecord()
        study_record.score = value
        self.study_record = study_record


class AdminAccounts(Accounts):

    def __init__(self):
        super(AdminAccounts, self).__init__()

    def getter(self, username, password):
        result = super(AdminAccounts, self).getter(username, password)
        if result:
            return result
        else:
            return False


    def setter(self, username=settings.DEFAULT_ADMIN_ACCOUNT, password=settings.DEFAULT_ADMIN_PASSWORD, account_type=1, status=0):
        super(AdminAccounts, self).setter(username, password, account_type, status)

    def __check_username(self):
        if not os.path.exists('%s/%s' % (self.storage.db_path, self.id)):
            return True
        else:
            return False
