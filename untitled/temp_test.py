#_*_ coding:utf-8 _*_

import MySQLdb
import pymssql
import webbrowser

s = 'sdglkhg'
print s.__contains__('k')
'''
s1 = raw_input('path:')
p= s1.split('\\')
print p

a,b = [8,9]
print a
print b
'''

def ddd():
    s1 = '小'
    s2 = '名'
    return s1,s2

print ddd()

print "dsdf"+str(1)

url = 'D:\study\Python\PycharmProjects\untitled\VRP\get_distanceAndTime.HTML'
webbrowser.open(url)