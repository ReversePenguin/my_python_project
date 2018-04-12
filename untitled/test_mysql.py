#_*_ coding:utf-8 _*_

import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123528',db='my3')
cur = conn.cursor()

for i in range(51,451):
    record = cur.execute("insert into app1_host(hostname,IP) values ('www.fangou%s.com','1.1.1.%s')" % (i,i))
    conn.commit()

#record = cur.execute("insert into app1_host(hostname,IP) values ('www.fangou1.com','1.1.1.1')")
#conn.commit()
cur.close()
conn.close()

'''
i = 1
hostname = 'www.fangou%d.com' % i
ip = '1.1.1.%d' % i
print hostname,ip,type(hostname),type(ip)
'''

