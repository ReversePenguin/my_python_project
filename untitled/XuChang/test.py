#_*_ coding:utf-8 _*_

import xlsxwriter
import xlrd
import datetime

'''

count = [712, 3216, 33496, 1494, 4842, 399, 389, 12, 28, 5, 11]
n = 0
for i in range(1,len(count)):
    n += i * count[i]

#print n

s = "123"
print s.find('4'), " ", type(s.find('4'))
if s.find('1') != -1 :
    print s
else:
    print "meiyou "

print divmod(70,60)[0]

w = xlsxwriter.Workbook("1.xlsx".decode('utf-8'))
sheet = w.add_worksheet("sheet1")
sheet.write(0,0,"10:00:00")
sheet.write(0,0,datetime.time(*(7,30)))
w.close()

print datetime.time(*(7,30))

print divmod(25,24)[1]

rfile = xlrd.open_workbook("test.xlsx")
table = rfile.sheet_by_index(0)
s = table.cell(2,14).value
print s<0


s = "培养党性q"
print s.find("q")



n = 0
big_middle=[[23,37,38],[7,8,9,10,12,13,14,16,17,18,19,20,21,22,27,28,29,30,31,33],[25,32,34],[26,11],[24,35],[5,6,15,36],[1,4],[2],[3]]
for i in range(len(big_middle)):
    n += len(big_middle[i])
    print n



workbook = xlsxwriter.Workbook('1.xlsx')
for i in range(2):
    s = "my_sheet" + str(i+1)
    sheet = workbook.add_worksheet(s)
    sheet.write(0,0,i+1)
workbook.close()
'''
a = [1,2,3,1]
for i in a :
    print i

