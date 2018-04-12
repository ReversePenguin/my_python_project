#_*_ coding:utf-8 _*_

from multiprocessing import Pool
import time

def f(x):
    time.sleep(1)
    print x
    print 10*x
    return x*x

if __name__ == '__main__':
    p = Pool(10)
    print p.map(f,range(1,10))
