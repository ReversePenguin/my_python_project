#_*_ coding:utf-8 _*_


'''遗传算法'''

import random
import time
import xlrd
import json
import copy
import os
import math
import get_instance


class GA(object):

    V = 3.6  #快递员的电动车行驶速度

    def __init__(self, max_generation=120, pmutation=0.01, population=100,N = 15):
        self.N = N #需求点的数量
        self.max_generation = max_generation   # 最大种群代数
        self.pmutation = pmutation   # 变异率
        self.population = population    # 种群大小
        self.memory_best_fit = []    #记录每次遗传最优的适应度值
        self.memory_best_fit_program = []    #记录每次遗传最优的配送方案

    def __rand_N(self,N):
        '''取1到N的随机排列'''
        item = []
        for i in range(N):
            item.append(i+1)
        random.shuffle(item)
        return item

    def __get_distance(self,point1,point2):
        return math.sqrt(pow((point1[0]-point2[0]),2)+pow((point1[1]-point2[1]),2))


    def get_fitness(self,one_n):
        '''
        获取适应度值：计算总成本（目标函数）。倒数即为适应度
        :param one_n: 种群的一个个体
        :return:字典：
        '''
        user_data = json.load(open('instance_data'))
        user_m = user_data['record_m']
        lines = user_data['lines']
        all_user_time = user_data['all_user_time']
        begin_time = 7  #快递员7点开始工作
        start_place = [0,0]   #仓库的位置
        record_time = []
        record_distance = []
        record_each_server_place = []

        for which_user in one_n:
            user_index = which_user - 1   #用户的下标
            end_place = []
            distance = 0
            one_time = 0
            for i in range(user_m[user_index] + 1):
                end_place = lines[user_index][i]
                distance = self.__get_distance(end_place,start_place)
                drive_time = distance/self.V/3600  #行驶时间
                #print all_user_time[user_index][i]
                user_real_start = all_user_time[user_index][i][0]   #该用户这个点的开始时间
                user_real_end = all_user_time[user_index][i][1]    #该用户这个点的结束时间
                server_time = round(random.uniform(5,10))/60.0
                one_time = begin_time+drive_time
                if one_time < user_real_start:  #小于开始时间，等待
                    one_time = user_real_start + server_time
                    break
                elif one_time < user_real_end:  #范围以内，服务
                    one_time += server_time
                    break
                else:   #超过这个范围，下一个点
                    if i == user_m[user_index]:   #万一出现无法再19点前服务完成的，则去客户家里服务
                        end_place = lines[user_index][i+1]
                        distance = self.__get_distance(end_place, start_place)
                        drive_time = distance / self.V/3600  # 行驶时间
                        one_time = begin_time+drive_time+server_time
                        break
                    continue

            begin_time = one_time
            start_place = end_place
            record_each_server_place.append(end_place)
            record_time.append(begin_time)   #每个客户的服务结束时间
            record_distance.append(distance)

        total_dis = sum(record_distance)
        fitness = 1.0/record_time[-1]

        result = {"fitness":fitness,'total_dis':total_dis,'program':one_n,'each_server_place':record_each_server_place,'record_time':record_time}
        return result

    def GA_select(self,all_n,fits):
        '''
        选择操作：选择适应度最高的一半个体保留
        :param all_n: 种群
        :param fits: 种群个体对应的适应度
        :return: 选择操作后的种群
        '''
        n = len(all_n)/2
        fits2 = sorted(fits,reverse=True)
        selected_result = []
        for i in range(n):
            selected_result.append(all_n[fits.index(fits2[i])])

        return selected_result

    def GA_crossover(self,parents):
        '''
        交叉操作
        :param parents: 种群
        :return: 交叉后的种群
        '''
        n = len(parents)
        m = self.N
        children = copy.copy(parents)
        flag = True
        i = 0
        while flag:
            parent1 = copy.copy(parents[i]); child1 = copy.copy(parent1); parent2 = copy.copy(parents[i+1]); child2 = copy.copy(parent2);
            indexs = []; indexs.append(random.randint(0,m-1)); indexs.append(random.randint(0,m-1));
            indexs = sorted(indexs)     #交叉范围
            for j in range(indexs[0],indexs[1]+1):
                if parent1[j] != parent2[j]:
                    child1[child1.index(parent2[j])] = child1[j]
                    child1[j] = parent2[j]
                    child2[child2.index(parent1[j])] = child2[j]
                    child2[j] = parent1[j]
                    parent1 = child1; parent2 = child2;
            children[i] = child1; children[i+1] = child2;
            i += 2
            if i >= n-1 :
                flag = False

        return children

    def GA_mutate(self,parents,p):
        '''
        变异操作
        :param parents: 种群
        :param p: 变异率
        :return: 变异后的种群
        '''
        n = len(parents); m = self.N; children = copy.copy(parents);
        for i in range(n):
            if random.random() < p:
                parent = copy.copy(parents[i]); child = copy.copy(parent);
                indexs = [];indexs.append(random.randint(0, m - 1));indexs.append(random.randint(0, m - 1));
                indexs = sorted(indexs)  # 变异范围
                for j in range(indexs[0],indexs[1]+1):
                    new_value = random.randint(1,m)
                    child[child.index(new_value)] = parent[j]
                    child[j] = new_value
                    parent = child
                children[i] = child

        #填充种群数量，，随机赋值
        for i in range(n,self.population):
            children.append(self.__rand_N(self.N))

        return children

    def GA_main(self):
        '''
        遗传算法的主程序
        '''

        GA_start_time = time.clock()    #记录算法开始的时间

        # 生成初始种群
        all_n = []
        for i in range(self.population):
            individual = self.__rand_N(self.N)
            all_n.append(individual)

        # 开始遗传
        for generation in range(self.max_generation):
            GA_start_time_each = time.clock()  #记录每次循环的开始时间

            #获取种群的适应度
            one_fits = []     #记录种群中每个个体的适应度值
            one_results = []   #记录种群中每个个体的配送方案
            for i in all_n:
                temp = self.get_fitness(i)
                one_fits.append(temp["fitness"])
                one_results.append(temp)

            #获取最优的方案，并保留
            best_index = one_fits.index(max(one_fits))
            best_one = all_n[best_index]
            self.memory_best_fit.append(1.0/one_fits[best_index])
            self.memory_best_fit_program.append(one_results[best_index])

            #选择、交叉、变异操作
            all_n = self.GA_select(all_n,one_fits)
            all_n = self.GA_crossover(all_n)
            all_n = self.GA_mutate(all_n,self.pmutation)
            all_n.append(best_one)

            GA_end_time_each = time.clock()  # 记录每次循环的结束时间
            record_each_time = '第 %d 次遗传用了 %f 时间' % (generation+1,GA_end_time_each-GA_start_time_each)
            print record_each_time

        #遗传算法结束，记录最优解
        for i in all_n:
            temp = self.get_fitness(i)
            one_fits.append(temp["fitness"])
            one_results.append(temp)
        best_index = one_fits.index(max(one_fits))
        self.memory_best_fit.append(1.0/one_fits[best_index])
        self.memory_best_fit_program.append(one_results[best_index])

        GA_end_time = time.clock()  # 记录算法结束的时间
        print'遗传算法一共用了 %f 时间' % ( GA_end_time - GA_start_time)






if __name__ == '__main__':
    #get_instance.get_instance_data()
    ga = GA()
    ga.GA_main()
    result_programs = ga.memory_best_fit_program
    result_fits = ga.memory_best_fit
    json.dump(result_programs,open("result_programs",'w'))
    json.dump(result_fits, open("result_fits",'w'))


