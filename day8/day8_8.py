
route_dic = {}
def make_route(name):
    def deco(func):
        route_dic[name] = func
    return deco
@make_route('select')
def func1():
    print('select')
 
@make_route('insert')
def func2():
    print('insert')
    
@make_route('update')
def func3():
    print('update')
    
@make_route('delete')
def func4():
    print('delete')
 
@make_route('create')
def func5():
    print('create')
 
print(route_dic)
