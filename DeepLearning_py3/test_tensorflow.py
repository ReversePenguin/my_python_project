#_*_ coding:utf-8 _*_

'''
tensorflow框架小试
'''

import numpy as np
import tensorflow as tf

coefficients = np.array([[1],[-2],[1]])      #系数

w = tf.Variable([0],dtype=tf.float32)      #需要优化的参数
x = tf.placeholder(tf.float32, [3,1])      #训练的数据
cost = x[0][0] * w**2 + x[1][0]*w + x[2][0]      #损失函数
train = tf.train.GradientDescentOptimizer(0.001).minimize(cost)      #梯度下降法，学习率为0.01

init = tf.global_variables_initializer()
session = tf.Session()
session.run(init)

print(session.run(w))

#经过  次训练
for i in range(10000):
    session.run(train, feed_dict={x:coefficients})
#输出训练结果
print(session.run(w))





