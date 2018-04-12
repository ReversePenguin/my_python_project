#_*_ coding:utf-8 _*_

import xlsxwriter
import xlrd
import sys

#反推OD量


def get_marix_excel(out_file,all_data):
    workbook = xlsxwriter.Workbook(out_file,{"strings_to_formulas":True})
    sheet = workbook.add_worksheet("sheet1")
    m = len(all_data)
    sheet.write(0,0,"X")
    sheet.write(m+1, 0, "合计")
    sheet.write(0, m+1, "合计")

    for i in range(1,m+1):
        sheet.write(i,0,i)
    for j in range(1,m+1):
        sheet.write(0,j,"C"+str(j))

    for i in range(m):
        #row_sum = 0
        for j in range(m):
            sheet.write(i+1, j+1, all_data[i][j])
            #row_sum += all_data[i][j]
        #sheet.write(i + 1, m+1, row_sum)

    col_last = ""
    row_last = ""
    if m == 554:
        #小区
        col_last = "UI"
        row_last = "555"
    if m == 38:
        #中区
        col_last = "AM"
        row_last = "39"

    for i in range(1,m+1):
        row = "sum(B" + str(i+1) + ":" + col_last + str(i+1)+")"
        sheet.write_formula(i , m + 1, row)
        #col = "sum(B2:B" + row_last + str(i+1)+")"
        #sheet.write_formula(m+1, i, col)

    workbook.close()


def adjust(big_file,small_file,out_file,correspond_table):
    '''

    :param big_file: 上一级的OD矩阵
    :param small_file: 这一级的OD矩阵
    :param correspond_table: 小区大小对应关系的数组
    :return:
    '''
    reload(sys)
    sys.setdefaultencoding('utf-8')

    bfile = xlrd.open_workbook(big_file)
    big_table = bfile.sheet_by_index(0)
    big_nrows = big_table.nrows
    big_ncols = big_table.ncols
    sfile = xlrd.open_workbook(small_file)
    small_table = sfile.sheet_by_index(0)
    small_nrows = small_table.nrows
    small_ncols = small_table.ncols

    big_OD = []  #较大的区的行OD量
    for i in range(1,big_nrows-1):
        s = int(big_table.cell(i,big_ncols-1).value)
        big_OD.append(s)

    n = len(correspond_table)  #较大的区的数量
    small_OD = []  #每个较大的区对应的较小的区的OD量之和
    for i in range(n):
        small_sum = 0
        for ii in correspond_table[i]:
            v = int(small_table.cell(ii,small_ncols-1).value)
            small_sum += v
        small_OD.append(small_sum)

    print big_OD
    print small_OD
    print n," ",len(big_OD)," ",len(small_OD)," "
    scale = []  #两个OD量的比例
    for i in range(n):
        scale.append(float(big_OD[i])/small_OD[i])

    print scale

    #修改后的较小的区的OD矩阵
    marix = []
    for i in range(small_nrows -2):
        temp = []
        for ii in range(small_nrows -2):
            temp.append(0)
        marix.append(temp)

    for k in range(n):
        for i in correspond_table[k]:
            for j in range(1,small_ncols-1):
                v = small_table.cell(i,j).value  #float格式
                marix[i-1][j-1] = int(round(v*scale[k]))
                #marix[i - 1][j - 1] = v * scale[k]

    get_marix_excel(out_file,marix)


def adjust2(from_file,out_file):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    rfile = xlrd.open_workbook(from_file)
    table = rfile.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols

    scale = 99928 / table.cell(nrows-1,ncols-1).value

    marix = []
    for i in range(nrows - 2):
        temp = []
        for ii in range(nrows - 2):
            temp.append(0)
        marix.append(temp)

    for i in range(1,nrows -1):
        for j in range(1,ncols - 1):
            v = table.cell(i,j).value  #float格式
            #marix[i - 1][j - 1] = int(round(v * scale))
            marix[i - 1][j - 1] = v * scale

    get_marix_excel(out_file, marix)



#大区对应中区
big_middle = [[23, 37, 38], [7, 10, 13, 17, 18, 19, 21, 22, 27, 28, 29, 30, 31, 33], [8, 9, 12, 14, 16, 20],
              [25, 32, 34], [26, 11], [24, 35], [5, 6, 15, 36], [1, 4], [2], [3]]
#中区对应小区
middle_small = [[2, 3, 11, 5, 13, 20, 9], [12, 10, 15, 24, 26, 29, 30, 4, 17], [7, 23, 36, 32, 8, 6, 1],
                [31, 18, 22, 14, 28, 37], [165, 312, 321, 295, 302, 519, 326, 301, 439, 25, 34, 19, 16],
                [21, 33, 35, 27, 359, 150, 237, 232, 448, 225, 323, 428], [39, 315, 107, 57, 101, 60, 100, 144, 178, 169, 268, 38, 85, 216],
                [366, 53, 116, 123, 190, 54, 77, 84, 78, 119, 66, 168, 51, 75],
                [72, 227, 269, 158, 213, 48, 47, 127, 62, 380, 248, 91, 175, 170, 152],
                [58, 95, 98, 246, 220, 41, 200, 196, 138, 266, 224, 319, 271, 360, 195, 172, 290],
                [487, 550, 545, 500, 336, 490, 374, 324, 482, 350, 262, 257, 331, 391, 425, 511, 325, 293, 140, 228, 252, 281, 333, 427, 486, 444, 155, 244, 114, 278],
                [89, 46, 64, 113, 90, 162, 93, 159, 171, 173, 349, 247, 103],
                [288, 480, 145, 65, 386, 102, 201, 56, 203, 494, 71, 122, 104, 254, 79],
                [92, 130, 418, 330, 108, 164, 88, 52, 186, 97, 523, 251, 193, 49],
                [236, 43, 340, 229, 40, 167, 207, 277, 245, 112, 163, 298, 341, 222, 410],
                [82, 59, 153, 189, 182, 256, 223, 125, 109, 146, 243, 106, 73],
                [263, 454, 42, 99, 217, 80, 270, 343, 124, 344, 535, 458, 362, 131, 390, 420],
                [215, 183, 111, 291, 311, 296, 339, 50, 209, 347, 398, 304, 280, 387, 318, 358, 406, 507, 504, 469],
                [234, 120, 126, 68, 174, 181, 118, 180, 206, 141, 115, 179],
                [160, 274, 166, 235, 132, 149, 128, 238, 294, 316, 117, 426, 194, 70],
                [233, 401, 45, 208, 142, 338, 286, 240, 395, 242, 83, 505, 157, 69],
                [86, 197, 81, 191, 267, 110, 94, 198, 134, 177, 276],
                [383, 308, 255, 292, 332, 423, 478, 400, 513, 526, 475, 376, 449, 394, 416, 422, 352, 445, 498, 377, 417, 434, 348, 489, 460, 476, 258, 415],
                [230, 129, 96, 317, 226, 297, 461, 264, 306, 205, 143, 259, 303, 313, 370, 459],
                [136, 354, 435, 379, 441, 533, 497, 368, 491, 510, 372, 516, 309, 310, 437, 334, 470, 307, 411, 355, 335, 413],
                [279, 212, 188, 260, 272, 381, 473, 382, 407, 414, 467, 539, 453, 389, 412, 378, 154, 365],
                [133, 466, 465, 184, 151, 483, 202, 477, 474, 488, 443, 399, 452, 250, 342, 464, 506, 493, 528],
                [249, 61, 187, 502, 363, 289, 273, 540, 210, 204, 397, 495, 231], [76, 55, 137, 63, 87, 305],
                [299, 287, 282, 353, 44, 218, 536, 221, 74], [139, 161, 405, 241, 300, 462, 192, 199, 176, 219, 409],
                [479, 429, 403, 357, 328, 436, 471, 451, 515, 534, 531, 527, 554, 522, 385, 485, 463, 530, 456, 345, 520, 388, 549, 524, 481],
                [442, 404, 356, 253, 67, 375, 431, 419, 509, 430, 518, 135, 337], [351, 517, 265, 283, 285, 105, 185, 327, 211, 147],
                [468, 521, 402, 396, 432, 329, 393, 261, 239, 392, 447, 320, 314, 450, 421, 446], [156, 455, 148, 284, 121, 373, 424, 537, 214, 438, 472],
                [457, 322, 371, 501, 364, 346, 275, 433, 408, 508, 546, 503, 499, 361, 367],
                [529, 544, 548, 542, 543, 552, 532, 547, 551, 514, 541, 484, 440, 492, 538, 512, 525, 384, 496, 369, 553]]


#adjust('20170516-大区数据.xlsx'.decode('utf-8'),'20170516-中区数据.xlsx'.decode('utf-8'),'20170516-中区数据-修改后.xlsx'.decode('utf-8'),big_middle)
adjust('20170516-中区数据-修改后.xlsx'.decode('utf-8'),'20170516-小区数据.xlsx'.decode('utf-8'),'20170516-小区数据-修改后.xlsx'.decode('utf-8'),middle_small)
#adjust2('20170516-中区数据-修改后.xlsx'.decode('utf-8'),'20170516-中区数据-总出行量一致.xlsx'.decode('utf-8'))
#adjust2('20170516-小区数据-修改后.xlsx'.decode('utf-8'),'20170516-小区数据-总出行量一致.xlsx'.decode('utf-8'))

