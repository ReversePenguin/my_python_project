#_*_ coding:utf-8 _*_

'''
线性回归
a = z = w*x + b
梯度下降法更新系数
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class LinearRegression:

    def __init__(self):
        pass

    def train_gradient_descent(self,X,Y,learning_rate = 0.01, n_iters = 100):
        '''
        使用梯度下降法进行训练
        :param X: 样本的X值，（m，n）
        :param Y: 样本的Y值，（m，1）
        :param learning_rate:学习率
        :param n_iters:迭代次数
        :return:
        '''
        m, n = X.shape     #样本数量、维度
        self.w = np.zeros((n,1))
        self.b = 0
        costs = []

        for i in range(n_iters):
            y_predict = np.dot(X,self.w) + self.b       #激活函数，a = w*x + b
            cost = (1/m) * np.sum((y_predict - Y)**2)      #成本函数
            costs.append(cost)

            #每一百个打印一次成本函数数值
            if i % 100 == 0:
                print("Cost at iteration{}:{}".format(i,cost))

            dw = (2/m) * np.dot(X.T,(y_predict - Y))      #w对成本函数的偏导
            db = (2/m) * np.sum((y_predict - Y))      #b对成本函数的偏导

            self.w = self.w - learning_rate*dw      #更新w
            self.b -= learning_rate*db      #更新b

        return self.w,self.b,costs


    def train_normal_equation(self,X,Y):
        '''
        使用正太方程进行训练
        :param X:
        :param Y:
        :return:
        '''
        self.w = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), Y)
        self.b = 0

        return self.w,self.b


    def predict(self,X):
        return np.dot(X,self.w) + self.b

def train_using_gradient_descent(X_train, Y_train,X_test,Y_test):
    regressor = LinearRegression()

    #训练
    learning_rate = 0.005
    n_iters = 600
    w_trained, b_trained, costs = regressor.train_gradient_descent(X_train, Y_train, learning_rate, n_iters)
    print(regressor.w)
    print(regressor.b)

    #绘图
    fig1 = plt.figure(figsize=(8,6))
    plt.plot(np.arange(n_iters),costs)
    plt.title("Development of cost during training")
    plt.xlabel("Number of iterations")
    plt.ylabel("Cost")

    #测试
    m_test,_ = X_test.shape
    m_train, _ = X_train.shape

    y_p_train = regressor.predict(X_train)
    y_p_test = regressor.predict(X_test)

    error_train = (1 / m_train) * np.sum((y_p_train - Y_train) ** 2)
    error_test = (1 / m_test) * np.sum((y_p_test - Y_test) ** 2)

    print("Error on training set: ",np.round(error_train, 4))
    print("Error on test set: ",np.round(error_test,4))

    #可视化预测值
    fig2 = plt.figure(figsize=(8, 6))
    plt.scatter(X_test, Y_test)
    plt.scatter(X_test, y_p_test)
    plt.xlabel("First feature")
    plt.ylabel("Second feature")
    plt.show([fig1,fig2])




if __name__ == '__main__':

    np.random.seed(123)      #使下一次rand的取值固定，即不会运行一次变一次   ???测试结果全都固定？？

    X = 2 * np.random.rand(500,1)      #取均匀分布的随机值
    Y = 5 + 3*X + np.random.randn(500,1)      #取正太分布的随机值

    #画图
    fig = plt.figure(figsize=(8,6))
    plt.scatter(X,Y)
    plt.title('train set')
    plt.xlabel("X")
    plt.ylabel("Y")
    #plt.show()

    #划分训练集和测试集
    #使用这个时X：(m,n),Y:(m,n)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)       #默认是75%/25%
    print('Shape X_train: {}'.format(X_train.shape))
    print('Shape y_train: ',Y_train.shape)
    print('Shape X_test: ',X_test.shape)
    print('Shape y_test: ',Y_test.shape)

    train_using_gradient_descent(X_train, Y_train, X_test, Y_test)





