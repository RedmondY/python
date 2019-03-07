class StudyRecord(object):

    def __init__(self):
        self.__score = None

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = value
