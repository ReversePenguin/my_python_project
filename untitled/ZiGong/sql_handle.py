# _*_ coding:utf-8 _*_

import pymssql
import xlsxwriter

def get_marix_excel(out_file,data1,data2,data3,data4):
    #参数传值有待改进
    workbook = xlsxwriter.Workbook(out_file)
    sheet = workbook.add_worksheet("sheet1")
    m = len(data1)
    for i in range(m):
        sheet.write(i, 0, data1[i])
        sheet.write(i, 1, data2[i])
        sheet.write(i, 2, data3[i])
        sheet.write(i, 3, data4[i])

    workbook.close()


'''数据库操作'''

'''
Data Source=NOTHING\MSSQLSERVER2014;Initial Catalog=ZiGong;Integrated Security=True
'''
SQLSever_Connect = dict(host='NOTHING\MSSQLSERVER2014', user='sa', password='123528', database='ZiGong',as_dict = True)
conn = pymssql.connect(**SQLSever_Connect)
# 游标
cur = conn.cursor()

# 执行sql语句
sql1 = 'select person_NO from Out_attribute'

#返回查询的结果
cur.execute(sql1)
out_person_NO_data = cur.fetchall()

out_home_NO_data = []
for i in range(len(out_person_NO_data)):
    sql2 = r"select home_NO from Personal_attribute where person_NO = '" + str(out_person_NO_data[i]['person_NO']) + "' "
    cur.execute(sql2)
    a = cur.fetchall()[0]['home_NO']
    out_home_NO_data.append(a)

out_quming_data = []
out_xiangzhenming_data = []
out_jiedaoming_data = []
for i in range(len(out_person_NO_data)):
    sql3 = r"select quming,xiangzhenming,jiedaoming from Home_attribute where home_NO = '" + str(out_home_NO_data[i]) + "' "
    cur.execute(sql3)
    aaa = cur.fetchall()
    out_quming_data.append(aaa[0]['quming'])
    out_xiangzhenming_data.append(aaa[0]['xiangzhenming'])
    out_jiedaoming_data.append(aaa[0]['jiedaoming'])


# 关闭数据库
cur.close()
conn.close()
'''数据库操作结束'''


print len(out_quming_data),"  ",len(out_xiangzhenming_data),"  ",len(out_jiedaoming_data),"  "

get_marix_excel("区县镇名.xlsx".decode("utf-8"),out_home_NO_data,out_quming_data,out_xiangzhenming_data,out_jiedaoming_data)



