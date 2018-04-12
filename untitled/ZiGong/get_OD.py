#_*_ coding:utf-8 _*_

import xlsxwriter
import xlrd
import sys

def get_way_od(origin_file,out_file,ways):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(origin_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows

    workbook = xlsxwriter.Workbook(out_file)
    for way in ways:
        sheet = workbook.add_worksheet("方式"+str(way))  # 新建一个sheet
        marix = []
        for i in range(nrows):
            read_way = int(table.cell(i, 2).value)
            if read_way == way:
                temp = []
                read_O = int(table.cell(i, 0).value)
                read_D = int(table.cell(i, 1).value)
                temp.append(read_O)
                temp.append(read_D)
                marix.append(temp)
        all_data = []
        m = 266
        for i in range(m):
            temp = []
            for j in range(m):
                temp.append(0)
            all_data.append(temp)

        for i in range(len(marix)):
            v = marix[i][0]
            v2 = marix[i][1]
            all_data[v-1][v2-1] += 1

        #放入excel中
        sheet.write(0, 0, "X")
        for i in range(1, m + 1):
            sheet.write(i, 0, i)
        for j in range(1, m + 1):
            sheet.write(0, j, "C" + str(j))

        for i in range(m):
            for j in range(m):
                sheet.write(i + 1, j + 1,all_data[i][j])
        print way, "的OD完成"

    workbook.close()


ways = [1,2,3,4,5,6,7,8,9,10]
get_way_od("分方式.xlsx".decode("utf-8"),"不同出行方式的OD矩阵.xlsx".decode("utf-8"),ways)



