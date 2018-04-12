#_*_ coding:utf-8 _*_

import time
from person import Person
from story import life


aside_begin = '''
================================游戏开始================================
请根据提示进行选择，根据您的选择会有不一样的结局。。。
'''
print aside_begin
time.sleep(1)
print '请根据提示创建您的角色'
imf = ['姓名','性别','年龄','学历','国籍']
information = []
for i in range(len(imf)):
    information.append(raw_input('请输入人物的%s:' % imf[i]))
person1 = Person(information)
life(person1)






