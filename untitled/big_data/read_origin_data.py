#_*_ coding:utf-8 _*_

import copy
import json
import math
import time


class CleanData(object):
    LonIndex = 1 # 经度的下标
    LatIndex = 2  # 维度的下标
    TimeIndex = 3  # 时间的下标
    UserIDIndex = 0 #用户名的下标
    DayIndex = 4  #天数标识的下标
    VTHRESHOLD = 16.0  # 速度阈值，暂时设置为16.0m/s
    DAY = 30  #总天数
    MAXDISTANCE = 1000.0   #乒乓切换的距离阈值

    def get_perons_outing(self,list1):
        '''
        处理原始用户出行数据，获取不同用户的出行数据
        :param list1: 去空值后的结果数组
        :return: 字典:'origin_length' 原始数据出行量（int），'final_length' 整合后的用户数（int），
        'result' 结果字典（key=用户名，value=出行数据（list）），'persons_id' 用户名列表，
        'persons_count' 用户出行数列表
        '''

        #排序
        user_index = self.UserIDIndex #用户名的下标
        record_time_index = self.TimeIndex  #记录的时间节点的下标
        list2 = sorted(list1)
        #print len(list2)
        persons_id = []
        persons_outings = []
        flag = True
        begin = 0

        while flag:
            one_outing = []
            o_id = list2[begin][user_index]
            one_outing.append(list2[begin])
            if begin == len(list2)-1:
                persons_id.append(o_id)
                persons_outings.append(one_outing)
                flag = False
            else:
                for i in range(begin+1,len(list2)):
                    if list2[i][user_index]  == o_id:
                        one_outing.append(list2[i])
                        if i == len(list2) -1 :
                            persons_id.append(o_id)
                            persons_outings.append(one_outing)
                            flag = False
                            break
                        continue
                    else:
                        persons_id.append(o_id)
                        persons_outings.append(one_outing)
                        begin = i
                        break
        result = {}
        persons_count = []
        #print len(persons_id),len(persons_outings)
        for i in range(len(persons_id)):
            result[persons_id[i]] = sorted(persons_outings[i],key=lambda x:x[record_time_index])   #按照时间排序
            persons_count.append(len(persons_outings[i]))

        data = {'origin_length':len(list2),'final_length':len(result),'result':result,'persons_id':persons_id,'persons_count':persons_count}
        return data

    def clean_null(self,filename):
        '''
        清理空值
        :param filename: 原始文件名
        :return: 字典：'null_count' 空值的行数（int）、'result_data' 清理后的所有出行数据（list）
        '''
        origin_file = file(filename)
        origin_file_list = origin_file.readlines()
        list1 = []
        for i in origin_file_list:
            list1.append(i.split('\t'))
        result_data = []

        for i in range(len(list1)):
            temp = 0
            for j in range(len(list1[i])):
                if list1[i][j] == "\N":
                    temp += 1
                if j == len(list1[i]) - 1:
                    if temp == 0:
                        result_data.append(list1[i])

        null_count = len(list1)-len(result_data)

        return_data = {'null_count':null_count,'result_data':result_data}
        return return_data

    def clean_excursion_points(self,origin_outing_dict):
        '''
        清洗偏移点
        :param origin_outing_dict: 每个用户的所有出行数据，dict，出行数据中要有天数标识
        :return:字典：'result_data' 结果数据（字典：key=用户名，value=出行数据（list）），
        'exc_information' 偏移点信息（字典：key=用户名，value=每天的偏移点数量（str））
        '''

        # 经度维度的下标
        lon_index = self.LonIndex
        lat_index = self.LatIndex
        time_index = self.TimeIndex    #时间的下标
        day_index = self.DayIndex    #天数的下标
        DAY = self.DAY   #总天数
        cleaned_data = {}   #清洗后的数据字典，key=用户名，value=每日出行数据字典集（list，[{},{}]）

        for username in origin_outing_dict:
            t1 = time.clock()
            one_cleaned_outings = []
            one_all_outings = origin_outing_dict[username]   #该用户所有的出行数据
            for day in range(1,DAY + 1):
                oneday_outings = []   #用户一天的数据
                for i in one_all_outings:
                    if int(i[day_index]) == day:
                        oneday_outings.append(i)
                #获取当日的偏移点，并记录正常的点
                origin_list = copy.copy(oneday_outings)
                excursion_index = []
                N = len(origin_list)

                for i in range(N - 1):
                    if i not in excursion_index:
                        dist = get_distance(origin_list[i][lon_index],origin_list[i][lat_index],origin_list[i+1][lon_index],origin_list[i+1][lat_index])  #与下一点的距离
                        time_int = get_time_interval(origin_list[i][time_index],origin_list[i+1][time_index])  #与下一点的时间差
                        if time_int == 0:
                            v = 0
                        else:
                            v = dist/float(time_int)
                        if v > self.VTHRESHOLD :
                            excursion_index.append(i+1)   #记录偏移点的下标
                    else:
                        #如果i点是偏移点，则以最近的（往前搜索）正常点为基础，来进行下一个点的判断，
                        ii = i; j = i + 1;
                        while True:
                            ii -= 1
                            if ii not in excursion_index:
                                break
                        dist = get_distance(origin_list[ii][lon_index], origin_list[ii][lat_index],
                                            origin_list[j][lon_index], origin_list[j][lat_index])  # 与下一点的距离
                        time_int = get_time_interval(origin_list[ii][time_index],
                                                     origin_list[j][time_index])  # 与下一点的时间差
                        if time_int == 0:
                            v = 0
                        else:
                            v = dist / float(time_int)
                        if v > self.VTHRESHOLD:
                            excursion_index.append(j)  # 记录偏移点的下标


                result_data = []
                for i in range(N):
                    if excursion_index.count(i) == 0 :
                        result_data.append(origin_list[i])

                one_oneday_result = {'data':result_data,'day':day,'excursion_points_count':len(excursion_index)}
                one_cleaned_outings.append(one_oneday_result)
            cleaned_data[username] = one_cleaned_outings
            print '用时：',time.clock() - t1

        #print cleaned_data
        #print len(cleaned_data)
        #整理处理的数据，并输出
        collated_data = {}
        exc_information = {}
        for username in cleaned_data:
            one_list = cleaned_data[username]
            one_outings_data = []
            exc_points_record = ''
            for i in one_list:
                for temp in i['data']:
                    one_outings_data.append(temp)
                if i['excursion_points_count'] > 0:
                    exc_points_record += str(i['day']) + ":" + str(i['excursion_points_count']) + '\n'  #记录哪一天存在偏移点以及个数
            collated_data[username] = one_outings_data
            exc_information[username] = exc_points_record

        result = {'result_data':collated_data,'exc_information':exc_information}
        return result

    def add_day(self,origin_outing_dict):
        '''
        添加天数标识，不同数据需改变代码
        :param origin_list: 出行数据字典
        :return: 添加标识后的数据(字典：key=用户名，value=出行数据（list）)
        '''
        day_index = self.DayIndex
        result_data = {}
        for username in origin_outing_dict:
            one_outings = origin_outing_dict[username]
            backup = copy.copy(one_outings)
            for i in range(len(one_outings)):
                backup[i][day_index] = int(((one_outings[i][day_index]).split('-'))[2]) - 4
            result_data[username] = backup

        return result_data

    def clean_pingpang_points(self,origin_outing_dict):
        '''
        清洗乒乓切换的点
        :param origin_outing_dict:每个用户的所有出行数据，dict，出行数据中要有天数标识
        :return:
        '''
        # 经度维度的下标
        lon_index = self.LonIndex
        lat_index = self.LatIndex
        time_index = self.TimeIndex  # 时间的下标
        day_index = self.DayIndex  # 天数的下标
        DAY = self.DAY  # 总天数
        minV = 1  #最小时间值，步行，，设为1m/s
        cleaned_data = {}  # 清洗后的数据字典，key=用户名，value=每日出行数据字典集（list，[{},{}]）
        record_all_pingpang_index = {}

        for username in origin_outing_dict:
            #username = '000302d702e11f0733516074c47caf08'
            t1 = time.clock()
            one_cleaned_outings = []
            one_all_outings = origin_outing_dict[username]   #该用户所有的出行数据
            record_oneday_pingpang_index = {}
            for day in range(1,DAY + 1):
                oneday_outings = []   #用户一天的数据
                for i in one_all_outings:
                    if int(i[day_index]) == day:
                        oneday_outings.append(i)
                #记录乒乓切换点的下标
                all_pingpang_index = []
                N = len(oneday_outings)
                for i in range(N):
                    all_lon_lat = []
                    o_lon_lat = oneday_outings[i][lon_index] + ',' + oneday_outings[i][lat_index]
                    all_lon_lat.append(o_lon_lat)
                    one_pingpang_index = []  #记录属于该点的切换点,包括自己
                    one_pingpang_index.append(i)
                    #搜索乒乓切换的点
                    for j in range(i+1,N):
                        if j not in all_pingpang_index:
                            dist = get_distance(oneday_outings[i][lon_index], oneday_outings[i][lat_index],oneday_outings[j][lon_index], oneday_outings[j][lat_index])  # 两点的距离
                            time_int = get_time_interval(oneday_outings[i][time_index], oneday_outings[j][time_index])  # 两点的时间间隔
                            if dist == 0.0:
                                i = j
                                one_pingpang_index.append(j)
                                all_lon_lat.append(o_lon_lat)
                                continue
                            if dist < self.MAXDISTANCE and time_int > dist/minV:
                                #距离小于最大间隔，时间间隔大于最大的时间，则识别为乒乓切换点
                                one_pingpang_index.append(j)
                                all_lon_lat.append(oneday_outings[j][lon_index] + ',' + oneday_outings[j][lat_index])
                                continue
                            else:
                                #乒乓切换的点应该是连续的，所以搜索到不符合条件的点就直接退出循环
                                break
                    #乒乓切换点处理：1.找到真实点（出现最多次的点->先出现的点）；2.用真实点的经纬度替换切换点
                    all_lon_lat2 = set(all_lon_lat)
                    if len(all_lon_lat2) > 1:
                        all_pingpang_index.extend(one_pingpang_index)
                        real_point_lon_lat = ''  #真实点的经纬度，lon,lat
                        one_pingpang_count = {}
                        counts = []
                        #第一步
                        for i in all_lon_lat2:
                            counts.append(all_lon_lat.count(i))
                            one_pingpang_count[i] = all_lon_lat.count(i)
                        real_points = []
                        for item in all_lon_lat2:
                            if one_pingpang_count[item] == max(counts):
                                real_points.append(all_lon_lat.index(item))
                        real_point_lon_lat = all_lon_lat[min(real_points)]
                        #第二步
                        real_lon = (real_point_lon_lat.split(','))[0]
                        real_lat = (real_point_lon_lat.split(','))[1]
                        for index in one_pingpang_index:
                            oneday_outings[index][lon_index] = real_lon
                            oneday_outings[index][lat_index] = real_lat
                one_cleaned_outings.extend(oneday_outings)
                record_oneday_pingpang_index['day'+str(day)] = all_pingpang_index
            cleaned_data[username] = one_cleaned_outings
            record_all_pingpang_index[username] = record_oneday_pingpang_index
            print time.clock()-t1

        result = {'result_data':cleaned_data,'pingpang_information':record_all_pingpang_index}

        return result


    def clean_pingpang_points2(self, origin_outing_dict):
        '''
        清洗乒乓切换的点，只基于寻找规则，ABA...
        :param origin_outing_dict:每个用户的所有出行数据，dict，出行数据中要有天数标识
        :return:（dict）：result_data 清洗后的数据（dict），pingpang_information 乒乓切换点的信息（dict）
        '''
        # 经度维度的下标
        lon_index = self.LonIndex
        lat_index = self.LatIndex
        time_index = self.TimeIndex  # 时间的下标
        day_index = self.DayIndex  # 天数的下标
        DAY = self.DAY  # 总天数
        minV = 1  # 最小时间值，步行，，设为1m/s
        cleaned_data = {}  # 清洗后的数据字典，key=用户名，value=每日出行数据字典集（list，[{},{}]）
        record_all_pingpang_index = {}

        for username in origin_outing_dict:
            # username = '000302d702e11f0733516074c47caf08'
            t1 = time.clock()
            one_cleaned_outings = []
            one_all_outings = origin_outing_dict[username]  # 该用户所有的出行数据
            record_oneday_pingpang_index = {}
            for day in range(1, DAY + 1):
                oneday_outings = []  # 用户一天的数据
                for i in one_all_outings:
                    if int(i[day_index]) == day:
                        oneday_outings.append(i)
                #记录所有点的经纬度
                N = len(oneday_outings)
                all_lon_lat = []
                for i in range(N):
                    o_lon_lat = oneday_outings[i][lon_index] + ',' + oneday_outings[i][lat_index]
                    all_lon_lat.append(o_lon_lat)
                oneday_rule = self.get_pingpong_rule(all_lon_lat)
                deal_rule = self.deal_pingpong_rule(oneday_rule,all_lon_lat)
                #print oneday_rule;print deal_rule["result_rule"];print deal_rule["record_index"]
                # 记录乒乓切换点的下标
                all_pingpang_index = deal_rule["record_index"]
                #替代旧的经纬度
                for i in all_pingpang_index:
                    temp = deal_rule["result_lon_lat"][i].split(',')
                    oneday_outings[i][lon_index] = temp[0]
                    oneday_outings[i][lat_index] = temp[1]
                #记录数据
                one_cleaned_outings.extend(oneday_outings)
                record_oneday_pingpang_index['day' + str(day)] = all_pingpang_index
                print username + ":"+"day"+str(day)
            cleaned_data[username] = one_cleaned_outings
            record_all_pingpang_index[username] = record_oneday_pingpang_index
            print time.clock() - t1

        result = {'result_data': cleaned_data, 'pingpang_information': record_all_pingpang_index}

        return result


    def get_staying_points(self,origin_outing_dict):
        '''
        获取停留点
        :param origin_outing_dict: 每个用户的所有出行数据，dict，出行数据中要有天数标识
        :return:
        '''
        # 经度维度的下标
        lon_index = self.LonIndex
        lat_index = self.LatIndex
        time_index = self.TimeIndex  # 时间的下标
        day_index = self.DayIndex  # 天数的下标
        DAY = self.DAY  # 总天数
        staying_data = {}
        record_count = {}

        for username in origin_outing_dict:
            one_all_outings = origin_outing_dict[username]  # 该用户所有的出行数据
            one_stay_info = []
            one_stay_count = {}

            for day in range(1, DAY + 1):
                oneday_outings = []  # 用户一天的数据
                for i in one_all_outings:
                    if int(i[day_index]) == day:
                        oneday_outings.append(i)
                #记录所有点的经纬度
                N = len(oneday_outings)
                all_lon_lat = []
                for i in range(N):
                    o_lon_lat = oneday_outings[i][lon_index] + ',' + oneday_outings[i][lat_index]
                    all_lon_lat.append(o_lon_lat)
                one_day_staying_points = []
                one_day_staying_points_begin_times = []
                one_day_staying_points_end_times = []

                #识别停留点
                for i in range(N):
                    this_lon_lat = all_lon_lat[i]
                    this_time = oneday_outings[i][time_index]
                    #一天中第一个点，开始时间设置为00:00:00
                    if i == 0:
                        one_day_staying_points.append(this_lon_lat)
                        date_begin_time = ((oneday_outings[i][time_index]).split(' '))[0] + " 00:00:00"
                        one_day_staying_points_begin_times.append(date_begin_time)
                        one_day_staying_points_end_times.append(this_time)
                        continue

                    date_end_time = ((oneday_outings[i][time_index]).split(' '))[0] + " 23:59:59"
                    if this_lon_lat != one_day_staying_points[-1]:
                        #与上一个点不是同一个点，则创建新的停留点，否则更新结束时间
                        one_day_staying_points.append(this_lon_lat)
                        one_day_staying_points_begin_times.append(this_time)
                        if i == N - 1:
                            # 一天中最后个点，开始时间设置为23:59:59
                            one_day_staying_points_end_times.append(date_end_time)
                        else:
                            one_day_staying_points_end_times.append(this_time)
                    else:
                        if i == N - 1:
                            one_day_staying_points_end_times[-1] = date_end_time
                        else:
                            one_day_staying_points_end_times[-1] = this_time
                #print one_day_staying_points_begin_times;print one_day_staying_points_end_times
                new_oneday_staying_info = []
                for i in range(len(one_day_staying_points)):
                    temp = [username,one_day_staying_points[i].split(',')[0],one_day_staying_points[i].split(',')[1],one_day_staying_points_begin_times[i],one_day_staying_points_end_times[i],day]
                    new_oneday_staying_info.append(temp)
                one_stay_info.extend(new_oneday_staying_info)
                one_stay_count['day' + str(day)] = len(one_day_staying_points)

            staying_data[username] = one_stay_info
            record_count[username] = one_stay_count

        return_data = {"result_data":staying_data,"record_count":record_count}

        return return_data


    def get_pingpong_rule(self,origin_data):
        '''
        得到这组数据的切换形式
        :param origin_data: 原始数据列表,值为经纬度(str)
        :return:
        '''
        norepetition = []
        N = len(origin_data)
        for i in origin_data:
            if i not in norepetition:
                norepetition.append(i)

        rule = []
        for i in origin_data:
            rule.append(norepetition.index(i))

        for i in range(N):
            rule[i] = chr(rule[i] + 65)

        return rule

    def deal_pingpong_rule(self,rule,all_lon_lat):
        '''
        加上距离阈值
        :param rule:
        :return:
        '''
        N = len(rule)
        result_rule = copy.copy(rule)
        result_lon_lat = copy.copy(all_lon_lat)
        record_index = []
        begin = 0

        while True:
            if begin > N - 3:
                break
            this_value = rule[begin]
            next_value = rule[begin + 1]
            next2_value = rule[begin + 2]
            if this_value != next_value and this_value == next2_value:
                this_value_list = all_lon_lat[begin].split(',')
                next_value_list = all_lon_lat[begin+1].split(',')
                if get_distance(this_value_list[0],this_value_list[1],next_value_list[0],next_value_list[1]) > self.MAXDISTANCE:
                    begin += 1
                    continue
                result_rule[begin + 1] = this_value
                record_index.append(begin+1)
                begin += 2
                continue
            begin += 1

        for i in range(N):
            result_lon_lat[i] = all_lon_lat[result_rule.index(result_rule[i])]

        return_data = {"result_rule":result_rule,"result_lon_lat":result_lon_lat,"record_index":record_index}

        return return_data


def get_distance(longitude_a,latitude_a,longitude_b,latitude_b):
        '''
        根据经纬度计算a、b两点之间的距离
        :param longitude_a: a点的经度，东经，str或者float
        :param latitude_a: a点的维度，北纬，str或者float
        :param longitude_b: b点的经度，东经，str或者float
        :param latitude_b: b点的维度，北纬，str或者float
        :return:两点之间的距离（float,米）
        '''
        flon_a = float(longitude_a)
        flat_a = 90 - float(latitude_a)
        flon_b = float(longitude_b)
        flat_b = 90 - float(latitude_b)
        R = 6371004    #地球平均半径，米
        C = math.sin(flat_a)*math.sin(flat_b)*math.cos(flon_a-flon_b) + math.cos(flat_a)*math.cos(flat_b)
        #print flon_a,'  ',flat_a,'  ',flon_b,'  ',flat_b,'  ',C
        if C > 1.0:
            #print C
            distance = 0.0
        else:
            distance = R * (math.acos(C)) * (math.pi) / 180
        '''
        try:
            distance = R*(math.acos(C))*(math.pi) / 180
        except Exception,e:
            print C,type(C)
            print e
            distance = 0.0
        '''
        return distance

def get_time_interval(string_time1,string_time2):
        '''
        计算时间差，同一天的两个时间，time2>time1
        :param string_time1: 时间（年-月-日 时：分：秒），str
        :param string_time2: 时间（年-月-日 时：分：秒），str
        :return: 时间差（int，秒）
        '''

        timeArray1 = (string_time1.split(' '))[1].split(':')
        timeArray2 = (string_time2.split(' '))[1].split(':')
        t1_sencond = 3600*int(timeArray1[0]) + 60*int(timeArray1[1]) + int(timeArray1[2])
        t2_sencond = 3600*int(timeArray2[0]) + 60*int(timeArray2[1]) + int(timeArray2[2])

        result = t2_sencond - t1_sencond

        return result

def mainfunc():
    '''
    运行主程序
    :return:无
    '''
    clean_data = CleanData()

    #list1 = clean_data.clean_null("nice50_src.txt")
    #print list1['null_count']
    #cleaned_null_dict = clean_data.get_perons_outing(list1['result_data'])
    #json.dump(cleaned_null_dict, open('nice50_src_dict', 'w'))

    #cleaned_null_data = json.load(open('data_source_3weeks_nonull_dict'))
    #add_day_data = (json.load(open('nice50_src_dict')))['result']

    #add_day_data = clean_data.add_day(cleaned_null_dict['result'])
    #cleaned_null_dict['result'] = add_day_data
    #json.dump(add_day_data,open('nice50_day_file','w'))
    #cleaned_exc = clean_data.clean_excursion_points(add_day_data)    #清洗偏移点
    #json.dump(cleaned_exc,open('nice50_exc_file','w'))

    #cleaned_exc = json.load(open('nice50_exc_file'))
    #cleaned_pingpang = clean_data.clean_pingpang_points2(cleaned_exc['result_data'])   #清洗乒乓切换点
    #json.dump(cleaned_pingpang, open('nice50_pp_file', 'w'))

    cleaned_pingpang = json.load(open('nice50_pp_file'))
    stay_data = clean_data.get_staying_points(cleaned_pingpang['result_data'])
    json.dump(stay_data, open('nice50_stay_file', 'w'))


if __name__ == '__main__':
    mainfunc()
    '''
    list1 = clean_null("nice50_src.txt")
    print list1['null_count']
    result = get_perons_outing(list1['result_data'])
    #for i in result['result']:
    #    print len(result['result'][i])
    json.dump(result,open('nice50_src_dict','w'))

    data = json.load(open('data_source_3weeks_nonull_dict'))
    counts = data['persons_count']
    user = data['persons_id']
    #print data['origin_length']
    #print sum(counts)
    '''
    '''
    no_repetition = list(set(counts))
    data_count = {}
    for i in no_repetition:
        data_count[str(i)] = counts.count(i)
    for i in no_repetition:
        print i, "：", data_count[str(i)]

    for i in range(len(counts)):
        if counts[i] == 20:
            print i,':',user[i]
    '''
    '''
    a_lon = 106.69808190431
    a_lat = 26.519530236353
    b_lon = 106.70042592788
    b_lat = 25.523387400982

    dis = get_distance(a_lon,a_lat,b_lon,b_lat)
    print dis

    time1 = "2016-09-01 00:31:50"
    time2 = "2016-09-01 00:50:15"
    print get_time_interval(time1,time2)
'''
    '''
    clean_data = CleanData()
    data = json.load(open('nice50_exc_file'))
    cleaned_pingpang = clean_data.clean_pingpang_points(data['result_data'])
    json.dump(cleaned_pingpang,open('nice50_pp_file','w'))

    data = json.load(open('nice50_pp_file'))
    print data['pingpang_information']['000302d702e11f0733516074c47caf08']
    '''






