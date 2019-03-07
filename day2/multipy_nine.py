for row in range(9):
    row += 1
    line = 0
    while(line != row):
        line += 1
        s = str(row) + '*' + str(line) + '=' + str(row*line)
        print(s,end=" ")
    print('')