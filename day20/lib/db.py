import abc
import pickle
import os

class AbstractDatabase(object, metaclass=abc.ABCMeta):
    def __init__(self, conn_params, username, password):
        self.conn_params = conn_params
        self.username = username
        self.password = password
        self.db_path = '%s/%s' % (conn_params['path'], conn_params['name'])

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def quary(self, sql):
        pass

    @abc.abstractmethod
    def nonquary(self,sql):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class FileStorage(AbstractDatabase):

    def __init__(self, conn_params, username, password):
        super(FileStorage, self).__init__(conn_params, username, password)

    def connect(self):
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)

    def quary(self, file):
        with open('%s/%s' % (self.db_path, file), "rb") as f:
            data = pickle.load(f)
            return data

    def nonquary(self, file, data):
        with open('%s/%s' % (self.db_path, file), 'wb') as f:
            pickle.dump(data, f)
        return True

    def close(self):
        pass


def inter_db_handler(conn_params):
    if conn_params['engine'] == 'file_storage':
        file_db = FileStorage(conn_params, conn_params['username'], conn_params['password'])
        return file_db

    # 扩展功能，支持mysql存储
    elif conn_params['engine'] == 'mysql_storage':
        mysql_db = MysqlStroage(conn_params, conn_params['username'], conn_params['password'])
        return mysql_db


def inter_db_connect(obj):
    obj.connect()


def inter_file_load_data(obj, file):
    obj.load_data(file)


def inter_file_dump_data(obj, file, data):
    obj.dump_data(file, data)

