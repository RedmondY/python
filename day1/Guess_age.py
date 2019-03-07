user_age = 20

while(1):
    guess_age = input('请输入年龄：')   
    guess_age = int(guess_age)

    if user_age == guess_age:
        print('恭喜您猜对了')
        break
    elif guess_age > user_age:
        print('您猜的数字太大')
    else:
        print('您猜的数字太小')