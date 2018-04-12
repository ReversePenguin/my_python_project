#_*_ coding:utf-8 _*_


'''
K-Means 是一种非常简单的聚类算法(聚类算法都属于无监督学习)。
给定固定数量的聚类和输入数据集，该算法试图将数据划分为聚类，使得聚类内部具有较高的相似性，聚类与聚类之间具有较低的相似性。

算法原理
1. 初始化聚类中心，或者在输入数据范围内随机选择，或者使用一些现有的训练样本(推荐)
2. 直到收敛
    将每个数据点分配到最近的聚类。点与聚类中心之间的距离是通过欧几里德距离测量得到的。
    通过将聚类中心的当前估计值设置为属于该聚类的所有实例的平均值，来更新它们的当前估计值。

目标函数
    数据与其最接近的聚类中心之间的距离尽可能小


K-Means 算法的缺点：
    聚类的个数在开始就要设定
    聚类的结果取决于初始设定的聚类中心
    对异常值很敏感
    不适合用于发现非凸聚类问题
    该算法不能保证能够找到全局最优解，因此它往往会陷入一个局部最优解

'''

import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.datasets import make_blobs


class KMeans():

    def __init__(self,n_clusters = 4):
        '''

        :param n_clusters: 聚类中心的数量
        '''
        self.k = n_clusters


    def fit(self,data):
        '''

        :param data: (m,n)
        :return:
        '''

        m = data.shape[0]

        #初始化中心点
        #在样本本随机选择k个点作为中心点
        self.centers = np.array(random.sample(list(data),self.k))
        self.initial_centers = np.copy(self.centers)

        old_assigns = None
        n_iters = 0

        while True:
            #每个样本点对应的中心点的下标,(m,1)
            new_assigns = [self.classify(datapoint) for datapoint in data]

            #如果两次的中心都是一样的，说明无法再优化了，则输出最终结果
            if new_assigns == old_assigns:
                print("Training finished after {} iterations!".format(n_iters))
                return

            old_assigns = new_assigns
            n_iters += 1

            for i in range(self.k):
                points_idx = np.where(np.array(new_assigns) == i)     #返回new_assigns中符合条件的元素的下标
                datapoints = data[points_idx]
                self.centers[i] = datapoints.mean(axis = 0)      #新的中心是这一类新的点的平均坐标


    def l2_distance(self,datapoint):
        '''
        输入点与各个中心点之间的距离
        :param datapoint: (1,n)
        :return: (self.k,1)
        '''
        dists = np.sqrt(np.sum((self.centers -datapoint)**2, axis=1))
        return dists

    def classify(self,datapoint):
        '''

        :param datapoint: (1,n)
        :return:中心点的下标,int
        '''
        dists = self.l2_distance(datapoint)
        return np.argmin(dists)

    def plot_clusters(self,data):
        plt.figure(figsize=(12, 10))
        plt.title("Initial centers in black, final centers in red")
        plt.scatter(data[:, 0], data[:, 1], marker='.')
        plt.scatter(self.centers[:, 0], self.centers[:, 1], c='r')
        plt.scatter(self.initial_centers[:, 0], self.initial_centers[:, 1], c='k')
        plt.show()



def  make_data():
    '''
    生成初始数据
    :return:
    '''
    np.random.seed(123)

    # 生成数据集,主义y的维度是（n_samples，）
    X, Y = make_blobs(n_samples=1000, n_features=2, centers=4)

    print(X.shape)
    print(Y.shape)
    plt.scatter(X[:, 0], X[:, 1], c=Y)
    plt.title("Dataset")
    plt.xlabel("First feature")
    plt.ylabel("Second feature")
    #plt.show()

    Y = Y[:, np.newaxis]  # 转化Y的维度，变为（n_samples，1）
    print(Y.shape)


    return X,Y

if __name__ == "__main__":
    X,Y = make_data()
    kmeans = KMeans()
    kmeans.fit(X)
    kmeans.plot_clusters(X)






