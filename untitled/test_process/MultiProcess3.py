#_*_ coding:utf-8 _*_

from multiprocessing import Pool
import time

def f(x):
    print x*x
    time.sleep(1)
    return x*x

if __name__ == '__main__':
    #CPU的核数或者两倍
    pool = Pool(5)
    res = []
    for i in range(1,11):
        #异步,先创建进程，储存到列表，形成进程池
        r = pool.apply_async(f,[i])
        res.append(r)
    #调用进程里面的函数
    for i in res:
        print i.get()
'''楼上这么多相当于MultiProcess2中的方法'''


