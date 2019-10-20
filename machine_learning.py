# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 10:48:25 2019
复现课程代码2  machine learning
@author: us
"""
from sklearn.datasets import load_boston
import random
import matplotlib.pyplot as plt

dataset = load_boston()
x,y=dataset['data'],dataset['target']
dataset['DESCR']
'''
:Attribute Information (in order):
    - CRIM     per capita crime rate by town
    - ZN       proportion of residential land zoned for lots over 25,000 sq.ft.
    - INDUS    proportion of non-retail business acres per town
    - CHAS     Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
    - NOX      nitric oxides concentration (parts per 10 million)
    - RM       average number of rooms per dwelling
    - AGE      proportion of owner-occupied units built prior to 1940
    - DIS      weighted distances to five Boston employment centres
    - RAD      index of accessibility to radial highways
    - TAX      full-value property-tax rate per $10,000
    - PTRATIO  pupil-teacher ratio by town
    - B        1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
    - LSTAT    % lower status of the population
    - MEDV     Median value of owner-occupied homes in $1000's
'''
X_rm = x[:,5]

# plot the RM with respect to y
plt.scatter(X_rm,y)

'''
=============================Gradient descent==================================
Assume that the target funciton is a linear function
y=k∗rm+b
'''
#define target function
def price(rm, k, b):
    return k * rm + b

'''
Define mean square loss
loss=1n∑(yi−yi^)2
loss=1n∑(yi−(kxi+bi))2
'''
# define loss function 
def loss(y,y_hat):
    return sum((y_i - y_hat_i)**2 for y_i, y_hat_i in zip(list(y),list(y_hat)))/len(list(y))

'''
Define partial derivatives
∂loss∂k=−2n∑(yi−yi^)xi
∂loss∂k=−2n∑(yi−yi^)xi
∂loss∂b=−2n∑(yi−yi^)
'''
# define partial derivative 
def partial_derivative_k(x, y, y_hat):
    n = len(y)
    gradient = 0
    for x_i, y_i, y_hat_i in zip(list(x),list(y),list(y_hat)):
        gradient += (y_i-y_hat_i) * x_i
    return -2/n * gradient

def partial_derivative_b(y, y_hat):
    n = len(y)
    gradient = 0
    for y_i, y_hat_i in zip(list(y),list(y_hat)):
        gradient += (y_i-y_hat_i)
    return -2 / n * gradient

#initialized parameters

k = random.random() * 200 - 100  # -100 100
b = random.random() * 200 - 100  # -100 100

learning_rate = 1e-3

iteration_num = 200 
losses = []
for i in range(iteration_num):
    
    price_use_current_parameters = [price(r, k, b) for r in X_rm]  # \hat{y}
    
    current_loss = loss(y, price_use_current_parameters)
    losses.append(current_loss)
    print("Iteration {}, the loss is {}, parameters k is {} and b is {}".format(i,current_loss,k,b))
    
    k_gradient = partial_derivative_k(X_rm, y, price_use_current_parameters)
    b_gradient = partial_derivative_b(y, price_use_current_parameters)
    
    k = k + (-1 * k_gradient) * learning_rate
    b = b + (-1 * b_gradient) * learning_rate
best_k = k
best_b = b

plt.plot(list(range(iteration_num)),losses)

price_use_best_parameters = [price(r, best_k, best_b) for r in X_rm]
plt.scatter(X_rm,y)
plt.scatter(X_rm,price_use_current_parameters)





















