#_*_ coding:utf-8 _*_

'''Person类'''
class Person(object):
    #静态字段
    xue = 5
    
    def __init__(self,name,age,sex):
        #动态字段
        self.Name = name
        self.Age = age
        #私有字段
        self.__sex = sex
    
    #动态方法，类不能访问
    def action(self,doing):
        #正在做的事情
        print self.Name + doing
        
    #静态方法
    @staticmethod
    def Foo():
        print '中国人'
        
    #特性
    @property
    def Bar(self):
        #print self.Name
        return '善良'
    
    def __home(self):
        print '福州'    
    
    def Show(self):
        print self.__sex
        self.__home()
    
    #只读(如果不继承object，那么这里可以直接改，只有继承了object才是只读的)
    @property
    def Sex(self):
        return self.__sex
    
    #可改（需要类继承object）
    @Sex.setter
    def Sex(self,value):
        self.__sex = value
    
   
'''Person2类'''
class Person2:
    
    def __init__(self,name):
        self.__Name = name
        
    @property
    def Show(self):
        return self.__Name
    
    def __call__(self):
        print self.__Name + 'like' 

'''主程序'''

p1 = Person('小明',10,'男')
#类和对象都可以访问静态字段，类不能访问动态字段
print p1.Name,p1.xue,Person.xue
p1.action('走路')
Person.Foo()
p1.Foo()
print p1.Bar
p1.Show()
#强行调用私有方法
p1._Person__home()
p1.Name = '小红'
print p1.Name
print p1.Sex
p1.Sex = '女'
print p1.Sex

#无继承object时的特性测试
p2 = Person2('白')
print p2.Show
p2.Show = '空'
print p2.Show
p2('')






