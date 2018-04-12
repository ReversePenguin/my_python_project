#_*_ coding:utf-8 _*_

a = [1,2,3,4,5,1,2,3,4,5,2]

a1 = a
index = []
#quest = input("请输入你要查找的数字：")

'''
first = a1.index(quest);
index.append(first)
for i in range(a.count(quest)):
    post = a.index(quest,post+1)
    index.append(post)
print ("%d 的下标为： " % quest) ,index
for i in range(a.count(quest)-1):
    a1 = a[first+1:]
    first += a1.index(quest)+1
    index.append(first)
 '''
g = [x*x for x in range(1,9)]
li = ['m'+ str(m) + '-'+ str(n) for m in range(4) for n in g]
print li
print len(li)
