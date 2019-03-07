'''
自定义轿车元类CarMeta，
实现元类为CarMeta的类至少有生产日期(production_date)、
发动机编号(engine_number)及载客量(capacity)三个基本属性，
没有就不行
'''

class CarMeta(type):
    def __call__(self, *args, **kwargs):
        obj=self.__new__(self)
        self.__init__(obj,*args,**kwargs)
        if ('production_date'  and 'engine_number' and 'capacity') not in obj.__dict__:
            raise TypeError('必须有生产日期、发动机编号及载客量')
        return obj

class BMW(metaclass=CarMeta):
    def __init__(self,production_date,engine_number,capacity):
        self.production_date = production_date
        self.engine_number = engine_number
        self.capacity = capacity
    
    def get(self):
        print(self.production_date, self.engine_number, self.capacity)
    
class Audi(metaclass=CarMeta):
    def __init__(self,production_date,engine_number):
        self.pro_date=production_date
        self.en_number=engine_number

a = BMW(111,2222,4)
a.get()
b = Audi(123, 4)
print(b)
