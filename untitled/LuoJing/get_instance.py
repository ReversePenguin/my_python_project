#_*_ coding:utf-8 _*_


import random
import json

def get_instance_data(N = 15 ):
      #用户数
    home_x_y = []
    location_x_y = []   #便于画图的存放形式
    location_x_y2 = []   #基于用户的存放形式
    lines = []
    record_m = []
    s1 = 3.6
    T = 8*3600
    home_r = s1*T/N
    p = 1
    all_user_time = []

    for i in range(N):
        one_home = []   #每个用户家的坐标
        one_home.append(round(random.uniform(0-home_r,home_r),2))
        one_home.append(round(random.uniform(0-home_r,home_r),2))
        home_x_y.append(one_home)
        if i <= int(round(0.6*N)):
            m = int(round(random.uniform(0,1)))   #每个用户的停留点数量
        else:
            m = int(round(random.uniform(0, 4)))
        record_m.append(m)
        one_location = []
        for j in range(m):
            location_x = round(random.uniform(one_home[0]-home_r*p/m,one_home[0]+home_r*p/m),2)
            location_y = round(random.uniform(one_home[1] - home_r * p / m, one_home[1] + home_r * p / m), 2)
            location_x_y.append([location_x,location_y])
            one_location.append([location_x, location_y])
        location_x_y2.append(one_location)
        temp = one_location
        temp.insert(0,one_home)
        temp.append(one_home)
        lines.append(temp)

        #用户时间生成
        
        first_begin = 7; first_end = 19;
        if i > int(round(0.7*N)):
            first_begin = 13
        #print first_begin
        user_time = []
        if m == 0:
            user_time = [[first_begin,first_end]]
        else:
            interval = (first_end - first_begin)/(m+1)
            begin = first_begin
            for i in range(m):
                end = first_begin + (i+1) * interval - 0.1*interval
                user_time.append([begin,end])
                begin = end + 1
            user_time.append([begin,first_end])
        all_user_time.append(user_time)



    data = {'home_x_y':home_x_y,'location_x_y':location_x_y,'location_x_y2':location_x_y2,'record_m':record_m,"lines":lines,'all_user_time':all_user_time}
    json.dump(data,open('instance_data','w'))
    return data


if __name__ == "__main__":
    data = get_instance_data()

    print data["home_x_y"]
    print data["location_x_y"]
    print data["record_m"]
    print data["lines"]
    print data['all_user_time']


