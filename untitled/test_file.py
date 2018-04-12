#_*_ coding:utf-8 _*_

import os

my_file = file('file1')
content = my_file.read(30)
'''
while 1:
    want = raw_input('Please enter your want to find: ')
    if want in content:
        cont_list = content.split(want)
        print "the sum of your want is "+ str(len(cont_list))
        print ('\033[32m%s\033[0m' % want).join(cont_list)
        break
    else:
        print "your want not in this file, please try again."
'''

print __file__
print os.path.dirname(os.path.abspath(__file__))
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))