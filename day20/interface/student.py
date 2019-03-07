from interface.persion import Persion

class Student(Persion):

    def __init__(self):
        super(Student, self).__init__()
        self.__student_data = None
        self.__study_record = None

    @property
    def student_data(self):
        return self.__student_data

    @property
    def study_record(self):
        return self.__study_record

    @student_data.setter
    def student_data(self, value):
        self.__student_data = value

    @study_record.setter
    def study_record(self, value):
        self.__student_data = value
