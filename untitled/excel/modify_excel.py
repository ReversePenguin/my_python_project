#_*_ coding:utf-8 _*_

import os
import xlrd
import xlwt


def modify_excel_forNull(file_name,out_file,sheet_name,col_index,new_col_val=0):
    w = xlwt.Workbook()
    sheet = w.add_sheet(sheet_name,cell_overwrite_ok=True)

    rfile = xlrd.open_workbook(file_name)
    table = rfile.sheet_by_name(sheet_name)

    nrows = table.nrows
    ncols = table.ncols


    m = 0
    for i in range(nrows):
        n = 0
        for j in range(ncols):
            val = table.cell(i, j).value
            if val == "" and j in col_index:
                n += 1
                val = 0
            if n == 5:
                n = 0
                sheet.write(i, 8, 1)
                m += 1
                print "改了第 ",i+1,"行\n",

            sheet.write(i, j, val)
    print "共改了", m ,"行"
    w.save(out_file)

modify_excel_forNull("20170428-魏都区-整理后.xlsx".decode('utf-8'),"test1.xls","家庭属性".decode('utf-8'),[9,10,11,12,13]);





