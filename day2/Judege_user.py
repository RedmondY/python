userPsw = {'1000':'1000', '2000':'2000', '3000':'3000'}
userCnt = {'1000':0, '2000':0, '3000':0}

JUDGE = 0
while(JUDGE != 3): 
    
    inputUser = input('请输入用户名：')
    if userCnt[inputUser] == 3:
        print("您输错密码次数太多，被禁止登陆!!!")
    
    if userCnt[inputUser] < 3:
        inputPsw = input('请输入密码：')
        if inputPsw != userPsw[inputUser]:
            print("您输入密码错误！！！")
            userCnt[inputUser] += 1
            if userCnt[inputUser] == 3:
                JUDGE += 1
                print("您输错密码次数太多，将被禁止登陆!!!")
        else:
            print("您输入密码正确!!!")
    
print("所有用户都被禁止登陆！！！")