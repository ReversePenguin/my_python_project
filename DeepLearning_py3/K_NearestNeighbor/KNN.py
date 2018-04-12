#_*_ coding:utf-8 _*_

'''
K最近邻算法，k-nn
'''

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt


class KNN():

    def __init__(self):
        pass

    def fit(self,X,Y):
        '''

        :param X: (m,n)
        :param Y: (m,)
        :return:
        '''
        self.data = X
        self.targets = Y

    def euclidean_distance(self,X):
        '''
        计算输入的X与训练数据每一个点之间的欧式距离
        :param X:
        :return:
        '''

        #a.ndim:返回a的维度，矩阵是2维,list是1维
        #输入一个单独点时
        if X.ndim == 1:
            #X:(1,n)
            #dis:(m_data,1)    m_data是self.data的行数
            dis = np.sqrt(np.sum((self.data - X)**2,axis=1))

        #输入一个矩阵时
        if X.ndim == 2:
            # X:(m,n)
            # dis:[(m_data,1),(m_data,1),...]该list的length==m
            m = X.shape[0]
            dis = [np.sqrt(np.sum((self.data - X[i])**2,axis=1)) for i in range(m)]

        return np.array(dis)

    def predict(self,X,k=1):

        dists = self.euclidean_distance(X)

        if X.ndim == 1:
            if k == 1:
                nn = np.argmin(dists)      #返回最小值的下标
                return self.targets[nn]
            else:
                knn = np.argsort(dists)[:k]      #返回从小到大排列的下标
                #print("ndim == 1,k>1:",knn)
                y_knn = self.targets[knn]
                #y_knn = [9,9,10, 10, 10]
                #print("ndim == 1,k>1:", y_knn)
                # 由于只有的一共有k个值，但是只能去一个值，所以，选择k个中出现最多次的那个作为最终值
                max_vote = max(y_knn, key=list(y_knn).count)
                return max_vote
        if X.ndim == 2:
            knn = np.argsort(dists)[:,:k]
            y_knn = self.targets[knn]
            if k == 1:
                #矩阵，(1,m)
                return y_knn.T
            else:
                m = X.shape[0]
                max_votes = [max(y_knn[i],key=list(y_knn[i]).count) for i in range(m)]
                #list，len() = m
                return max_votes

def training(X_train, Y_train,X_test,Y_test):
    knn = KNN()
    knn.fit(X_train,Y_train)
    '''
    print("Testing one datapoint, k=1")
    print('Predicted label:', knn.predict(X_test[0]))
    print("True label:",Y_test[0])
    print()
    print("Testing one datapoint, k=5")
    print('Predicted label:', knn.predict(X_test[20],k=5))
    print("True label:", Y_test[20])
    print()
    print("Testing 10 datapoint, k=1")
    print('Predicted label:', knn.predict(X_test[5:15], k=1))
    print("True label:", Y_test[5:15])
    print()
    print("Testing 10 datapoint, k=5")
    print('Predicted label:', knn.predict(X_test[5:15], k=5))
    print("True label:", Y_test[5:15])
    print()
    '''
    y_p_test1 = knn.predict(X_test,k=1)
    print(type(y_p_test1))
    print(y_p_test1.shape)
    test_acc1 = np.sum(y_p_test1[0] == Y_test)/len(y_p_test1[0]) * 100
    print("Test accuracy with k = 1: ",format(test_acc1))

    y_p_test2 = knn.predict(X_test, k=5)
    print(type(y_p_test2))

    test_acc2 = np.sum(y_p_test2 == Y_test) / len(y_p_test2) * 100
    print("Test accuracy with k = 5: ", format(test_acc2))






def make_data():
    '''
    生成初始数据
    :return:
    '''
    np.random.seed(123)
    digits = load_digits()
    X,Y = digits.data,digits.target#[:,np.newaxis]
    print(X.shape)
    print(Y.shape)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
    '''
    print('Shape X_train: {}'.format(X_train.shape))
    print('Shape y_train: ', Y_train.shape)
    print('Shape X_test: ', X_test.shape)
    print('Shape y_test: ', Y_test.shape)
    '''
    fig = plt.figure(figsize=(10,8))
    for i in range(10):
        ax = fig.add_subplot(2,5,i+1)
        plt.imshow(X[i].reshape((8,8)),cmap='gray')

    return X_train, X_test, Y_train, Y_test


if __name__ == '__main__':
    X_train, X_test, Y_train, Y_test = make_data()
    training(X_train, Y_train, X_test, Y_test)


