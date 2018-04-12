#_*_ coding:utf-8 _*_

import xlsxwriter
import xlrd


def change_null(file_name,final_name = None):
    '''

    :param file_name: 原始文件名称，excel，英文
    :param final_name: 输出文件名称，excel，英文
    :return:
    '''
    rfile = xlrd.open_workbook(file_name)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    #初始化结果矩阵
    result_marix = []
    for i in range(nrows):
        temp = []
        for i in range(ncols):
            temp.append(0)
        result_marix.append(temp)
    for i in range(1,nrows):
        for j in range(1,ncols):
            this_value = str(table.cell(i, j).value)
            if this_value != "":
                result_marix[i][j] = float(this_value)

    #记录每行的均值，非空/非零值，行和列是一样的
    average_row = []
    for i in range(1,nrows):
        s = sum(result_marix[i])
        n = nrows-1 - result_marix[i].count(0)
        if n == 0:
            average_row.append(0)
        else:
            average_row.append(s/n)

    print result_marix
    print average_row

    #填空值（一半），整行都没有则填0
    for i in range(1,nrows):
        for j in range(i+1,ncols):
            if result_marix[i][j] == 0:
                result_marix[i][j] = average_row[i-1]
    #填空值（一半），上一步没有填充的整行都没有的数据，以列均值填充
    for i in range(1, nrows):
        for j in range(i + 1, ncols):
            if result_marix[i][j] == 0:
                result_marix[i][j] = average_row[j - 1]
    #填充对称的另一半数据
    for i in range(1,nrows):
        for j in range(1,i):
            if result_marix[i][j] == 0:
                result_marix[i][j] = result_marix[j][i]

    #写入excel
    workbook = xlsxwriter.Workbook(final_name)
    sheet1 = workbook.add_worksheet("sheet1")

    for i in range(nrows):
        for j in range(ncols):
            if i == 0:
                result_marix[i][j] = j
            if j == 0:
                result_marix[i][j] = i
            sheet1.write(i, j, result_marix[i][j])

    workbook.close()

if __name__ == "__main__":
    change_null("zukang.xlsx","final.xlsx")




