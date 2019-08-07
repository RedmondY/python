f = open('C:/Users/VULCAN/Desktop/Python/day5/test.txt', mode='r',)

txt_list = []

i = 0
j = 0
for line in f:
    i += 1
    if line not in line:
        line += '\n'
    if line not in txt_list:
        txt_list.append(line)

f = open('C:/Users/VULCAN/Desktop/Python/day5/test.txt', mode='w',)
for line in txt_list:
    j += 1
    if j == i:
        line = line[:-2]
    f.write(line)


f.close()
