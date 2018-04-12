#_*_ coding:utf-8 _*_

def outer(fun):
    def wrapper(avg):
        print '验证'
        result = fun(avg)
        print '东京'
        return result
    return wrapper

@outer
def func1(avg):
    print 'func1: '+ avg
    return '返回'
'''
func1(avg) =
    def wrapper(avg):
        print '验证'
        result = fun(avg)
        print '东京'
        return result

'''

'''
@outer
def func2():
    print 'func2'

@outer
def func3():
    print 'func3'

'''
    
result = func1('老客户')
print result


