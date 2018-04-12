#_*_ coding:utf-8 _*_

import time

#时间的三种表现方式
print time.time()  #时间戳形式：1970年1月1日之后的秒
print time.gmtime()  #元组形式
print time.strftime('%Y-%m-%d %H:%M:%S')  #字符串形式

#三个形式可以相互转换
print time.strptime('2016-8-4','%Y-%m-%d')
print time.localtime()
print time.mktime(time.localtime())