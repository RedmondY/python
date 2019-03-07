from lib import db
from conf import settings
import hashlib
import os
from lib.persion import *


class Accounts(object):
    """ 账号父类 """
    storage = db.inter_db_handler(settings.ACCOUNT_DATABASE)
    human = Persion()

    def __init__(self, username, password, account_type, account_status, user_info_obj = None):
        self.id = self.generate_md5(username)
        self.username = username
        self.__password = self.generate_md5(self.check_password(password))
        self.__account_type = account_type
        self.__account_status = account_status
        self.user_info_obj = user_info_obj

    @property
    def password(self):
        return self.__password

    @property
    def account_type(self):
        return self.__account_type

    @staticmethod
    def check_password(self, value):
        return value

    def getter(self, username, password):
        """ 获取账号

        :return:
        """
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
            # self.storage.nonquary(self.id, self)  # 存储到数据库
            return self
        else:
            return False

    @staticmethod
    def generate_md5(value):
        md5_id = hashlib.md5()
        md5_id.update(value.encode('utf-8'))
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
        # self.storage.nonquary(self.id, account_data)
        return account_data

    def change_password(self, account_data, new_password):
        self.new_password = self.create_hash(new_password)
        account_data.password = self.new_password
        print(account_data.__dict__)
        self.storage.nonquary(self.id, account_data)
        return account_data


class TeacherAccounts(Accounts):
    # storage = db.inter_db_handler(settings.TEACHER_ACCOUNT_DATABASE)

    def __init__(self):
        super(TeacherAccounts, self).__init__()

    def getter(self, username, password):
        result = super(TeacherAccounts, self).getter(username, password)
        if result:
            return result
        else:
            return False


    def setter(self, username, password, account_type, status):
        super(TeacherAccounts, self).setter(username, password, account_type, status)

    def __check_username(self):
        if not os.path.exists('%s/%s' % (self.storage.db_path, self.id)):
            return True
        else:
            return False

class StudentAccounts(Accounts):

    def __init__(self):
        super(StudentAccounts, self).__init__()


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


if __name__ == '__main__':
    import pickle
    ac = Accounts()
    ac.setter('12345','123456',1,2)

    print(ac.__dict__)
    ac.set_info('12345','123456',19)
    print(ac.__dict__)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(base_dir)
    with open('%s/db/accounts/%s'% (base_dir,ac.id)) as f:
        print(pickle.load(f.encoding('utf-8')))
