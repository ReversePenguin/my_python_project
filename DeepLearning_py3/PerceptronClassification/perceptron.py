#_*_ coding:utf-8 _*_

'''
感知器分类
z = x*x + b
激活函数Heaviside step 函数：a = 1 ≥0，else 0
更新：
dw = afa * x*(a - y)
db = afa*(a- y)
w = w + dw
b = b + db
'''

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt


class Perceptrom:

    def __init__(self):
        pass

    def train(self,X,Y,learning_rate = 0.01, n_iters = 1000):
        '''
        使用梯度下降法进行训练
        :param X: 样本的X值，（m，n）
        :param Y: 样本的Y值，（m，1）
        :param learning_rate:
        :param n_iters:
        :return:
        '''
        m, n = X.shape  # 样本数量、维度
        self.w = np.zeros((n, 1))
        self.b = 0

        for i in range(n_iters):
            z = np.dot(X,self.w) + self.b
            a = self.step_function(z)

            dw = learning_rate * np.dot(X.T,a - Y)
            db = learning_rate * np.sum(a - Y)

            self.w += dw
            self.b += db

        return self.w,self.b


    def step_function(self,z):
        return np.array([1 if elem >= 0 else 0 for elem in z])[:,np.newaxis]

    def predict(self,X):
        z = np.dot(X, self.w) + self.b
        return self.step_function(z)


def training(X_train, Y_train,X_test,Y_test):
    regressor = Perceptrom()
    learning_rate = 0.01
    n_iters = 1000
    w_trained, b_trained = regressor.train(X_train, Y_train, learning_rate,n_iters)

    y_p_train = regressor.predict(X_train)
    y_p_test = regressor.predict(X_test)

    #np.mean()：求均值
    #这里，相减之后，0说明是正确的，1说明是错误的，求均值刚好就是错误数据的占比
    print("train accuracy:{}%".format((100- np.mean(np.abs(y_p_train - Y_train)))))
    print("test accuracy:{}%".format((100 - np.mean(np.abs(y_p_test - Y_test)))))

    plot_hyperplane(X_train,Y_train,w_trained, b_trained)

    #plt.show([fig1])

def  make_data():
    '''
    生成初始数据
    :return:
    '''
    np.random.seed(123)

    # 生成数据集,主义y的维度是（n_samples，）
    X, Y = make_blobs(n_samples=1000, n_features=2, centers=2)

    print(X[0:4,:])
    print(Y[0:100])
    print(X.shape)
    print(Y.shape)
    plt.scatter(X[:, 0], X[:, 1], c=Y)
    plt.title("Dataset")
    plt.xlabel("First feature")
    plt.ylabel("Second feature")
    # plt.show()

    Y = Y[:, np.newaxis]  # 转化Y的维度，变为（n_samples，1）
    print(Y.shape)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    print('Shape X_train: {}'.format(X_train.shape))
    print('Shape y_train: ', Y_train.shape)
    print('Shape X_test: ', X_test.shape)
    print('Shape y_test: ', Y_test.shape)

    return X_train, X_test, Y_train, Y_test

def plot_hyperplane(X,Y,w,b):

    slope = - w[0] / w[1]
    intercept = - b / w[1]
    x_hyperplane = np.linspace(-10, 10, 10)
    y_hyperplane = slope * x_hyperplane + intercept
    fig = plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=Y[:,0])
    plt.plot(x_hyperplane, y_hyperplane, '-')
    plt.title("Dataset and fitted decision hyperplane")
    plt.xlabel("First feature")
    plt.ylabel("Second feature")
    plt.show()


if __name__ == '__main__':
    X_train, X_test, Y_train, Y_test = make_data()
    training(X_train, Y_train, X_test, Y_test)

