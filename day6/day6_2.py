import pickle
 
def product_info():
    # 初始化商品列表
    product_dict = {'watch': 1222, 'iphoneX': 8888, 'coffee': 15,
                    'car':6666666, 'HUAIWEI': 17999, 'jacket': 200,
                    'MacBook pro': 23333, 'hamburger': 50}
    # 给商品添加索引
    product_list_index = [(index+1, key, product_dict[key]) for index, key in enumerate(product_dict)]
    return product_dict,product_list_index
 
def register():
    while True:
        # 输入注册账号
        user = input('请输入账号: ').strip()
        # 输入为空，重新输入
        if user == '':continue
        if user in user_dict:
            print('账号已存在，请重新输入!')
            continue
        else:
            pwd = input('请输入密码： ')
            user_dict[user] = [pwd, 0, 0]
            print('Registered successfully!')
            # 把更新后的账号字典保存到文件 user.pkl
            with open('user.pkl', 'wb') as f:
                pickle.dump(user_dict, f)
                break
 
def login():
    flag = False
    try_count = 0
    while True:
        user = input('请输入账号: ').strip()
        if user == '':
            continue
        if user in user_dict:
            count = user_dict[user][1]
            while True:
                if count < 3:
                    pwd = input('请输入密码: ')
                    if user_dict[user][0] == pwd:
                        print('登录成功!')
                        # 进入二级菜单选项界面
                        flag = login_module(user)
                        if flag:
                            break
                    else:
                        # 密码错误次数 count 加 1
                        count += 1
                        print('密码错误! 你有 %s 次重试机会!' % (3-count))
                        continue
                else:
                    # 输错3次后，锁定账号
                    print('此 %s 被锁定!' % user)
                    # 把该账号的错误次数更新到用户字典中
                    user_dict[user][1] = 3
                    with open('user.pkl', 'wb') as f:
                        # 重新写入到文件user.pkl
                        pickle.dump(user_dict, f)
                    # 账号被锁定后，返回上级菜单
                    break
        else:
            try_count += 1
            # 若果尝试3次后，则返回上级菜单
            if try_count == 3:
                break
            else:
                # 账号不存在，则重新输入，有3次机会
                print('账户不存在。你有 %s 次重试机会!' %(3-try_count))
                continue
        # 返回上级菜单
        if flag:
            break
 
def shopping(user):
    product, product_index = product_info()
    money = user_dict[user][2]
    print('你有 %s 元'.center(40) % money)
    print('-' * 40)
    shop_list = []
    total_num = 0
    total_cost = 0
    mix_price = min(product.values())
    while True:
        for i in product_index:
            print(i[0],end='--')
            print(i[1].ljust(13),end='')
            print(i[2])
 
        choose = input('请选择商品序号: ').strip()
        if choose.isdigit():
            if int(choose) in range(1, len(product_index)+1):
                choose_product = product_index[int(choose)-1][1]
                if money >= product[choose_product]:
                    shop_list.append(choose_product)
                    total_cost += product[choose_product]
                elif  money >= mix_price:
                    print('你有 %s 元, 请选择商品.' % money)
                else:
                    print('你余额不足!')
                    break
            else:
                print('输错错误序号，请重试!')
                continue
            # 标记退出
            flag = False
            while True:
                print('你余额为 %s.' % (money-total_cost))
                continue_shopping = input('继续购物？y or n: ').strip()
                if continue_shopping == 'y':
                    break
                elif continue_shopping == 'n':
                    flag = True
                    break
                else:
                    continue
            if flag:
                break
        else:
            print('输入错误，请重试!')
            continue
 
    product_set = set(shop_list)
    print('*' * 40)
    # 打印购物单表头信息
    print('你购物清单为：'.center(40))
    print('商品：'.ljust(15),'价格：'.ljust(7),'个数：'.ljust(5),'花费：'.ljust(7))
    print('-' * 40)
    for i in product_set:
        number = shop_list.count(i)
        total_num += number
        cost = product[i] * number
        print('%s %s %s  %s' % (i.ljust(15),str(product[i]).ljust(7),
                            str(number).ljust(5), str(cost).ljust(7)))
    print('-' * 40)
    print('''All number: %s All cost: %s'''
          % (str(total_num).ljust(7), str(total_cost).ljust(7)))
    print('你余额为 %s.' % (money-total_cost))
 
    with open('user.pkl','wb') as f:
        # 更新账号的余额，保存到文件user.pkl
        user_dict[user][2] = money-total_cost
        pickle.dump(user_dict, f)
 
def  recharge(user):
    # 获取参数user
    input_money = input('请输入需要存入金额: ').strip()
    while True:
        if input_money.isdigit():
            user_dict[user][2] = int(input_money)
            with open('user.pkl','wb') as f:
                # 更新账号的余额，保存到文件user.pkl
                pickle.dump(user_dict, f)
            print('存钱成功!')
            break
        else:
            print('输入错误!')
            continue
 
def  money_balance(user):
    # 打印余额
    print('你拥有 %s YUAN.'% user_dict[user][2])
 
def login_module(user):

    # 登录后显示界面的选项信息
    second_menu = [['1', '充值'], ['2','余额'], ['3', '购物'],
                   ['4', '返回'], ['5', '离开']]
    while True:
        print('*' * 40)
        # 打印二级菜单选项
        for i in second_menu:
            for j in i:
                print(j, end=' ')
            print('')
        choose = input('请输入序号: ').strip()
        if choose == '':
            continue
        # 充值函数
        if choose == '1':
            recharge(user)
        # 查询余额函数
        elif choose == '2':
            money_balance(user)
 
        # 选择购物索引，执行购物函数
        elif choose == '3':
            shopping(user)
        # 返回上级菜单
        elif choose == '4':
            break
        # 结束程序
        elif choose == '5':
            exit()
        else:
            print('输入错误，请重试!')
            continue
    return True
if __name__ == '__main__':
    # 预读取账号信息文件 user.pkl,给函数调用
    with open('user.pkl', 'rb') as f:
        # 读取用户信息
        user_dict = pickle.load(f)
 
    # 构造主菜单列表选项
    main_menu = [['1', '注册'], ['2','登录'], ['3', '离开']]
    while True:
        print('**** 欢迎来到超市 ****')
        # 打印主菜单选项
        for i in main_menu:
            for j in i:
                print(j, end=' ')
            print('')
        choose = input('请输入序号: ').strip()
        if choose == '':
            continue
        # 选择注册索引，执行注册函数
        if choose == '1':
            register()
        # 选择登录索引，执行登录函数
        elif choose == '2':
            login()
        # 选择退出，则程序运行结束
        elif choose == '3':
            print('欢迎下次光临!')
            break
        # 输入不匹配，重新输入
        else:
            print('输入错误，请重试！')
            continue