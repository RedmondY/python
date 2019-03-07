import configparser
import hashlib
import os
from conf import settings
from lib import common

class UserHandle():
    def __init__(self,username):
        self.username = username
        self.config = configparser.ConfigParser() #先生成一个对象
        self.config.read(settings.ACCOUNTS_FILE)
    @property
    def password(self):
        return hashlib.md5('123'.encode('utf-8')).hexdigest()
    @property
    def quota(self):
        huiyuan = input('是否开通会员（请输入y/n）？').strip()
        if huiyuan == 'Y' or huiyuan == 'y':
            quota = input('请输入用户的磁盘配额大小>>>:').strip()
            if quota.isdigit():
                return quota
            else:
                exit('      磁盘配额须是整数      ')
        else:
            quota = '10'
            return quota

    def add_user(self):
        if not self.config.has_section(self.username):
            print('creating username is : ', self.username)
            self.config.add_section(self.username)
            self.config.set(self.username, 'password', self.password)
            self.config.set(self.username, 'homedir', 'home/'+self.username)
            self.config.set(self.username, 'quota', self.quota)
            with open(settings.ACCOUNTS_FILE, 'w') as f:
                self.config.write(f)
            os.mkdir(os.path.join(settings.BASE_DIR, 'home', self.username))#创建用户的home文件夹
            print('      创建用户成功      ')
        else:
            print('      用户已存在      ')

    def judge_user(self):
        if self.config.has_section(self.username):
            return self.config.items(self.username)
        else:
            return