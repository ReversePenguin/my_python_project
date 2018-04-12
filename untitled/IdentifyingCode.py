#_*_ coding:utf-8 _*_

import random

list_code = []
for i in range(1,7):
    if i == random.randint(1,6):
        list_code.append(str(random.randint(0,9)))
    else:
        list_code.append(chr(random.randint(65,90)))
print ''.join(list_code)