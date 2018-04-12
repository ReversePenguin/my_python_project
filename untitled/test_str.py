#_*_ coding:utf-8 _*_

m = 'fan jia xuan shi sha bi fan jia xuan fan jia xuan fan jia xuan'
print len(m)
print m.rfind('b'),m.rfind('f'),m.find('j')
ms = m.split('x')
a = ['f','a','n']
sa = ' - '.join(a)
print ms
print type(sa)
mm = m.replace('fan','Fan',1)  #替换一个，不写count属性则替换全部
print  mm
ml = m.split('fan')
mr = "\033[32mFan\033[0m" .join(ml)
print m
print mr
print '----------------------------------------------------'
print m[-7:]
print m[0:3]
print m[0:]
print m[-7:-1]
m2 = 'aaafanjaixuanshisb'
print m2.strip('aaa')  #去除字符串头部和尾部的相应字符，没有也不会报错
