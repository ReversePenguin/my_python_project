#_*_ coding:utf-8 _*_

import xlrd
import xlwt
import sys


def to_str(s):
    try:
        n = int(s)
        return str(n)
    except:
        return str(s)

def get_excel(out_file,all_data):
    w = xlwt.Workbook()
    sheet = w.add_sheet("sheet1")
    for i in range(len(all_data)):
        for j in range(len(all_data[0])):
            sheet.write(j, i, all_data[i][j])
    w.save(out_file)



def all_qu_chuxing(from_file,find_id,mudi):
    '''
    各个区出行目的、出行方式的统计函数
    :param from_file:
    :param find_id:
    :param mudi:
    :return:
    '''
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_id
    qu_name = ['魏都区','建安区','东城区','示范区','经开区','长葛市','禹州市','襄城县','鄢陵县']
    all_data = []

    for i in range(len(qu_name)):
        temp = []
        for i in range(len(mudi)):
            temp.append(0)
        all_data.append(temp)

    for i in range(1,nrows):
        for q in range(len(qu_name)):
            #找到对应区
            s = to_str(table.cell(i, j).value)
            if str(table.cell(i, 0).value) == qu_name[q] :
                #判断对应的目的
                for k in range(len(mudi)):
                    if s.find(str(mudi[k])) != -1 :
                        all_data[q][k] += 1
                break

    return all_data

def all_qu_time(from_file,find_id):
    #各个区出行时间的分布函数
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_id
    qu_name = ['魏都区', '建安区', '东城区', '示范区', '经开区', '长葛市', '禹州市', '襄城县', '鄢陵县']
    all_data = []

    for i in range(len(qu_name)):
        temp = []
        for i in range(24):
            temp.append(0)
        all_data.append(temp)

    for i in range(1,nrows):
        for q in range(len(qu_name)):
            # 找到对应区
            if str(table.cell(i, 0).value) == qu_name[q]:
                s = table.cell(i, j).value
                if type(s) == type(0.1):
                    a = xlrd.xldate_as_tuple(s, 0)
                else:
                    break

                #print a
                for k in range(24):
                    #判断值在哪个时段
                    if a[3] == k :
                        all_data[q][k] += 1
                        break


                break





    return all_data





mudi = [1,2,3,4,5,6,7,8,'其']
fangshi = [1,2,3,4,5,6,7,8,9,'其']
#all_data = all_qu_chuxingmudi("test.xlsx".decode('utf-8'),2)
#all_data = all_qu_chuxing("目的特征出行时间.xlsx".decode('utf-8'),2,mudi)
#print all_data
#all_data2 = all_qu_chuxing("目的特征出行时间.xlsx".decode('utf-8'),3,fangshi)
#print all_data2
#all_qu_chuxingmudi("目的特征出行时间.xlsx".decode('utf-8'),2)

#all_data = all_qu_time("20170504-出行属性.xlsx".decode('utf-8'),8)
all_data1 = all_qu_chuxing("20170504-出行属性.xlsx".decode('utf-8'),9,mudi)
#all_data2 = all_qu_chuxing("20170504-出行属性.xlsx".decode('utf-8'),10,fangshi)

#get_excel("各区的出行时间.xls".decode('utf-8'), all_data)
get_excel("各区的出行目的.xls".decode('utf-8'), all_data1)
#get_excel("各区的出行方式.xls".decode('utf-8'), all_data2)






