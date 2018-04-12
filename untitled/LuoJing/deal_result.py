#_*_ coding:utf-8 _*_

import json
import copy
import xlsxwriter
import math



def get_point_no():
    '''

    :return:
    '''
    ga_result = json.load(open(r"D:\study\Python\PycharmProjects\untitled\LuoJing\result_programs"))
    instance_data = json.load(open("D:\study\Python\PycharmProjects\untitled\LuoJing\instance_data"))
    best_result = ga_result[-1]
    #print best_result
    best_line = best_result['each_server_place']    #最优方案的配送点坐标
    user = best_result['program']    #最优方案的客户顺序
    lines = instance_data['lines']    #每个用户对应的所有的收货点坐标
    result = '0,'
    user_points = []
    for i in range(len(best_line)):
        user_no = user[i]
        user_point = lines[user_no-1].index(best_line[i])+1
        user_points.append(user_point)
        result += str(user_no) + "-" + str(user_point) + ","
    result += "0"

    record_time = best_result["record_time"]
    end_time = map(get_time,record_time)

    M = len(instance_data["record_m"]) + sum(instance_data["record_m"])
    total_dis = best_result['total_dis']
    rate__home_points = user_points.count(1)/float(len(user_points))

    return_data = {"result":result,"end_time":end_time,"M":M,"total_dis":total_dis,"rate__home_points":rate__home_points}

    return return_data

def get_time_window():
    '''
    解析客户的时间窗，转换成时间格式
    :return:
    '''
    instance_data = json.load(open("D:\study\Python\PycharmProjects\untitled\LuoJing\instance_data"))
    time_w = instance_data['all_user_time']
    result_w = copy.copy(time_w)
    for i in range(len(time_w)):
        user_times = time_w[i]
        for j in range(len(user_times)):
            begin_time = get_time(user_times[j][0])   #转换成时间格式
            end_time = get_time(user_times[j][1])
            result_w[i][j][0] = begin_time
            result_w[i][j][1] = end_time
        result_w[i].append(str(i+1))

    return result_w

def get_dismarix():
    instance_data = json.load(open("D:\study\Python\PycharmProjects\untitled\LuoJing\instance_data"))
    home_points = instance_data['home_x_y']
    home_points.insert(0,[0,0])   #添加配送中心坐标
    workbook = xlsxwriter.Workbook('home_distance_marix.xlsx')
    sheet = workbook.add_worksheet("sheet1")
    m = len(home_points)
    sheet.write(0, 0, "X")
    for i in range(1, m+1):
        sheet.write(i, 0, "C" + str(i-1))
    for j in range(1, m + 1):
        sheet.write(0, j, "C" + str(j-1))

    for i in range(m):
        for j in range(m):
            sheet.write(i + 1, j + 1, round(get_distance(home_points[i],home_points[j]),2))
    workbook.close()

def get_fitness():
    '''
    获取适应度函数到excel中
    :return:
    '''
    ga_fit = json.load(open(r"D:\study\Python\PycharmProjects\untitled\LuoJing\result_fits"))
    N = len(ga_fit)
    workbook = xlsxwriter.Workbook('best_fitness.xlsx')
    sheet = workbook.add_worksheet("sheet1")
    for i in range(N):
        sheet.write(i,1,i+1)
        sheet.write(i, 2, ga_fit[i])
    workbook.close()



def get_time(t):
    '''

    :param t: 浮点数格式
    :return:
    '''
    hour = int(t)
    minute = int(round((t - hour) * 60))
    if minute < 10:
        minute = "0" + str(minute)

    return str(hour) + ":" + str(minute)


def get_distance(point1, point2):
    return math.sqrt(pow((point1[0] - point2[0]), 2) + pow((point1[1] - point2[1]), 2))

if __name__ == '__main__':
    return_data = get_point_no()
    print return_data["result"]
    print return_data["end_time"]
    print return_data["M"]
    print return_data["total_dis"]
    print get_time_window()
    #get_dismarix()
    get_fitness()


