#_*_ coding:utf-8 _*_

import random
import time

'''测试用'''

GA_start_time_each = time.clock()
item=[1,200,30,4,5,6,70]
'''
print item
random.shuffle(item)
print item
print item[0:3]

start_end = True
n = 0
while start_end:
    print n
    n += 1
    if n==2:
        start_end = False

item.insert(0,0)
item.append(0)

result = {"fitness":item,"total_cost":item,"total_req":item,
          "total_time":item,"final_program":item,"car_count":item
          }
items = [[1,2],[3,4],[5],[6],[7]]
n = item.index(min(item))
print n

print sorted(item,reverse=True)
print sorted(item)

#item.append(9,10)
print item
for i in range(0,11,2):
    print i
GA_end_time_each = time.clock()
record_each_time = '第 %d 次遗传用了 %f 时间\n' % (1, GA_end_time_each - GA_start_time_each)
print record_each_time
a=1;b=0;c=2
if a > b or a < c:
    print a



a = [["22","20"],["33","30"],["11","10"]]
b = sorted(a)

print b
b[0] = ['1']
print b
print a
print round(1.245,2)

dic = {}
for i in range(2):
    dic["s"+str(i)] = i;
print dic
for i in dic:
    print i
'''

a = [[2],[1,3]]
print a.index(1,)
