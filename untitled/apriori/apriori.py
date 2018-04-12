#_*_ coding:utf-8 _*_

import xlsxwriter
import xlrd
import json

def get_data(origin_file = "basedata.xlsx",minsup = 0.2):
    rfile = xlrd.open_workbook(origin_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    #提取每一个订单的商品编号
    order = {}
    commodity_col = []   #记录商品列，
    for i in range(1,nrows):
        no = str(table.cell(i, 0).value)
        commodity = str(table.cell(i, 3).value)
        commodity_col.append(commodity)
        if no not in order.keys():
            order[no] = [commodity]
        else:
            order[no].append(commodity)


    commodities = set(commodity_col)  #获取商品数量，无重复值
    print len(commodities)

    min_n = minsup * len(order.keys())
    print min_n

    result = {}
    n = 1
    L_one = []
    record_count = []
    for i in commodities:
        print commodity_col.count(i)
        record_count.append(commodity_col.count(i))
        if commodity_col.count(i) > min_n:
            L_one.append(i)
    result['L' + str(n)] = L_one


    return result

print get_data()


