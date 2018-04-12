#_*_ coding:utf-8 _*_

import os
import xlrd
import xlwt
import sys


def compound(from_file,out_file,begin_row,sheet_name):
    existed_row = 0
    w = xlwt.Workbook()
    sheet = w.add_sheet(sheet_name)#,cell_overwrite_ok=True)

    for k in range(len(from_file)):
        a = from_file[k]
        #print a

        rfile = xlrd.open_workbook(from_file[k])
        #table = rfile.sheet_by_index(sheet_index)
        # 其他方式
        # table = rfile.sheets()[0]
        table = rfile.sheet_by_name(sheet_name)

        # 获取整行，整列的值
        table.row_values(0)
        table.col_values(0)

        # 获取行数和列数
        nrows = table.nrows
        ncols = table.ncols

        print nrows,"  ",ncols

        # 循环获取列表的数据
        # for i in range(nrows):
        #  print table.row_values(i)



        # 获取所有值
        for i in range(begin_row,nrows):
            for j in range(ncols):
                # table.cell(i,j).value获取某一单元格的值
                val = table.cell(i, j).value

                sheet.write(existed_row + i - begin_row, j, val)
        existed_row = existed_row + nrows - begin_row
        print existed_row
    w.save(out_file)

def getFileName(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            #if os.path.splitext(file)[1] == '.xlsx':
                L.append(os.path.join(root, file))
    return L

print "开始"
files = getFileName("D:\study\Python\PycharmProjects\untitled\excel\shujubiao")

#compound(files,"test1.xls",2,"家庭属性".decode('utf-8'))
compound(files,"test2.xls",2,"个人属性".decode('utf-8'))
#compound(files,"test3.xlsx",1,"出行属性".decode('utf-8'))



