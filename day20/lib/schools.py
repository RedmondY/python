from lib import db
from conf import settings
import os


class Schools(object):
    """ 学校类 """
    storage = db.inter_db_handler(settings.BASE_DATABASE)

    def __init__(self):
        self.name = None
        self.city = None
        self.location = None
        self.course_list = None
        self.class_list = []
        self.teacher_list = []
        self.student_list = []

    def setter(self, name, city, location):
        if self.__check_name(name):
            self.name = name
            self.city = city
            self.location = location
            return self
        else:
            return False

    def getter(self, name):
        if self.__check_name(name):
            return False
        else:
            return self.storage.quary(name)

    def __check_name(self, name):
        if not os.path.exists('%s/%s' % (self.storage.db_path, name)):
            return True
        else:
            return False
