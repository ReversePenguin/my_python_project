#_*_ coding:utf-8 _*_

'''遗传算法'''

import random
import time
import xlrd
import json
import copy
import os


class GA(object):
    N = 36 #需求点的数量

    def __init__(self, max_generation=120, pmutation=0.01, population=100):
        self.max_generation = max_generation   # 最大种群代数
        self.pmutation = pmutation   # 变异率
        self.population = population    # 种群大小
        self.memory_best_fit = []    #记录每次遗传最优的适应度值
        self.memory_best_fit_program = []    #记录每次遗传最优的车辆配送方案

    def __rand_N(self,N):
        '''取1到N的随机排列'''
        item = []
        for i in range(N):
            item.append(i+1)
        random.shuffle(item)
        return item

    def __get_marix(self,filename):
        '''
        获取数据矩阵
        :param filename:文件名  .xlsx
        :return:数据矩阵
        '''
        rfile = xlrd.open_workbook(filename)
        table = rfile.sheet_by_index(0)
        nrows = table.nrows
        ncols = table.ncols
        result_marix = []

        for i in range(nrows):
            temp = []
            for j in range(ncols):
                temp.append(float(table.cell(i,j).value))
            result_marix.append(temp)

        return result_marix


    def get_fitness(self,one_n_f):
        '''
        获取适应度值：计算总成本（目标函数）。倒数即为适应度
        :param one_n_f: 种群的一个个体
        :return:字典：适应度、总成本、载货量、总时间、路径方案、车辆数、初始方案
        '''
        origin_path =  os.path.abspath(os.curdir)
        DIS = self.__get_marix(origin_path+"\distance.xlsx")  # 导入距离矩阵，包含车场
        DRIVETIME = self.__get_marix(origin_path+r"\time.xlsx")    # 导入行驶时间矩阵, 小时制，包含车场
        TIMEON = self.__get_marix(origin_path+r"\timeon.xlsx")    # 导入停留时间，小时制
        TIMELIMIT = self.__get_marix(origin_path+r"\timelimit.xlsx")   # 导入到达时间约束，小时制
        REQ = self.__get_marix(origin_path+r"\REQ.xlsx")  # 导入需求
        MAXLOAD = 7.0   # 车辆的载重量
        C = 2.0   # 车辆行驶一公里的成本
        FIXED = 400.0   #车辆的启动成本

        final = []
        one_n = []

        #找出不符合实际的客户：离配送中心120公里
        for i in one_n_f:
            if DIS[0][i] > 120:
                temp = []; temp.append(i);final.append(temp);
            else:
                one_n.append(i)

        M = len(one_n)
        #分割路径
        start_end = True
        start_index = 0  # 需求点游标
        while start_end:
            total_req = 0
            total_time = 6 + DRIVETIME[0][one_n[start_index]]  # 早上六点出发
            for i in range(start_index,M):
                if i == M - 1:
                    temp = one_n[start_index:(i+1)]
                    final.append(temp)
                    start_end = False
                    break
                real_point = one_n[i] - 1     #需求点的编号,注意下标对应
                real_next_point = one_n[i+1] - 1  #下一个需求点的编号,注意下标对应
                total_req += REQ[real_point][0]    #需求量
                total_time += TIMEON[real_point][0]   #加上停留时间，小时
                drive_time = DRIVETIME[real_point+1][real_next_point+1]    #到下一个点的行驶时间
                #时间约束和载重量约束
                if total_req + REQ[real_next_point][0] > MAXLOAD or total_time + drive_time > TIMELIMIT[real_next_point][0]:
                    temp = one_n[start_index:(i+1)]
                    final.append(temp)
                    start_index = i + 1
                    break
                total_time += drive_time     #记录总的运行时间

        #计算总成本
        car_req = []  # 记录每辆车的载货量
        car_time = []  # 记录每辆车直到回到配送中心消耗的时间
        car_dis = []   #记录每辆车的行驶路程
        car_cost = []   #记录每辆车的成本,距离
        car_count = len(final)   #记录使用的车辆数
        for i in range(car_count):
            one_dis = 0
            one_cost = FIXED
            one_time = 0
            one_req = 0
            #获取车辆路径，并加入配送中心
            car_route = final[i]
            car_route.insert(0,0)
            car_route.append(0)
            for j in range(len(car_route)):
                if j == len(car_route) - 1:
                    break
                begin_index = car_route[j]
                next_index = car_route[j+1]
                one_dis += DIS[begin_index][next_index]   #加上行驶费用
                one_time += DRIVETIME[begin_index][next_index]   #加上行驶时间
                if next_index != 0:
                    one_time += round(TIMEON[next_index - 1][0] ,2)    #加上停留时间
                    one_req += REQ[next_index - 1][0]    #加上需求点的需求
            one_cost += C*one_dis
            car_dis.append(one_dis)
            car_req.append(one_req)
            car_cost.append(one_cost)
            car_time.append(one_time)

        #整理需要返回的结果
        total_cost = sum(car_cost)    #总成本
        fitness = 1.0/total_cost    #适应度

        result = {"fitness":fitness,"total_cost":total_cost,"total_req":car_req,"total_dis":car_dis,"each_cost":car_cost,
                  "total_time":car_time,"final_program":final,"car_count":car_count,"origin_program":one_n
                  }
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
    ga = GA()
    ga.GA_main()
    result_programs = ga.memory_best_fit_program
    result_fits = ga.memory_best_fit
    print result_programs[-1]["final_program"]
    #json.dump(result_programs,open("result_programs",'w'))
    #json.dump(result_fits, open("result_fits",'w'))
