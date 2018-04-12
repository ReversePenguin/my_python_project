#_*_ coding:utf-8 _*_

import xlrd
import xlwt
import sys

#不同出行方式、出行目的的出行次数

def to_str(s):
    #先把读取出来的数据转换成string
    try:
        n = int(s)
        return str(n)
    except:
        return str(s)


def out_count(from_file,find_index,mudi):
    '''
    不同出行方式、出行目的、不同职业的出行次数
    :param from_file:
    :param find_index:
    :param mudi:
    :param mudi_index:
    :return:
    '''
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    nrows = table.nrows
    j = find_index

    result = []
    for i in range(len(mudi)):
        result.append(0)

    for i in range(nrows):
        s = to_str(table.cell(i,j).value)

        for k in range(len(mudi)):
            if s.find(str(mudi[k])) != -1:
                result[k] += 1

    return result

def get_excel(out_file,result):
    #写入excel
    w = xlwt.Workbook()
    sheet = w.add_sheet("sheet1")
    for i in range(len(result)):
        sheet.write(i, 0,i+1)
        sheet.write(i, 1, result[i])
    w.save(out_file)

fangshi = [1,2,3,4,5,6,7,8,9,'其']
mudi = [1,2,3,4,5,6,7,8,'其']

'''
result = out_count("20170504-出行属性.xlsx".decode('utf-8'),10,fangshi)
print result
get_excel("不同出行方式的出行次数.xls".decode('utf-8'),result)
'''
result = out_count("20170504-出行属性.xlsx".decode('utf-8'),9,mudi)
print result
get_excel("不同出行目的的出行次数.xls".decode('utf-8'),result)

