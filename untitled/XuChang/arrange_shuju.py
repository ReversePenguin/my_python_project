#_*_ coding:utf-8 _*_

#整理出行属性数据

import xlsxwriter
import xlrd
import sys
import datetime
import random


def to_str(s):
    try:
        n = int(s)
        return str(n)
    except:
        return str(s)


def get_time_interval(t1,t2):
    #计算t1到t2花了多少时间
   # result = [0,0]
    result = divmod(t2[3]*60+t2[4] - t1[3]*60-t1[4],60)
    return result

def time_jian(t,interval=30):
    #求t减去interval分钟的时间
    #result = [0, 0,"00"]
    result = divmod(t[3]*60+t[4]  - interval,60)
    return result

def time_jia(t,interval=30):
    # 求t加上interval分钟的时间
    #result = [0, 0]
    result = divmod(t[3] * 60 + t[4] + interval,60)
    return result


def get_wrong_data(from_file,out_filename):
    #筛选出到达时间小于出发时间的数据
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows


def fill_data(from_file,out_filename):
    # 填充返程时的出发时间和到达时间不填写的空白数据（写了到达地地和出发地）
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("my_sheet")

    for i in range(nrows):
        for j in range(ncols):
            #先把原有数据复制一份
            sheet.write(i,j,table.cell(i,j).value)

    for i in range(nrows):
        s8 = table.cell(i,7).value
        pre_s8 = table.cell(i - 1, 7).value
        s12 = table.cell(i,11).value
        pre_s12 = table.cell(i - 1, 11).value
        pre_s9 = table.cell(i - 1, 8).value
        pre_s13 = table.cell(i - 1, 12).value
        if s8 == pre_s12 and s12 == pre_s8 and table.cell(i,8).value == "" and s8 != "" and s12 != "" and pre_s9 != "" and pre_s13 != "":
            print i, "  ", pre_s9, "  ", pre_s13
            pre_s9 = xlrd.xldate_as_tuple(pre_s9, 0)
            pre_s13 = xlrd.xldate_as_tuple(pre_s13, 0)
            begin_time = [0,0]
            begin_time[0] = divmod(pre_s13[3] + 2,24)[1]

            sheet.write(i, 8, datetime.time(*begin_time))
            onway_time = get_time_interval(pre_s9,pre_s13)

            arrival_time = [0,0]
            arrival_time[0] = divmod(begin_time[0]+onway_time[0],24)[1]
            arrival_time[1] = onway_time[1]
            sheet.write(i, 12, datetime.time(*arrival_time))
        #把空白的出行方式补充为上一行的数据
        s11 = table.cell(i, 10).value
        if s11 == "":
            ii = i
            while 1:
                s11_1 = table.cell(ii, 10).value
                if s11_1 == "":
                    ii -= 1
                else:
                    sheet.write(i, 10, to_str(table.cell(ii-1, 10).value))
                    break

    workbook.close()


def one_blank_time(from_file,out_filename):
    # 填充其中一个时间是空白的另一个时间的数据
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("my_sheet")

    for i in range(nrows):
        for j in range(ncols):
            #先把原有数据复制一份
            sheet.write(i,j,table.cell(i,j).value)

    for i in range(nrows):
        s9 = table.cell(i, 8).value
        s13 = table.cell(i, 12).value
        if s9 == "" and s13 != "":
            s13_1 = xlrd.xldate_as_tuple(s13,0)
            s13_2 = time_jian(s13_1)
            print i,"  ",s13_1,"   ",s13_2
            sheet.write(i, 8, datetime.time(*s13_2))
        if s9 != "" and s13 == "":
            s9_1 = xlrd.xldate_as_tuple(s9,0)
            s9_2 = time_jia(s9_1)
            print i, "  ", s9_1, "   ", s9_2
            sheet.write(i, 12,datetime.time(*s9_2))

    workbook.close()

def fill_data1(from_file,out_filename):
    #填充出发地点写了但是没有写到达地点的数据
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s8 = table.cell(i,7).value  #出发地点
        s12 = table.cell(i, 11).value  # 到达地点
        if s8 != "" and s12 == "":
            s3 = table.cell(i, 2).value  # 社区/村
            if s3 == "":
                s2 = table.cell(i, 1).value  # 街道
                sheet.write(i, 11, s2)
            else:
                sheet.write(i, 11, s3)

    workbook.close()

def fill_data2(from_file,out_filename):
    #填充返程的出行序号和出行方式
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s7 = table.cell(i,6).value  #出行序号
        s8 = table.cell(i,7).value  #出发地点
        s10 = table.cell(i, 9).value  # 出发目的
        s12 = table.cell(i, 11).value  # 到达地点
        #补充出行序号2
        if s8 != "" and s12 != "" and s7 == "":
            sheet.write(i,6,2)
        #补充出行目的8
        s7 = table.cell(i, 6).value  # 出行序号
        if s10 == "" and s7 != "" and int(s7) == 2:
            sheet.write(i,9,8)

    workbook.close()


def fill_data3(from_file,out_filename):
    #补充出行序号为1的数据
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s7 = table.cell(i,6).value
        s8 = table.cell(i, 7).value
        s9 = table.cell(i, 8).value
        s12 = table.cell(i, 11).value
        s13 = table.cell(i, 12).value

        if i > 10:
            if s7 != "" and int(s7) == 1 and s8 == "" and s9 == "" and s12 == "" and s13 =="":
                print i
                ii = i
                while 1:
                    pre_s7 = table.cell(ii-1,6).value
                    pre_s8 = table.cell(ii-1,7).value
                    pre_s9 = table.cell(ii - 1, 8).value
                    pre_s12 = table.cell(ii - 1, 11).value
                    pre_s13 = table.cell(ii - 1, 12).value
                    ii -= 1
                    if pre_s7 != ""  and int(pre_s7) == 1 and pre_s8 != "" and pre_s9 != "" and pre_s12 != ""and pre_s13 != "":
                        sheet.write(i,7,pre_s8)
                        sheet.write(i, 8, pre_s9)
                        sheet.write(i, 11, pre_s12)
                        sheet.write(i, 12, pre_s13)
                        break

    workbook.close()

def fill_data4(from_file,out_filename):
    #补充返程的出发地点、时间、方式和到达地点
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s7 = table.cell(i,6).value  #出行序号
        s8 = table.cell(i,7).value  #出发地点
        #s10 = table.cell(i, 9).value  # 出发目的
        #s12 = table.cell(i, 11).value  # 到达地点

        if i > 10:
            if s7 != "" and int(s7) == 2 and s8 == "":
                print i
                pre_s8 = table.cell(i-1, 7).value  # 上一行的出发地点，即从家里出来的出行
                pre_s12 = table.cell(i-1, 11).value  # 上一行的到达地点
                pre_s9 = table.cell(i - 1, 8).value   #上一行的出发时间
                pre_s13 = table.cell(i - 1, 12).value  #上一行的到达时间
                pre_s11 = table.cell(i-1,10).value  #上一行的出行方式

                # 补充返程的出发地点和到达地点
                sheet.write(i,7,pre_s12)
                sheet.write(i,11,pre_s8)

                #填充返程的时间
                pre_s9 = xlrd.xldate_as_tuple(pre_s9, 0)
                pre_s13 = xlrd.xldate_as_tuple(pre_s13, 0)
                begin_time = [0, 0]
                begin_time[0] = divmod(pre_s13[3] + 2, 24)[1]
                sheet.write(i, 8, datetime.time(*begin_time))
                onway_time = get_time_interval(pre_s9, pre_s13)
                arrival_time = [0, 0]
                arrival_time[0] = divmod(begin_time[0] + onway_time[0], 24)[1]
                arrival_time[1] = onway_time[1]
                sheet.write(i, 12, datetime.time(*arrival_time))

                #填充返程的方式
                sheet.write(i,10,pre_s11)

    workbook.close()

def fill_data5(from_file,out_filename):
    #补充剩余的空白行的出发地点、时间等
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s8 = table.cell(i,7).value  #出发地点
        if s8 == "" :
            print i
            ii = i
            #找到最近的一行出行序号为1的数据替代
            while 1 :
                pre_s7 = table.cell(ii - 1,6).value
                pre_s8 = table.cell(ii - 1, 7).value
                if pre_s7 != "" and int(pre_s7) == 1 and pre_s8 != "":
                    sheet.write(i, 6, 1)
                    for k in range(7,13):
                        sheet.write(i, k, table.cell(ii - 1, k).value)
                    break
                ii -= 1

    workbook.close()

def fill_data6(from_file,out_filename):
    #补充出行方式和出行目的
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    mudi = [1, 2, 3, 4, 5, 6, 7, 8, '其']

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s10 = table.cell(i,9).value  #出发目的
        s11 = table.cell(i, 10).value  # 出发方式
        if s10 == "":

            r = random.randint(0, len(mudi) - 1)
            print i, " 目的 ",r
            sheet.write(i,9,mudi[r])

        if s11 == "" :
            print i," 方式"
            ii = i
            #找到最近的一行出行方式的数据替代
            while 1 :
                pre_s11 = table.cell(ii - 1,10).value
                ii -= 1
                if pre_s11 != "" :
                    sheet.write(i, 10, pre_s11)
                    break

    workbook.close()


def fill_data7(from_file, out_filename):
    # 把到达时间小于出发时间的行的时间对调
    reload(sys)  # 2
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    workbook = xlsxwriter.Workbook(out_filename)
    sheet = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            # 先把原有数据复制一份
            sheet.write(i, j, table.cell(i, j).value)

        s15 = table.cell(i,14).value
        if s15 < 0:
            print i
            s9 = table.cell(i, 8).value
            s13 = table.cell(i, 12).value
            sheet.write(i,8,s13)
            sheet.write(i,12,s9)

    workbook.close()




#one_blank_time("出行属性.xlsx".decode('utf-8'),"填充一个时间是空白的出行属性.xlsx".decode('utf-8'))
#fill_data("填充一个时间是空白的出行属性.xlsx".decode('utf-8'),"填充回程和出行方式的出行属性.xlsx".decode('utf-8'))
#fill_data1("填充回程和出行方式的出行属性.xlsx".decode('utf-8'),"填充出发地点有但到达地点无的出行属性.xlsx".decode('utf-8'))
#fill_data2("填充出发地点有但到达地点无的出行属性.xlsx".decode('utf-8'),"填充出行序号2和返程出行目的的出行属性.xlsx".decode('utf-8'))
#fill_data3("填充出行序号2和返程出行目的的出行属性.xlsx".decode('utf-8'),"填充出行序号1的数据的出行属性.xlsx".decode('utf-8'))
#fill_data4("填充出行序号1的数据的出行属性.xlsx".decode('utf-8'),"填充返程的所有数据的出行属性.xlsx".decode('utf-8'))
#fill_data5("填充返程的所有数据的出行属性.xlsx".decode('utf-8'),"填充剩余的空白行数据的出行属性.xlsx".decode('utf-8'))
#fill_data6("填充剩余的空白行数据的出行属性.xlsx".decode('utf-8'),"填充出行目的和方式的出行属性.xlsx".decode('utf-8'))
#fill_data7("20170503-出行属性-时耗未修正.xlsx".decode('utf-8'),"修正时耗数据的出行属性.xlsx".decode('utf-8'))

fill_data6("20170503-出行属性.xlsx".decode('utf-8'),"把多个目的和方式改成一个的出行属性.xlsx".decode('utf-8'))


