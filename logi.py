#!/usr/bin/env python
# multinomial_logistic_regression.py
# Author : Saimadhu Polamuri
# Date: 05-May-2017
# About: Multinomial logistic regression model implementation
 
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.externals import joblib
import time
import os
'''
model_dir = os.path.abspath('models')

def save_model(model):
    joblib.dump(model, os.path.join(model_dir, 'model.pkl'))
'''

def main():
    data=np.load('model_files/inceptionv4_results_avg_pool.npz')
    #['X_test', 'X_train', 'y_train', 'y_test']

    train_x=data['X_train'] 
    test_x=data['X_test']
    train_y=data['y_train']
    test_y=data['y_test']

    # Train multinomial logistic regression model
    mul_lr = linear_model.LogisticRegression(multi_class='ovr', solver='liblinear').fit(train_x,  train_y)
    predicted_class=mul_lr.predict(test_x)
    actual_class=test_y

    '''x=time.time()
    sgd_lr = linear_model.SGDClassifier(loss = 'log', penalty = 'l2', max_iter = 1000).fit(train_x,train_y)
    print "Training Time : ",time.time()-x
    save_model(sgd_lr)'''

    #model_path = os.path.abspath(os.path.join(model_dir, 'model.pkl'))
    #sgd_lr = joblib.load(model_path)
    
   	#print "Multinomial Logistic regression Train Accuracy :: ", metrics.accuracy_score(train_y, mul_lr.predict(train_x))

    for i in range(len(predicted_class)):
    	print "Predicted Class - ", predicted_class[i], "; Actual Class - ", actual_class[i]
    
    print "LR Test Accuracy :: ", metrics.accuracy_score(test_y, mul_lr.predict(test_x))
    #print "SGD  Test Accuracy :: ", metrics.accuracy_score(test_y, sgd_lr.predict(test_x))

 
if __name__ == "__main__":
    main()