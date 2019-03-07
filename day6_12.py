import pickle
 
def unlock_user():
    '''
    输入解锁的账号，即可解锁
    :return: None
    '''
    while True:
        # 输入解锁的账号
        user = input('Please input unlock the user: ').strip()
        # 判断该账号是否存在
        if user in user_dict:
            # 把锁状态标志3 修改为 0
            user_dict[user][1] = 0
            with open('user.pkl','wb') as f:
                # 更新解锁后的账号信息，保存到user.pkl文件中
                pickle.dump(user_dict,f)
                print('The %s unlock successfully!' % user)
                break
        else:
             print('Account does not exist, try again!')
             continue
    return None
 
def change_pwd():
    '''
    输入要修改密码的账号，然后更新密码
    :return: None
    '''
    while True:
        # 输入解锁的账号
        user = input('Please input the user of change password: ').strip()
        # 判断该账号是否存在
        if user in user_dict:
            # 输入新的密码
            new_pwd = input('Please input the %s new password: ' % user).strip()
            user_dict[user][0] = new_pwd
            with open('user.pkl','wb') as f:
                # 更新密码后的账号信息，保存到user.pkl文件中
                pickle.dump(user_dict,f)
                print('The %s change password successfully!' % user)
                break
        else:
             print('Account does not exist, try again!')
             continue
    return None
 
 
 
if __name__ == '__main__':
    # 设置界面功能选项列表
    choose = [['1','unlock user'], ['2','change password'], ['3', 'exit']]
    # 读取账号文件 user.pkl
    with open('user.pkl','rb') as f:
        user_dict = pickle.load(f)
 
    while True:
        # 打印界面功能选项
        print('=' * 50)
        for i in choose:
            for j in i:
                print(j, end= ' ')
            print('')
 
        input_choose = input('Please choose the index: ').strip()
        # 选择解锁功能
        if input_choose == '1':
            unlock_user()
        # 选择修改密码
        elif input_choose == '2':
            change_pwd()
        # 选择退出界面
        elif input_choose == '3':
            break
        else:
            print('You input error, try again!')
            print('-' * 30)
            continue