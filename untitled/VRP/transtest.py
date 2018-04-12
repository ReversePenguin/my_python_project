import json
from urllib.request import urlopen
import requests
import datetime
import time
import numpy as np


#导入数据为txt格式
#输入
#ID,longitude,latitude,time1,time2
#编号，经度，纬度，停留开始时刻，停留结束时刻

#输出为json格式
#输出
#ID,O_longitude,O_latitude,D_longitude,D_latitude,starttime,arrivetime,duration,mode
#编号，起点，终点，出发时刻，到达时刻，时间，出行模式

#读入数据，每次读入一行，第一行数据不计算，用标记变量记录当前ID,从读入第二行开始，ID相同则进行一次计算，ID不同则不进行计算，
#也就是说如果某个ID只有一行，那么这个ID的计算值为空

#面向过程设计
#主函数负责数据读入，循环，调用计算函数，存储结果
#计算函数包括，调用API，模式判别，时间换算


def pos_mode(time, kw): #认为时间差绝对值最小的是最有可能的出行方式
    dur = list(kw.items())
    dur = sorted(dur, key=lambda x: abs(x[1][0]-time))
    return dur[0][0]  #返回最有可能的出行方式，字符串


def timedelta(t1,t2): #t1,t2为时间戳，格式为20170101000000,字符串
    time1 = datetime.datetime(int(t1[0:4]), int(t1[4:6]), int(t1[6:8]), int(t1[8:10]), int(t1[10:12]), int(t1[12:14]))
    time2 = datetime.datetime(int(t2[0:4]), int(t2[4:6]), int(t2[6:8]), int(t2[8:10]), int(t2[10:12]), int(t2[12:14]))
    return (time2-time1).seconds  #返回两时间戳的时间差，以秒为单位


def getdt(mode, origin, destination):  # 调用百度地图API获得两个停留点之间mode方式下返回数据
    url = 'http://api.map.baidu.com/routematrix/v2/'
    output = 'json'
    ak = 'GPe8YW0mmh1AM7PFLSNGV11VeTLKrx2R'
    # http://api.map.baidu.com/routematrix/v2/driving?output=json&origins=40.45,116.34|40.54,116.35&destinations=40.34,116.45|40.35,116.46&ak=您的ak
    uri = url + mode + '?' + '&output=' + output + '&origins=' + origin + '&destinations=' + destination + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)  # 对json数据进行解析
    return temp


# file = open(r'F:\贵阳大数据\project\transtest\output.json','w') #建立json数据文件

correct = 0
wrong = 0
error = 0
flag = 0

# 读入数据，每次读入一行，第一行数据不计算，用标记变量记录当前ID,从读入第二行开始，ID相同则进行一次计算，ID不同则不进行计算，
# 也就是说如果某个ID只有一行，那么这个ID的计算值为空

# 设置文件存储调用API返回的不同方式出行用时
baidu = open(r'E:\Project\GuiyangBigData\GuiYang_jiaotong\Code\transtest\baiduoutt.txt', 'w')
# 设置文件存储判断错误时的情况
wrong_list = open(r'E:\Project\GuiyangBigData\GuiYang_jiaotong\Code\transtest\baiduout_wrongg.txt', 'w')
# 设置计算百度API平均调用时间的变量
api_cpu_time = []
api_real_time = []

with open(r'E:\Project\GuiyangBigData\GuiYang_jiaotong\Code\transtest\textout2.txt', 'r') as f: #用readlines()
    start = datetime.datetime.now()
    input = f.readlines()
    index = 0
    for data in input:
        index += 1
        line = data.split(' ')
        origin = line[4] + ',' + line[5]  # origin的格式为 lat,lng
        destination = line[6] + ',' + line[7].rstrip()  # destination的格式为 lat,lng
        time1, time2 = line[1], line[2]  # 停留开始时刻,停留结束时刻
        t = timedelta(time1, time2)  # 时间差
        mode_type = {'driving': [0, ''],'riding' : [0, ''],'walking' : [0, '']}
        for mode in mode_type.keys():

            stime = time.clock()
            stime2 = datetime.datetime.now()
            temp = getdt(mode, origin, destination)
            api_cpu_time.append(time.clock() - stime)  # 记录当次调用API用时，供参考
            api_real_time.append((datetime.datetime.now() - stime2).seconds)

            if temp['status'] != 0:
                flag = 1
                break
            mode_type[mode][0] = temp['result'][0]['duration']['value']
            mode_type[mode][1] = temp['result'][0]['distance']['value']
        if flag == 0:
            mode = pos_mode(t, mode_type)  # 识别出行方式
        else:
            flag = 0
            error += 1
            continue

        for mode in mode_type:
            mode_type[mode][0] = str(mode_type[mode][0])
            mode_type[mode][1] = str(mode_type[mode][1])

        if mode == line[3]:
            correct += 1
        else:
            wrong += 1
            wrong_line = str(index) + ' ' + data[0: -1] + ' ' + mode + ' ' + ' ' + ' '.join(mode_type['driving']) + ' ' + ' '.join(mode_type['riding']) \
                         + ' ' + ' '.join(mode_type['walking']) + '\n'
            wrong_list.write(wrong_line)
        for mode in mode_type:
            mode_type[mode][0] = str(mode_type[mode][0])
            mode_type[mode][1] = str(mode_type[mode][1])

        print("it's %dth data, it cost %f cpu time and %f real time" % (index, api_cpu_time[-1], api_real_time[-1]))
        baidu_line = str(index) + ' ' + data[0: -1] + ' ' + ' '.join(mode_type['driving']) + ' ' + ' '.join(mode_type['riding']) \
                         + ' ' + ' '.join(mode_type['walking']) + '\n'
        print(baidu_line)
        baidu.write(baidu_line)

end = datetime.datetime.now()
percent = correct/(correct + wrong)

baidu.close()
wrong_list.close()

api_time = np.array(api_cpu_time)
print("The total time used on api is %f, which average time is %f while the variance is %f" \
      % (api_time.sum(), api_time.mean(), api_time.var()))
print("correct:", correct, "\nwrong:", wrong, "\ncorrectness:", percent)
print("\ntime:", (end-start).seconds)
print("\ntime per API use:", (end-start).seconds/(correct + wrong))
print('OK')

