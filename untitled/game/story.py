#_*_ coding:utf-8 _*_

import time

begin_work = ['网管','洗碗工','扫地','搬砖']
begin_salary = ['2000','2000','2500','4000']

def Background(person):
    background = ' Hello,%s. Liz 是你高中同学时的恋人。' % person.Name
    time.sleep(1)
    print '你们决定考同一所大学。但是，高考你落榜了，选择工作：'
    for i in range(len(begin_work)):
        print i+1,begin_work[i],':',begin_salary[i]
    choose = raw_input()
    return choose

def go_work(choose):
    time.sleep(1)
    print '''
    ================================家里================================
    Liz考上了北京城市学院，而你因为落榜只好选择了%s的工作。
    你对liz说：“亲爱的，虽然我没有考上，但是我可以去工作，养你，供你读书”
    Liz很开心的亲了你一口，说：“亲爱的谢谢你，你最棒了，最喜欢你了”
    ''' % begin_work[choose-1]
    time.sleep(2)
    print '四年后，Liz成功毕业了'
    time.sleep(2)
    print '''
    ================================公司面试================================
    Peter：“Liz，你很优秀，我们公司很需要你，恭喜你成为了公司的一份子，明天来
    上班吧”
    Liz：“谢谢老板，我也很荣幸”
    两人握手后离去。。。
    '''
    time.sleep(2)
    print '''
    ================================家里================================
    Liz：“亲爱的，我通过面试啦，好开心，以后你就不用这么辛苦了，我可以养你”
    你说：“太棒了亲爱的，不辛苦，我很幸福呢，为了庆祝顺利工作，我们去吃烛光
    晚餐吧。”
    Liz：“讨厌。”
    两人度过了一个幸福的夜晚...
    '''
    time.sleep(2)
    print '''
    ================================公司================================
    Peter：“Liz，今天辛苦了，我请你吃个饭吧。”
    Liz：“嗯嗯，我也好饿了，走吧”
    Peter开着法拉利载Liz去了饭店。
    ......（你懂的）
    '''
    time.sleep(2)
    print '''
    ================================家里深夜================================
    你：“怎么还是那么迟回家啊，饿不饿，给你做吃的？”
    Liz：“不用，我在公司吃过了，我累了，我去睡觉了”
    沉默......
    '''
    time.sleep(2)







def life(person):
    choose = Background(person)
    go_work(int(choose))





