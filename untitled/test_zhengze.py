#_*_ coding:utf-8 _*_
import re

str1 = 'I\'m singing while you\'re dancing.'
result1 = re.findall(r'\b\w+(?=ing\b)',str1)
result2 = re.match(r'\b\w+(?=ing\b)',str1)   #从头开始匹配，一开始没有返回None
result3 = re.search(r'\b\w+(?=ing\b)',str1)  #返回找到的第一个，否则返回None
print result1
if result2:
    print result2.group()
else:
    print result2
if result3:
    print result3.group()
else:
    print result3

a = re.compile(r'\b\w+(?=ing\b)')
print a.findall(str1)