#_*_ coding:utf-8 _*_
import copy
import json
import time
import datetime
import math
import re
import numpy
import random

'''


d = {"s1":[3],"s2":4}
#c = copy.copy(d)
c = d['s1']
c=[2]
print d
print c


data = json.load(open('data_source_3weeks_nonull_dict'))
data_dict = data['result']

idnames = []
a = {}
for i in data_dict:
    idnames.append(i)

for i in idnames:
    if idnames.count(i) > 1:
        a[i] = idnames.count(i)

print a
'''
def get_time_interval(string_time1,string_time2):
    '''
    计算时间差
    :param string_time1: 时间（年-月-日 时：分：秒）
    :param string_time2: 时间（年-月-日 时：分：秒）
    :return: 时间差（float）
    '''
    timeArray1 = time.strptime(string_time1, "%Y-%m-%d %H:%M:%S")  # 转换为时间措
    timeArray2 = time.strptime(string_time2, "%Y-%m-%d %H:%M:%S")
    timeStamp1 = int(time.mktime(timeArray1))
    timeStamp2 = int(time.mktime(timeArray2))
    result = (timeStamp2 - timeStamp1)/60.0

    return result

def get_pingpong_type(origin_string):
    N = len(origin_string)






'''
stime1 = "2016-09-01 00:31:50"
stime2 = "2016-09-01 00:32:15"
t1 = stime1.split(' ')
t11 = t1[1].split(':')
print t11
a = map(lambda x:60*int(x),t11[0:2])
print sum(a)
t22 = [1,2,3]

t11.append(t22)
print 1 not in t11
print t11

t = [5,5,1,1,1,2,3,3,3]
a = set(t)

for i in range(10):
    print i
    if i == 4:

        i += 3
        print i

a = "jlsdgo1235.245" + "-" + "jlsdoi" + "-" + "1343.545643"
print a
file(a,'w')

str1 = 'ACACACBBBAAACADEF'
a = re.search(r"((\w)\w)\1*\2",str1)
print a
print a.group()
print a.groups()

print ord('A')
print chr(65)

print round(2.2)

c=[]
a = [1,2]; b=[[2,3]];
b.append(a)

print pow(2,5)
'''
str1 = 'CACACBBBAAACADEF'
com = re.compile(r"((\w)\w)\1*\2")

print len(str1)
print str1[15]

'''
while True:
    a = re.search(com,str2)

    if a != None:
        found_str = a.group()
        long = len(found_str)

        begin_index += long + str2.find(found_str)
        print begin_index
        str2 = str1[begin_index:]
        result.append(found_str)
        result_long.append(long)
    else:
        break



#a = re.search(com,str2)
print a
print result
print result_long
'''
