#_*_ coding:utf-8 _*_

import urllib
import json
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')


def getdt(origin, destination,mode="driving"):  # 调用百度地图API获得两个停留点之间mode方式下返回数据
    url = 'http://api.map.baidu.com/routematrix/v2/'
    output = 'json'
    ak = 'vNVPMSDWNZm3Whu0W469R0PmrSydmbcz'
    # http://api.map.baidu.com/routematrix/v2/driving?output=json&origins=40.45,116.34|40.54,116.35&destinations=40.34,116.45|40.35,116.46&ak=您的ak
    #纬度，经度
    uri = url + mode + '?' + '&output=' + output + '&origins=' + origin + '&destinations=' + destination + '&ak=' + ak
    req = urllib.urlopen(uri)
    res = req.read().decode()  # 将其他编码的字符串解码成unicode
    temp = json.loads(res)  # 对json数据进行解析
    return temp


mycars = [[104.17264,30.825707],[103.985272, 30.596266], [103.840545, 30.666324], [104.233915, 30.655102], [103.975997, 30.661402],
          [104.114013, 30.947109], [103.914821, 30.382478], [104.068132, 30.677681], [104.074488, 30.766221],
          [104.063184, 30.621445], [103.526338, 30.580576], [107.21558, 30.742227], [104.101763, 30.684715],
          [104.02731, 30.665375], [104.035122, 30.639816], [104.078171, 30.509079], [104.084634, 30.618309],
          [104.26724, 30.553361], [106.09279, 30.801611], [104.267312, 30.897759], [104.077056, 30.658545],
          [103.46868, 30.407623], [105.379051, 30.864054], [104.111733, 30.650633], [103.864362, 30.692485],
          [104.185501, 30.816061], [104.020953, 30.700217], [103.986832, 30.650895], [104.652978, 30.128409],
          [104.048047, 30.557234], [104.026923, 30.675858], [104.397788, 31.110966], [104.033832, 30.68923],
          [104.06792, 30.60769], [104.049237, 30.531143], [103.921071, 30.601453], [103.980237, 30.556182]]
distance_file = file("distance_file", 'wt')
time_file = file("time_file", 'wt')
n = len(mycars)
sn = 0  #行数减一
for i in range(sn, n):
    stime = time.clock()
    origin = str(mycars[i][1])+","+str(mycars[i][0])
    for j in range(i, n):
        stime1 = time.clock()
        destination = str(mycars[j][1]) + "," + str(mycars[j][0])
        temp = getdt(origin,destination)
        distance = round(temp["result"][0]["distance"]["value"]/1000.0,2)  #公里
        ftime = round(temp["result"][0]["duration"]["value"] / 3600.0, 2)    #分钟
        distance_file.write(str(distance)+',')
        time_file.write(str(ftime)+',')
        time_file.flush()
        distance_file.flush()
        use_time1 = time.clock() - stime
        print "第" + str(i+1) + "次大中的第" + str(j - i + 1) + "次小循环用时：" + str(use_time1)
    distance_file.write("%第"+str(i+1)+"行结束\n")
    time_file.write("%第" + str(i + 1) + "行结束\n")
    distance_file.flush()
    time_file.flush()
    use_time = time.clock() - stime
    print "第" + str(i+1) + "次循环用时：" + str(use_time)
distance_file.close()



'''
print temp["result"][0]["duration"]["value"]/60
print temp["result"][0]["distance"]["value"]/1000
'''
