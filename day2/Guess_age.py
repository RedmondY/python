user_age = 20

count = 0
JUDGE_2 = 0

while(JUDGE_2 == 0):
    
    guess_age = input('请输入年龄：')   
    count += 1
    
    if user_age == guess_age:
        print('恭喜您猜对了!!!')
        break
    else:
        print('不好意思，您猜错了。')
        
    if count%3 == 0:
        JUDGE_2 = 1
    
    while(JUDGE_2 == 1):
        choose = input('您已猜错三次，是否继续(请输入Y/N(y/n):').lower()
        if choose == 'n':
            JUDGE_2 = 2
            break
        elif choose != 'y':
            print('请输入正确字母!!!')
        else:
            JUDGE_2 = 0
            break
        
    if JUDGE_2 == 2:
        break    