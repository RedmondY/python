max = 10
for cur in range(1, max+1):
    for i in range(max - cur):
        print(' ',end='')
    for j in range(2*cur - 1):
        print('*',end='')
    print('')
