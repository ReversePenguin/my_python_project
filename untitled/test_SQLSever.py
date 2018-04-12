# _*_ coding:utf-8 _*_

import pymssql

'''数据库操作'''
# 连接本地的sqlsever数据库,as_dict属性为bool设置是否以字典形式返回数据库表格
#conn = pymssql.connect(host='127.0.0.1', user='sa', password='123528', database='MyDatabase',as_dict = True)
'''
#还可以这么连接（这样最好，因为可以吧配置信息放在其他文件里）
SQLSever_Connect = dict(host='127.0.0.1', user='sa', password='123528', database='MyDatabase',as_dict = True)
conn = pymssql.connect(**SQLSever_Connect)
'''
#这样也可以，不过顺序很重要（上面两个不需要注意顺序）
SQLSever_Connect = ('127.0.0.1', 'sa', '123528', 'MyDatabase')
conn = pymssql.connect(*SQLSever_Connect)
# 游标
cur = conn.cursor()

# 执行sql语句
sql1 = 'select * from friend'
#这里只有%s，没有%d等(这个模块决定)
sql2 = "insert into thing (name) values(%s)"
sql3 = "delete from thing where name = %s"
sql4 = "update thing set name = %s where id = %s"
sql5 = "insert into thing (name,sex) values(%s,%s)"
#这个参数是上面sql语句中的%s，执行一条时只能是元组（）或者字典{}，不能是列表[]
params = ('john',1)
params2 = ('john')
#这种参数可以执行多条，有多少参数执行几次sql语句
li = [
    ('lucy','nv'),
    ('lufei','nan')
]
#cur.executemany(sql5,li)  #执行多条时是executemany()
#cur.execute(sql3,params2)

#提交请求，在insect等改变数据库的操作时必须写这个
conn.commit()
#返回查询的结果
cur.execute(sql1)
#data cur.fetchone()
#data = cur.fetchmany(3)
data = cur.fetchall()


# 关闭数据库
cur.close()
conn.close()
'''数据库操作结束'''

print data[0][0]




