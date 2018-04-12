#_*_ coding:utf-8 _*_

import xlrd
import xlwt
import sys

#总的出发时间分布，不同出行方式、出行目的的出发时间分布

def to_str(s):
    #先把读取出来的数据转换成string
    try:
        n = int(s)
        return str(n)
    except:
        return str(s)


def total_time(from_file,find_index):
    #总的时间分布
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index

    result = []
    for i in range(24):
        result.append(0)

    for i in range(1,nrows):
        s = xlrd.xldate_as_tuple(table.cell(i,j).value, 0)
        for k in range(len(result)):
            if s[3] == k :
                result[k] += 1
                break
    return result

def time_mudi(from_file,find_index,mudi,mudi_index):
    '''
    不同出行方式、出行目的的时间分布
    :param from_file:
    :param find_index: 出行时间在第几列（01）
    :param mudi: 出行目的或者出行方式
    :param mudi_index:
    :return:
    '''

    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index
    j1 = mudi_index

    all_data = []
    for i in range(len(mudi)):
        temp = []
        for i in range(24):
            temp.append(0)
        all_data.append(temp)

    for i in range(1,nrows):
        s_mudi = to_str(table.cell(i, j1).value)

        for k in range(len(mudi)):
            #找到对应的目的或者方式
            if s_mudi.find(str(mudi[k])) != -1:
                s = xlrd.xldate_as_tuple(table.cell(i, j).value, 0)

                for kk in range(24):
                    if kk == s[3]:
                        all_data[k][kk] += 1
                        break

    return all_data

def get_excel1(out_file,result):
    #写入excel
    w = xlwt.Workbook()
    sheet = w.add_sheet("sheet1")
    for i in range(len(result)):
        sheet.write(i, 0,i+1)
        sheet.write(i, 1, result[i])
    w.save(out_file)

def get_excel2(out_file,all_data):
    w = xlwt.Workbook()
    sheet = w.add_sheet("sheet1")
    for i in range(len(all_data)):
        for j in range(len(all_data[0])):
            sheet.write(j, i, all_data[i][j])
    w.save(out_file)



fangshi = [1,2,3,4,5,6,7,8,9,'其']
mudi = [1,2,3,4,5,6,7,8,'其']

#result = total_time("20170504-出行属性.xlsx".decode('utf-8'),8)
all_data = time_mudi("20170504-出行属性.xlsx".decode('utf-8'),8,mudi,9)
#all_data1 = time_mudi("20170504-出行属性.xlsx".decode('utf-8'),8,fangshi,10)
#get_excel1("总的出行时间分布.xls".decode('utf-8'),result)
get_excel2("出行目的的出行时间分布.xls".decode('utf-8'),all_data)
#get_excel2("出行方式的出行时间分布.xls".decode('utf-8'),all_data1)


