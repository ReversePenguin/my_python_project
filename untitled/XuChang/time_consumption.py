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

def get_excel1(out_file,result):
    #写入excel
    w = xlwt.Workbook()
    sheet = w.add_sheet("sheet1")
    for i in range(len(result)):
        sheet.write(i, 0,i+1)
        sheet.write(i, 1, result[i])
    w.save(out_file)

def timeConsumptionOfWays(from_file,find_index,mudi,mudi_index):
    #每种出行目的或者出行方式的时耗
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index
    j2 = mudi_index
    interval = [10,20,30,40,50,60,70,80,90,100]

    all_data = []
    for i in range(len(mudi)):
        temp = []
        for i in range(10):
            temp.append(0)
        all_data.append(temp)

    for i in range(1,nrows):
        #找到出行方式
        for m in range(len(mudi)):
            mudi_val = to_str(table.cell(i,j2).value)

            if mudi_val.find(str(mudi[m])) != -1:
                c = xlrd.xldate_as_tuple(table.cell(i,j).value, 0)
                cons = 60*c[3] + c[4]

                if cons >= 90 :
                    all_data[m][9] += 1
                else:
                    for k in range(len(interval)):
                        # 判断值在哪个时段
                        if cons < interval[k]:
                            all_data[m][k] += 1
                            break

    return all_data

def timeConsumptionOfWays1(from_file,find_index):
    #总的时耗
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index

    interval = [10,20,30,40,50,60,70,80,90,100]
    result = []
    for i in range(10):
        result.append(0)

    for i in range(1,nrows):
        #找到出行方式
        c = xlrd.xldate_as_tuple(table.cell(i,j).value, 0)
        cons = 60*c[3] + c[4]

        if cons > 90 :
            result[9] += 1
        else:
            for k in range(len(interval)):
                # 判断值在哪个时段
                if cons <= interval[k]:
                    result[k] += 1
                    break

    return result

def time_bus(from_file,find_index,mudi,mudi_index):
    #公交出行时耗
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index
    j2 = mudi_index
    interval = [10,20,30,40,50,60,70,80,90,100]

    all_data = []
    for i in range(len(mudi)):
        temp = []
        for i in range(10):
            temp.append(0)
        all_data.append(temp)

    for i in range(1,nrows):
        #找到出行方式
        for m in range(len(mudi)):
            mudi_val = to_str(table.cell(i,j2).value)

            if mudi_val.find(str(mudi[m])) != -1 and to_str(table.cell(i, 10).value) == "4":
                c = xlrd.xldate_as_tuple(table.cell(i, j).value, 0)
                cons = 60 * c[3] + c[4]

                if cons > 90 :
                    all_data[m][9] += 1
                else:
                    for k in range(len(interval)):
                        # 判断值在哪个时段
                        if cons <= interval[k]:
                            all_data[m][k] += 1
                            break

    return all_data


fangshi = [1,2,3,4,5,6,7,8,9,'其']
all_data = timeConsumptionOfWays("20170504-出行属性 - 改时耗.xlsx".decode('utf-8'),15,fangshi,10)
get_excel("不同出行方式的出行时耗.xls".decode('utf-8'), all_data)

qu_name = ['魏都区', '建安区', '东城区', '示范区', '经开区', '长葛市', '禹州市', '襄城县', '鄢陵县']
all_data1 = timeConsumptionOfWays("20170504-出行属性 - 改时耗.xlsx".decode('utf-8'),15,qu_name,0)
get_excel("各区的出行时耗.xls".decode('utf-8'), all_data1)


result = timeConsumptionOfWays1("20170504-出行属性 - 改时耗.xlsx".decode('utf-8'),15)
get_excel1("总的出行时耗分布.xls".decode('utf-8'),result)


qu_name = ['魏都区', '建安区', '东城区', '示范区', '经开区', '长葛市', '禹州市', '襄城县', '鄢陵县']
all_data2 = time_bus("20170504-出行属性 - 改时耗.xlsx".decode('utf-8'),15,qu_name,0)
get_excel("各区的公交出行时耗.xls".decode('utf-8'), all_data2)
