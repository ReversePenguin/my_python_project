#_*_ coding:utf-8 _*_

de = ['demo','demo1']
func = 'Foo'

module = __import__(de[0])
funct = getattr(module,func)
funct()

mod = __import__('test1.'+de[1])
print '第一步：'+mod.__name__
mod2 = getattr(mod,de[1])
print '第二步：'+mod2.__name__
funct = getattr(mod2,func)
funct()
