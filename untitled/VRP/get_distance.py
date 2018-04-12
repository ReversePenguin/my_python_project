#_*_ coding:utf-8 _*_


import xlrd

def get_point(from_file):
    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows

    points = []


    for i in range(nrows):
        temp =[]
        s1 = table.cell(i, 0).value
        s2 = table.cell(i, 1).value
        temp.append(s1)
        temp.append(s2)
        points.append(temp)

    return points

points = get_point("111.xlsx".decode("utf-8"))
print points
print len(points)
