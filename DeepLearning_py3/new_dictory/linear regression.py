import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
np.random.seed(123)

# use a simple training set
X = 2*np.random.rand(500,1)
y = 5+3*X+np.random.randn(500,1)
fig = plt.figure(figsize=(8,6))
plt.scatter(X,y)
plt.title('Dataset')
plt.xlabel('first feature')
plt.ylabel('second feature')
#plt.show()

# split the data into a training and test set
X_train, X_test, y_train, y_test = train_test_split(X,y)


# linear regression
class LinearRegression:
    
    def __init__(self):
        pass

    def train_gradient_descent(self,X,y,learning_rate=0.001,n_iters=100):
        #step 0: initialize the parameters
        n_samples, n_features = X.shape
        self.weights = np.zeros(shape=(n_features,1))
        self.bias = 0
        costs = []

        for i in range (n_iters):
            #step 1: compute a linear combination of the input features and weights
            y_predict = np.dot(X,self.weights)+self.bias

            #step 2: compute cost over training set
            cost = (1.0/n_samples)*np.sum((y_predict-y)**2)
            costs.append(cost)

            if i % 100 == 0:
                print ('cost at iteration',  i, ': ',cost)

            #step 3: compute the gradients
            dJ_dw = 2.0/n_samples*np.dot(X.T,(y_predict-y))
            dJ_db = 2.0/n_samples*np.sum(y_predict-y)

            #step 4: update the patameters
            self.weights = self.weights - learning_rate*dJ_dw
            self.bias = self.bias - learning_rate*dJ_db

        return self.weights, self.bias, costs

    def train_normal_equation(self,X,y):
        self.weights = np.dot(np.dot(np.linalg.inv(np.dot(X.T,y)),X.T),y)
        self.bias = 0

        return self.weights, self.bias

    def predict(self,X):
        return np.dot(X,self.weights)+self.bias

regressor = LinearRegression()
w_trained, b_trained, costs = regressor.train_gradient_descent(X_train, y_train, learning_rate=0.005, n_iters=600)
fig = plt.figure(figsize=(8,6))
plt.plot(np.arange(600),costs)
plt.title('development of cost during training')
plt.xlabel('Number of iterations')
plt.ylabel('Cost')
#plt.show()






        
