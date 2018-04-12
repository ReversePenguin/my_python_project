#_*_ coding:utf-8 _*_


'''
logistic回归算法
z = w*x+b
激活函数：sigmoid
梯度下降法训练模型

'''

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt



class LogisticRegression:
    def __init__(self):
        pass

    def sigmoid(self,z):
        return 1 / (1 + np.exp(-z))

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
        costs = []

        for i in range(n_iters):
            y_predict = self.sigmoid(np.dot(X, self.w) + self.b)
            cost = (-1 / m) * np.sum(Y * np.log(y_predict) + (1 - Y) * (np.log(1 - y_predict)))      #log() == ln

            dw = (1 / m) * np.dot(X.T, (y_predict - Y))
            db = (1 / m) * np.sum(y_predict - Y)

            self.w -= learning_rate * dw
            self.b -= learning_rate * db

            costs.append(cost)

            if (i+1) % 100 == 0:
                print("Cost at iteration{}:{}".format(i+1,cost))

        return self.w, self.b, costs

    def predict(self,X):
        y_predict = self.sigmoid(np.dot(X,self.w) + self.b)
        y_predict_labels = [1 if elem > 0.5 else 0 for elem in y_predict]    #四舍五入

        #确保维度
        return np.array(y_predict_labels)[:,np.newaxis]

    def accuracy(self,X,y):
        '''
        计算精确度的方法2
        :param X:
        :param y:
        :return:
        '''
        y_predict = self.sigmoid(np.dot(X,self.w) + self.b)
        accuracy = 100.0 - np.mean(1-(np.abs(y_predict-y) < 0.1))

        return accuracy

def train_using_gradient_descent(X_train, Y_train,X_test,Y_test):
    regressor = LogisticRegression()
    learning_rate = 0.01
    n_iters = 1000
    w_trained, b_trained, costs = regressor.train(X_train, Y_train, learning_rate,n_iters)

    fig1 = plt.figure(figsize=(8, 6))
    plt.plot(np.arange(n_iters), costs)
    plt.title("Development of cost during training")
    plt.xlabel("Number of iterations")
    plt.ylabel("Cost")


    y_p_train = regressor.predict(X_train)
    y_p_test = regressor.predict(X_test)

    #np.mean()：求均值
    #这里，相减之后，0说明是正确的，1说明是错误的，求均值刚好就是错误数据的占比
    print("train accuracy:{}%".format((100- np.mean(np.abs(y_p_train - Y_train)))))
    print("test accuracy:{}%".format((100 - np.mean(np.abs(y_p_test - Y_test)))))

    print("train accuracy2:{}%".format(regressor.accuracy(X_train,Y_train)))
    print("test accuracy2:{}%".format(regressor.accuracy(X_test, Y_test)))

    #plt.show([fig1])

def  make_data():
    np.random.seed(123)

    # 生成数据集,主义y的维度是（n_samples，）
    X, Y = make_blobs(n_samples=10000, n_features=2, centers=2)

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

if __name__ == '__main__':
    X_train, X_test, Y_train, Y_test = make_data()
    train_using_gradient_descent(X_train, Y_train, X_test, Y_test)




