name = input('name:')

if name == 'Albert':
    print('超级管理员')
elif name == 'tom':
    print('普通管理员')
elif name == 'jack' or name == 'rain':
    print('业务主管')
else:
    print('普通用户')