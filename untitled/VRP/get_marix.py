#_*_ coding:utf-8 _*_
import xlsxwriter

#解析爬到的时间矩阵或者距离矩阵
def get_marix(mode):
    result_marix = []
    marix1 = []

    #读取文件的所有数据
    if mode == "distance":
        distance_file = file('distance_file')
    if mode == "time":
        distance_file = file('time_file')
    datas = distance_file.readlines()
    for data in datas:
        temp = data.strip('\n').split(',')
        temp.pop()
        marix1.append(temp)

    #处理数据，形成距离/时间矩阵
    N = len(marix1[0])
    for i in range(N):
        l = []
        for j in range(N):
            if i == j:
                value = 0
            if i < j:
                value = marix1[i][j-i]
            if i > j:
                value = result_marix[j][i]
            l.append(value)
        #print l
        result_marix.append(l)

    return result_marix

def get_excel(file_name,data):
    workbook = xlsxwriter.Workbook(file_name)
    sheet = workbook.add_worksheet("sheet1")
    m = len(data)

    for i in range(m):
        for j in range(m):
            sheet.write(i, j, data[i][j])
    workbook.close()




if __name__ == '__main__':
    result_time = get_marix("time")
    get_excel("time.xlsx",result_time)
    result_dis = get_marix("distance")
    get_excel("distance.xlsx", result_dis)
    #print result



