#_*_ coding:utf-8 _*_


import os
import xlrd




def count_out_no(from_file):
    '''
    计算每种出行次数有多少人，比如出行1次的有多少人，2次有多少人
    :param from_file:
    :param out_file:
    :param begin_row:
    :param sheet_name:
    :return:
    '''
    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)

    # 获取行数和列数
    nrows = table.nrows


    count = [712, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    i = 0
    j = 0

    while 1:
        val = int(table.cell(i, j).value)
        i += 1
        if i < nrows:
            val2 = int(table.cell(i, j).value)
            if val2 != 1 :
                continue
            else:
                count[val] += 1
        else:
            #最后一行
            print i,"  ",nrows
            count[val] += 1
            break

    return count


count = count_out_no("out_NO.xlsx")
#count = count_out_no("test.xlsx")
print count









