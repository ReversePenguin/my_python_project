#_*_ coding:utf-8 _*_


import xlsxwriter
import xlrd
import sys
import xlwt




def to_str(s):
    try:
        n = int(s)
        return str(n)
    except:
        return str(s)


def get_marix_excel(out_file,all_data):
    workbook = xlsxwriter.Workbook(out_file)
    sheet = workbook.add_worksheet("sheet1")
    m = len(all_data)
    sheet.write(0,0,"X")
    for i in range(1,m+1):
        sheet.write(i,0,i)
    for j in range(1,m+1):
        sheet.write(0,j,"C"+str(j))

    for i in range(m):
        for j in range(m):
            sheet.write(i+1, j+1, all_data[i][j])
    workbook.close()


def get_OD_marix(from_file,row_index,col_index):
    '''
    得到OD矩阵
    :param from_file:
    :param row_index:到达小区编号的下标
    :param col_index:出发小区编号的下标
    :param out_filename:
    :return:
    '''
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    marix = []
    for i in range(554):
        temp = []
        for j in range(554):
            temp.append(0)
        marix.append(temp)

    for i in range(1,nrows):
        start_NO = int(table.cell(i,row_index).value)
        arrival_NO = int(table.cell(i,col_index).value)

        for k in range(len(marix)):
            #找到这一行的出发小区的编号
            if start_NO == k + 1:
                for k2 in range(len(marix[0])):
                    #找到这一行的目的小区的编号
                    if arrival_NO == k2 + 1:
                        marix[k][k2] += 1
                        break
                break

    return marix


def get_small_marix(from_file):
    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    marix = []
    for i in range(nrows-1):
        temp = []
        for j in range(nrows-1):
            temp.append(0)
        marix.append(temp)

    for i in range(1,nrows):
        for j in range(1,ncols):
            #s = int(table.cell(i,j).value)
            s = table.cell(i, j).value
            marix[i-1][j-1] = s

    return marix



def get_middle_OD(from_file,small_marix,middle_index=0,small_index=1):
    '''
    得到中区的od量
    :param from_file:
    :param middle_index:
    :param small_index:
    :return:
    '''
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows

    j1 = middle_index
    j2 = small_index

    marix = []
    midlle_small = []  #中区对应小区

    for i in range(38):
        temp = []
        for j in range(38):
            temp.append(0)
        marix.append(temp)
        midlle_small.append([])

    # 找到每个中区包含的小区
    for i in range(1,nrows):
        middle_NO = int(table.cell(i,j1).value)
        small_NO = int(table.cell(i,j2).value)
        for k in range(38):
            if middle_NO == k + 1:
                midlle_small[k].append(small_NO)

    print midlle_small

    m = len(small_marix)
    for i in range(m):
        #找到出发小区对应的中区k
        for k in range(38):
            if i+1 in midlle_small[k]:
                # 找到后再继续找到到达小区对应的中区k，并修改OD矩阵
                for j in range(m):
                    for k1 in range(38):
                        if j+1 in midlle_small[k1]:
                            #找到后对应的修改OD矩阵
                            marix[k][k1] += small_marix[i][j]
                            break

                break



    return marix

def get_big_OD(middle_marix):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    marix = []

    qu_name = ['魏都区', '建安区1', '建安区2', '东城区', '示范区', '经开区', '长葛市', '禹州市', '襄城县', '鄢陵县']
    big_middle = [[23, 37, 38], [7, 10, 13, 17, 18, 19, 21, 22, 27, 28, 29, 30, 31, 33], [8, 9, 12, 14, 16, 20],
                  [25, 32, 34], [26, 11], [24, 35], [5, 6, 15, 36], [1, 4], [2], [3]]
    n = len(big_middle)
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(0)
        marix.append(temp)

    m = len(middle_marix)

    for i in range(m):
        # 找到出发中区对应的大区k
        for k in range(n):
            if i + 1 in big_middle[k]:
                # 找到后再继续找到到达中区对应的大区k1，并修改OD矩阵
                for j in range(m):
                    for k1 in range(n):
                        if j + 1 in big_middle[k1]:
                            # 找到后对应的修改OD矩阵
                            marix[k][k1] += middle_marix[i][j]
                            break

                break

    return marix



def get_diffient_OD(from_file,out_file,mudi,mudi_index):
    #不同出行目的或者出行方式的小区OD
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows

    row_index = 1  #from_file中出发地编号的下标
    col_index = 5  #from_file中目的地编号的下标

    j2 = mudi_index
    workbook = xlsxwriter.Workbook(out_file)

    print "开始计算OD"
    for mudi_i in range(len(mudi)):
        #每一种出行目的或者出行方式建一个新的sheet
        md = str(mudi[mudi_i])
        sheet = workbook.add_worksheet(md)  #新建一个sheet

        marix = []
        for i in range(554):
            temp = []
            for j in range(554):
                temp.append(0)
            marix.append(temp)
        n = 0
        nn = 0
        for i in range(1, nrows):
            #找到特定出行目的或者方式的行
            if to_str(table.cell(i,j2).value) == md :
                nn += 1
                start_NO = to_str(table.cell(i, row_index).value)
                arrival_NO = to_str(table.cell(i, col_index).value)
                for k in range(len(marix)):
                    # 找到这一行的出发小区的编号
                    if start_NO == str(k + 1):
                        for k2 in range(len(marix[0])):
                            # 找到这一行的目的小区的编号
                            if arrival_NO == str(k2 + 1):
                                n += 1
                                marix[k][k2] += 1
                                break
                        break

        all_data = marix
        m = len(all_data)
        sheet.write(0, 0, "X")
        for i in range(1, m + 1):
            sheet.write(i, 0, i)
        for j in range(1, m + 1):
            sheet.write(0, j, "C" + str(j))

        for i in range(m):
            for j in range(m):
                sheet.write(i + 1, j + 1, all_data[i][j])
        print md,"的OD完成",n,"  ",nn

    workbook.close()


def fill_xiaoqu_NO(original_file,middle_file,final_file):
    #填充没有小区编号的目的地和出发地，市外的编号不编号
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(original_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows

    mfile = xlrd.open_workbook(middle_file)
    table2 = mfile.sheet_by_index(0)
    nrows2 = table2.nrows
    ncols2 = table2.ncols

    workbook = xlsxwriter.Workbook(final_file)
    sheet = workbook.add_worksheet()

    #先把excel复制一遍
    for i in range(nrows2):
        for j in range(ncols2):
            sheet.write(i,j,table2.cell(i,j).value)
    '''
    方法一：速度很慢，至少要5个小时才运行完成
    for i in range(1,nrows):
        original_start = str(table.cell(i, 0).value)  # 原始的出发地点
        original_start_NO = int(table.cell(i, 1).value)  # 原始的出发地点编号
        original_arrival = str(table.cell(i, 2).value)  # 原始的到达地点
        original_arrival_NO = str(table.cell(i, 3).value)  # 原始的到达地点编号
        print i

        for i2 in range(1,nrows2):
            final_start = str(table2.cell(i2, 0).value)  # 最终的表中的出发地点
            final_arrival = str(table2.cell(i2,4).value)   # 最终的表中的到达地点
            if original_start == final_start:
                sheet.write(i2,1,original_start_NO)
            if original_arrival == final_arrival :
                sheet.write(i2,5,original_arrival_NO)
    '''
    original_start = []
    original_start_NO = []
    original_arrival = []
    original_arrival_NO = []
    for i in range(1, nrows):
        original_start.append(str(table.cell(i, 0).value))
        original_start_NO.append(int(table.cell(i, 1).value))
        original_arrival.append(str(table.cell(i, 2).value))
        original_arrival_NO.append(int(table.cell(i, 3).value))

    print "开始填充编号"

    for i in range(1,nrows2):
        final_start = str(table2.cell(i, 0).value)  # 最终的表中的出发地点
        final_arrival = str(table2.cell(i, 4).value)  # 最终的表中的到达地点

        if final_start in original_start:
            sheet.write(i, 1, original_start_NO[original_start.index(final_start)])
        if final_arrival in original_arrival:
            sheet.write(i,5,original_arrival_NO[original_arrival.index(final_arrival)])
        print i


    workbook.close()





'''
small_marix = get_OD_marix("出发和目的小区编号.xlsx".decode("utf-8"),1,3)

#print marix
get_marix_excel("OD矩阵.xlsx".decode("utf-8"),marix)

small_marix = get_small_marix("OD矩阵.xlsx".decode("utf-8"))

middle_marix = get_middle_OD("中区对应小区.xlsx".decode("utf-8"),small_marix)

#print middle_marix
get_marix_excel("中区OD矩阵.xlsx".decode("utf-8"),middle_marix)


middle_marix = get_small_marix("中区OD矩阵.xlsx".decode("utf-8"))
big_marix = get_big_OD(middle_marix)
get_marix_excel("大区OD矩阵.xlsx".decode("utf-8"),big_marix)

'''
#fill_xiaoqu_NO("出发和目的小区编号.xlsx".decode("utf-8"),"地点方式目的以及小区编号.xlsx".decode("utf-8"),"出行属性-增加小区编号.xlsx".decode("utf-8"))

#fangshi = [1,2,3,4,5,6,7,8,9,'其它']
#get_diffient_OD("出行属性-增加小区编号.xlsx".decode("utf-8"),"不同出行方式的OD矩阵.xlsx".decode("utf-8"),fangshi,3)
'''
small_marix = get_small_marix("20170907-许昌小区扩样OD.xlsx".decode("utf-8"))
middle_marix = get_middle_OD("中区对应小区.xlsx".decode("utf-8"),small_marix)
get_marix_excel("20170907-许昌中区扩样OD.xlsx".decode("utf-8"),middle_marix)
'''
middle_marix = get_small_marix("20170907-许昌中区区平衡OD.xlsx".decode("utf-8"))
big_marix = get_big_OD(middle_marix)
get_marix_excel("20170907-许昌大区平衡OD.xlsx".decode("utf-8"),big_marix)

