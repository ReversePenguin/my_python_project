#_*_ coding:utf-8 _*_

grade = input('请输入成绩:\n')

if grade > 90 :
    msg = '优秀'
elif grade > 80 :
    msg =  '良好'
else:
    if grade > 60 :
        msg = '及格'
    else:
        msg = '不及格'

print msg