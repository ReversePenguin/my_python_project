#_*_ coding:utf-8 _*_

import random
import pickle

def calendar(persons,days):
    task = {}
    n = len(persons) - 1
    rs = []
    for i in range(0,days):
        key = '第%s天' % str(i+1)
        while True:
            r = random.randint(0,n)
            rs.append(r)
            if rs.count(r) <= 2:
                break
            else:
                rs.pop()


        task[key] = persons[r]
    pickle.dump(task,open('calendar_task','w'))

def show():
    task = pickle.load(open('calendar_task'))
    for i in task:
        print i,task[i]


if __name__ == '__main__':
    persons = ['樊稼璇','肖斌','吴浩','张艺潇']
    days = 7
    print "-----每天的人是主要负责垃圾清理和电饭锅及其周边的清洁。。。鼓励其他人积极干活-----"
    print "这周的安排如下："
    #calendar(persons,days)
    show()




