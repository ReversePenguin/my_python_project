#_*_ coding:utf-8 _*_

import json
from get_instance import get_instance_data
from ga import GA
from deal_result import get_point_no
import xlsxwriter


def run_ga(n):
    ga = GA(n)
    ga.GA_main()
    result_programs = ga.memory_best_fit_program
    result_fits = ga.memory_best_fit
    json.dump(result_programs, open("result_programs", 'w'))
    json.dump(result_fits, open("result_fits", 'w'))

def run_n(n):
    temp = []
    get_instance_data(n)
    run_ga(n)
    return_data = get_point_no()
    temp.append([n, return_data["M"], return_data["total_dis"], return_data["rate__home_points"]])
    return temp

if __name__ == '__main__':
    data = []
    nn = 0
    for i in range(100):
        temp = run_n(15)
        data.extend(temp)
        nn += 1
        print nn
    for i in range(100):
        temp = run_n(30)
        data.extend(temp)
        nn += 1
        print nn
    for i in range(100):
        temp = run_n(60)
        data.extend(temp)
        nn += 1
        print nn
    for i in range(100):
        temp = run_n(120)
        data.extend(temp)
        nn += 1
        print nn

    print data

    rows = len(data)
    cols = len(data[0])
    workbook = xlsxwriter.Workbook('lingmindufenxi.xlsx')
    sheet = workbook.add_worksheet("sheet1")
    sheet.write(0, 0, "客户数".decode('utf-8'))
    sheet.write(0, 1, "收货点数".decode('utf-8'))
    sheet.write(0, 2, "配送距离".decode('utf-8'))
    sheet.write(0, 3, "收货点为家的占比".decode('utf-8'))
    for i in range(1,rows+1):
        for j in range(cols):
            sheet.write(i,j,data[i-1][j])

    workbook.close()
